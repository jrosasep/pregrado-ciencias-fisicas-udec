"""
Visualización interactiva del campo de Liénard–Wiechert
=======================================================

Visualiza, en el plano xy, el campo eléctrico de una carga puntual en movimiento
sublumínico. Se separan el término de velocidad (~1/R²) y el término radiativo
(~1/R), evaluados en el tiempo retardado. El panel polar muestra en tiempo real
la forma angular normalizada de dP/dΩ.

La interfaz está optimizada para actualización interactiva: la dinámica, el campo
retardado y el patrón angular se calculan a frecuencias distintas; los artistas de
Matplotlib se actualizan en sitio y, cuando el backend lo permite, se usa blitting.

Unidades normalizadas: el objetivo es mostrar la estructura espacial y angular de
la solución, no fijar una escala SI concreta.
"""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import RadioButtons, Button

# -----------------------------------------------------------------------------
# Modelo numérico
# -----------------------------------------------------------------------------
K_E = 1.0
Q = 1.0
C = 4.0
BETA_MAX = 0.72
DOMAIN = 5.0
N_GRID = 31                 # mapa más fino; el cálculo retardado fue optimizado
DT = 0.025                  # integración interna de la trayectoria
HIST_LEN = 720
R_MIN = 0.28
RETARDED_ITERS = 7          # iteración de punto fijo; converge porque |beta|<1
FOLLOW_TIME = 0.22
VELOCITY_SMOOTH = 0.11
ACCEL_SMOOTH = 0.12

# Frecuencias desacopladas. El campo es la parte costosa.
TIMER_MS = 20               # timer de interfaz, ~50 Hz máximo
FIELD_PERIOD = 0.085        # ~12 Hz
POLAR_PERIOD = 0.045        # ~22 Hz
STATUS_PERIOD = 0.12
RENDER_PERIOD = 0.033       # objetivo visual ~30 fps
QUIVER_STEP = 3             # 11 x 11 flechas

# Estética
PAPER = "#f5f4ef"
SURFACE = "#ffffff"
INK = "#172433"
MUTED = "#667085"
NAVY = "#003a70"
NAVY2 = "#145a8d"
RULE = "#cbd2da"
GOLD = "#b27a2e"
RADIATION = "#8f4f69"
GRID = "#e1e6ec"

# -----------------------------------------------------------------------------
# Grilla espacial
# -----------------------------------------------------------------------------
x1 = np.linspace(-DOMAIN, DOMAIN, N_GRID)
y1 = np.linspace(-DOMAIN, DOMAIN, N_GRID)
X, Y = np.meshgrid(x1, y1)
R_OBS = np.column_stack((X.ravel(), Y.ravel()))
QX = X[::QUIVER_STEP, ::QUIVER_STEP]
QY = Y[::QUIVER_STEP, ::QUIVER_STEP]

# -----------------------------------------------------------------------------
# Historial circular
# -----------------------------------------------------------------------------
hist = {k: np.zeros(HIST_LEN) for k in ("t", "x", "y", "vx", "vy", "ax", "ay")}
hist.update(ptr=0, n=0)


def hist_push(t, x, y, vx, vy, ax, ay) -> None:
    p = hist["ptr"]
    for k, v in zip(("t", "x", "y", "vx", "vy", "ax", "ay"),
                    (t, x, y, vx, vy, ax, ay)):
        hist[k][p] = v
    hist["ptr"] = (p + 1) % HIST_LEN
    hist["n"] = min(hist["n"] + 1, HIST_LEN)


def hist_clear_rest() -> None:
    hist["ptr"] = 0
    hist["n"] = 0
    t0 = -(HIST_LEN - 1) * DT
    for i in range(HIST_LEN):
        hist_push(t0 + i * DT, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)


def hist_arrays():
    n = hist["n"]
    if n < HIST_LEN:
        idx = np.arange(n)
    else:
        p = hist["ptr"]
        idx = np.r_[np.arange(p, HIST_LEN), np.arange(0, p)]
    return tuple(hist[k][idx] for k in ("t", "x", "y", "vx", "vy", "ax", "ay"))


def interp_uniform(tq: np.ndarray, t0: float, arrays: tuple[np.ndarray, ...]):
    """Interpolación lineal rápida para un historial temporal uniformemente espaciado."""
    u = (np.asarray(tq) - t0) / DT
    i = np.floor(u).astype(np.int64)
    n = len(arrays[0])
    i = np.clip(i, 0, n - 2)
    f = np.clip(u - i, 0.0, 1.0)
    return tuple(a[i] * (1.0 - f) + a[i + 1] * f for a in arrays)

# -----------------------------------------------------------------------------
# Campo de Liénard–Wiechert
# -----------------------------------------------------------------------------
def campos_en_puntos(t_obs: float, obs: np.ndarray):
    t_arr, x_arr, y_arr, vx_arr, vy_arr, ax_arr, ay_arr = hist_arrays()
    npts = len(obs)
    z = np.zeros((npts, 2), dtype=float)
    if len(t_arr) < 2:
        return {"vel": z.copy(), "rad": z.copy(), "tot": z.copy(),
                "mask": np.zeros(npts, dtype=bool)}

    t0, t1 = float(t_arr[0]), float(t_arr[-1])

    # Estimación inicial: posición presente. La ecuación
    # t_ret = t_obs - |r-rq(t_ret)|/c es contractiva para |v|/c<1.
    rnow = np.array([x_arr[-1], y_arr[-1]])
    tret = t_obs - np.linalg.norm(obs - rnow[None, :], axis=1) / C
    tret = np.clip(tret, t0, t1)

    for _ in range(RETARDED_ITERS):
        rx, ry = interp_uniform(tret, t0, (x_arr, y_arr))
        R = np.hypot(obs[:, 0] - rx, obs[:, 1] - ry)
        tnew = np.clip(t_obs - R / C, t0, t1)
        # pequeña relajación: elimina oscilaciones cerca del límite relativista
        tret = 0.15 * tret + 0.85 * tnew

    rx, ry, vx, vy, ax, ay = interp_uniform(
        tret, t0, (x_arr, y_arr, vx_arr, vy_arr, ax_arr, ay_arr)
    )
    Rx = obs[:, 0] - rx
    Ry = obs[:, 1] - ry
    R = np.hypot(Rx, Ry)
    valid_history = (tret > t0 + 1.5 * DT)
    mask = valid_history & (R > R_MIN)
    Rs = np.where(mask, R, 1.0)
    nx, ny = Rx / Rs, Ry / Rs

    bx, by = vx / C, vy / C
    beta2 = np.minimum(bx * bx + by * by, 0.999**2)
    bdx, bdy = ax / C, ay / C
    kappa = np.maximum(1.0 - nx * bx - ny * by, 1e-4)

    fac_v = K_E * Q * (1.0 - beta2) / (kappa**3 * Rs**2)
    Evx = (nx - bx) * fac_v
    Evy = (ny - by) * fac_v

    ndotbd = nx * bdx + ny * bdy
    fac_r = K_E * Q / (C * kappa**3 * Rs)
    Erx = ((nx - bx) * ndotbd - bdx * kappa) * fac_r
    Ery = ((ny - by) * ndotbd - bdy * kappa) * fac_r

    for a in (Evx, Evy, Erx, Ery):
        a[~mask] = 0.0

    vel = np.column_stack((Evx, Evy))
    rad = np.column_stack((Erx, Ery))
    return {"vel": vel, "rad": rad, "tot": vel + rad, "mask": mask}


def calcular_campos(t_obs: float):
    f = campos_en_puntos(t_obs, R_OBS)
    sh = X.shape
    return {
        "vel": (f["vel"][:, 0].reshape(sh), f["vel"][:, 1].reshape(sh)),
        "rad": (f["rad"][:, 0].reshape(sh), f["rad"][:, 1].reshape(sh)),
        "tot": (f["tot"][:, 0].reshape(sh), f["tot"][:, 1].reshape(sh)),
        "mask": f["mask"].reshape(sh),
    }


def patron_radiacion_angular(nang: int = 361):
    theta = np.linspace(0.0, 2.0 * np.pi, nang)
    n = np.column_stack((np.cos(theta), np.sin(theta), np.zeros_like(theta)))
    beta = np.array([sim["vx"] / C, sim["vy"] / C, 0.0])
    beta_dot = np.array([sim["ax"] / C, sim["ay"] / C, 0.0])
    b2 = float(beta @ beta)
    if b2 >= 0.999**2:
        beta *= 0.999 / np.sqrt(b2)
    inner = np.cross(n - beta[None, :], beta_dot[None, :])
    outer = np.cross(n, inner)
    numer = np.einsum("ij,ij->i", outer, outer)
    kappa = np.maximum(1.0 - n @ beta, 1e-5)
    p = numer / kappa**5
    pmax = float(np.max(p)) if p.size else 0.0
    pn = p / pmax if pmax > 1e-14 else np.zeros_like(p)
    return theta, p, pn


def field_display(Ex: np.ndarray, Ey: np.ndarray):
    """Mapa logarítmico relativo y flechas comprimidas, ambos robustos a la singularidad."""
    mag = np.hypot(Ex, Ey)
    finite = mag[np.isfinite(mag) & (mag > 0)]
    scale = float(np.percentile(finite, 92)) if finite.size else 1.0
    scale = max(scale, 1e-12)
    display = np.log1p(mag / scale) / np.log(2.0)
    display = np.clip(display, 0.0, 1.0)

    # La dirección es exacta; la longitud de la flecha se comprime con tanh.
    amp = np.tanh(mag / scale)
    inv = np.divide(1.0, mag, out=np.zeros_like(mag), where=mag > 1e-13)
    U = Ex * inv * amp
    V = Ey * inv * amp
    return display, U, V, mag

# -----------------------------------------------------------------------------
# Dinámica sublumínica
# -----------------------------------------------------------------------------
sim = dict(t=0.0, x=0.0, y=0.0, vx=0.0, vy=0.0, ax=0.0, ay=0.0,
           target_x=0.0, target_y=0.0, drag=False, paused=False)


def reset_simulation() -> None:
    sim.update(t=0.0, x=0.0, y=0.0, vx=0.0, vy=0.0, ax=0.0, ay=0.0,
               target_x=0.0, target_y=0.0, drag=False, paused=False)
    hist_clear_rest()


def advance_charge(dt: float) -> None:
    d = np.array([sim["target_x"] - sim["x"], sim["target_y"] - sim["y"]])
    desired = d / max(FOLLOW_TIME, dt)
    vmax = BETA_MAX * C
    s = np.linalg.norm(desired)
    if s > vmax:
        desired *= vmax / s

    old_v = np.array([sim["vx"], sim["vy"]])
    av = 1.0 - np.exp(-dt / VELOCITY_SMOOTH)
    new_v = old_v + av * (desired - old_v)
    s = np.linalg.norm(new_v)
    if s > vmax:
        new_v *= vmax / s

    new_pos = np.array([sim["x"], sim["y"]]) + new_v * dt
    new_pos = np.clip(new_pos, -DOMAIN + 0.35, DOMAIN - 0.35)

    raw_a = (new_v - old_v) / max(dt, 1e-9)
    old_a = np.array([sim["ax"], sim["ay"]])
    aa = 1.0 - np.exp(-dt / ACCEL_SMOOTH)
    new_a = old_a + aa * (raw_a - old_a)

    sim["x"], sim["y"] = new_pos
    sim["vx"], sim["vy"] = new_v
    sim["ax"], sim["ay"] = new_a
    sim["t"] += dt
    hist_push(sim["t"], sim["x"], sim["y"], sim["vx"], sim["vy"], sim["ax"], sim["ay"])

# -----------------------------------------------------------------------------
# Interfaz
# -----------------------------------------------------------------------------
def main() -> None:
    reset_simulation()

    BASE = 10.0
    SMALL = 9.0
    SECTION = 10.8
    TITLE = 18.5
    FORMULA = 13.5
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": BASE,
        "axes.titlesize": SECTION,
        "axes.labelsize": BASE,
        "xtick.labelsize": SMALL,
        "ytick.labelsize": SMALL,
        "legend.fontsize": SMALL,
        "mathtext.fontset": "dejavusans",
    })

    # Figura científica de dos columnas: el mapa ocupa toda la izquierda;
    # a la derecha el patrón polar tiene la jerarquía principal.
    fig = plt.figure(figsize=(14.4, 8.35), facecolor=PAPER)
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1.62, 1.0],
                  left=0.052, right=0.965, bottom=0.08, top=0.865, wspace=0.18)
    ax_field = fig.add_subplot(gs[0, 0])
    rg = gs[0, 1].subgridspec(5, 1, height_ratios=[0.86, 3.62, 0.72, 1.02, 0.86], hspace=0.28)
    ax_formula = fig.add_subplot(rg[0, 0])
    ax_polar = fig.add_subplot(rg[1, 0], projection="polar")
    ax_scale = fig.add_subplot(rg[2, 0])
    ax_controls = fig.add_subplot(rg[3, 0])
    ax_info = fig.add_subplot(rg[4, 0])

    for a in (ax_field, ax_formula, ax_polar, ax_scale, ax_controls, ax_info):
        a.set_facecolor(SURFACE)

    fig.suptitle("Campo retardado de una carga puntual en movimiento",
                 x=0.052, y=0.957, ha="left", fontsize=TITLE,
                 color=INK, fontweight="semibold")
    fig.text(0.053, 0.920,
             "Liénard–Wiechert · campo cercano 1/R² · radiación 1/R",
             color=MUTED, fontsize=BASE)

    logo_path = Path(__file__).with_name("UdeC_escudo.png")
    if not logo_path.exists():
        logo_path = Path(__file__).with_name("UdeC_azul_centrado.png")
    if logo_path.exists():
        try:
            logo = plt.imread(logo_path)
            ax_logo = fig.add_axes([0.910, 0.902, 0.044, 0.073])
            ax_logo.imshow(logo)
            ax_logo.axis("off")
        except Exception:
            pass

    # --- mapa de campo -----------------------------------------------------
    ax_field.set_xlim(-DOMAIN, DOMAIN)
    ax_field.set_ylim(-DOMAIN, DOMAIN)
    ax_field.set_aspect("equal")
    ax_field.grid(True, color=GRID, lw=0.55)
    ax_field.set_xlabel("x [u.l.]", color=INK)
    ax_field.set_ylabel("y [u.l.]", color=INK)
    ax_field.tick_params(colors=MUTED)
    for s in ax_field.spines.values():
        s.set_color(RULE)

    mode = {"key": "tot"}
    mode_labels = {"Total": "tot", "Velocidad 1/R²": "vel", "Radiación 1/R": "rad"}
    fields = calcular_campos(sim["t"])
    Ex, Ey = fields["tot"]
    disp, U, V, _ = field_display(Ex, Ey)

    im = ax_field.imshow(disp, origin="lower",
                         extent=(-DOMAIN, DOMAIN, -DOMAIN, DOMAIN),
                         cmap="viridis", norm=Normalize(0, 1),
                         interpolation="bilinear", alpha=0.94, zorder=1)
    quiver = ax_field.quiver(QX, QY, U[::QUIVER_STEP, ::QUIVER_STEP],
                             V[::QUIVER_STEP, ::QUIVER_STEP],
                             color=NAVY, alpha=0.72, scale_units="xy", scale=2.75,
                             width=0.0037, headwidth=3.1, headlength=4.0, zorder=3)
    cbar = fig.colorbar(im, ax=ax_field, orientation="horizontal",
                        fraction=0.043, pad=0.068, aspect=34)
    cbar.set_label("intensidad logarítmica relativa", color=MUTED)
    cbar.set_ticks([0, 0.5, 1.0])
    cbar.ax.tick_params(colors=MUTED)
    cbar.outline.set_edgecolor(RULE)

    charge, = ax_field.plot([0], [0], "o", ms=11.5, mfc=NAVY, mec="white", mew=1.5, zorder=7)
    target, = ax_field.plot([0], [0], marker="x", ms=10, mew=1.8, color=GOLD, zorder=6)
    trajectory, = ax_field.plot([], [], lw=1.4, color="#8693a2", alpha=0.75, zorder=2)
    ax_field.text(-DOMAIN + .16, DOMAIN - .26, "arrastra para mover el objetivo",
                  va="top", color=MUTED, fontsize=SMALL, zorder=9,
                  bbox=dict(fc="white", ec=RULE, boxstyle="square,pad=.35", alpha=.96))
    trail_x: list[float] = []
    trail_y: list[float] = []

    # --- encabezado del patrón angular ------------------------------------
    ax_formula.axis("off")
    ax_formula.text(0.0, 0.98, "Patrón angular instantáneo",
                    transform=ax_formula.transAxes, ha="left", va="top",
                    fontsize=SECTION, color=INK, fontweight="semibold")
    ax_formula.text(0.50, 0.49,
                    r"$\frac{dP}{d\Omega}\;\propto\;"
                    r"\frac{|\hat{\mathbf{n}}\times[(\hat{\mathbf{n}}-\boldsymbol{\beta})"
                    r"\times\dot{\boldsymbol{\beta}}]|^2}"
                    r"{(1-\hat{\mathbf{n}}\cdot\boldsymbol{\beta})^5}$",
                    transform=ax_formula.transAxes, ha="center", va="center",
                    fontsize=FORMULA, color=INK)
    ax_formula.text(0.0, 0.02, "corte en el plano xy · patrón normalizado al máximo instantáneo",
                    transform=ax_formula.transAxes, ha="left", va="bottom",
                    fontsize=SMALL, color=MUTED)

    # --- patrón polar ------------------------------------------------------
    ax_polar.set_theta_zero_location("E")
    ax_polar.set_theta_direction(1)
    ax_polar.set_thetagrids([0, 90, 180, 270], ["0°", "90°", "180°", "270°"])
    ax_polar.set_rlim(0, 1.04)
    ax_polar.set_rticks([0.5, 1.0])
    ax_polar.set_rlabel_position(35)
    ax_polar.tick_params(colors=MUTED, pad=3)
    ax_polar.grid(color=GRID, lw=.65)
    ax_polar.spines["polar"].set_color(RULE)
    th0 = np.linspace(0, 2*np.pi, 361)
    lobe_line, = ax_polar.plot(th0, np.zeros_like(th0), color=RADIATION, lw=2.35)
    acc_ray, = ax_polar.plot([0, 0], [0, 1], color=GOLD, lw=1.6, ls="--")
    vel_ray, = ax_polar.plot([0, 0], [0, .84], color=NAVY2, lw=1.45, ls=":")
    no_rad = ax_polar.text(.5, .49, "sin aceleración\nno hay radiación",
                           transform=ax_polar.transAxes, ha="center", va="center",
                           fontsize=SMALL, color=MUTED)
    ax_polar.text(.04, .96, r"$\mathbf{a}$", transform=ax_polar.transAxes,
                  color=GOLD, fontsize=SMALL, va="top")
    ax_polar.text(.04, .89, r"$\mathbf{v}$", transform=ax_polar.transAxes,
                  color=NAVY2, fontsize=SMALL, va="top")

    # --- escala relativa ---------------------------------------------------
    ax_scale.set_title("Peso relativo de los términos", loc="left", pad=4,
                       fontsize=SECTION, color=INK, fontweight="semibold")
    bars = ax_scale.barh(["velocidad", "radiación"], [0, 0], height=.44,
                         color=[NAVY2, RADIATION], alpha=.86)
    ax_scale.set_xlim(0, 1)
    ax_scale.set_xticks([0, .5, 1.0])
    ax_scale.grid(axis="x", color=GRID, lw=.55)
    ax_scale.tick_params(colors=MUTED)
    for s in ax_scale.spines.values():
        s.set_color(RULE)

    # --- controles ---------------------------------------------------------
    ax_controls.axis("off")
    cb = ax_controls.get_position()
    ax_radio = fig.add_axes([cb.x0, cb.y0 + .03*cb.height, .60*cb.width, .90*cb.height], facecolor=PAPER)
    radio = RadioButtons(ax_radio, tuple(mode_labels.keys()), active=0, activecolor=NAVY)
    for lab in radio.labels:
        lab.set_fontsize(SMALL); lab.set_color(INK)
    for s in ax_radio.spines.values():
        s.set_visible(False)

    bx = cb.x0 + .67*cb.width
    bw = .29*cb.width
    bh = .31*cb.height
    ax_pause = fig.add_axes([bx, cb.y0 + .56*cb.height, bw, bh])
    ax_reset = fig.add_axes([bx, cb.y0 + .14*cb.height, bw, bh])
    btn_pause = Button(ax_pause, "Pausar", color="white", hovercolor="#eef2f6")
    btn_reset = Button(ax_reset, "Reiniciar", color="white", hovercolor="#eef2f6")
    for b in (btn_pause, btn_reset):
        b.label.set_color(INK); b.label.set_fontsize(SMALL)
        for s in b.ax.spines.values(): s.set_color(RULE)

    # --- estado ------------------------------------------------------------
    ax_info.axis("off")
    ax_info.text(0, 1.0, "Estado instantáneo", va="top", transform=ax_info.transAxes,
                 fontsize=SECTION, color=INK, fontweight="semibold")
    info_text = ax_info.text(0, .72, "", va="top", transform=ax_info.transAxes,
                             fontsize=SMALL, color="#405066", linespacing=1.45)

    # Estado de actualización
    last = dict(wall=perf_counter(), field=-1e9, polar=-1e9, status=-1e9, render=-1e9)
    cache = {"fields": fields, "bg": {}, "blit_ready": False}

    def update_trail():
        trail_x.append(sim["x"]); trail_y.append(sim["y"])
        if len(trail_x) > 220:
            del trail_x[:-220]; del trail_y[:-220]
        trajectory.set_data(trail_x, trail_y)

    def selected(f):
        return f[mode["key"]]

    def update_field():
        f = calcular_campos(sim["t"])
        cache["fields"] = f
        Exs, Eys = selected(f)
        dmap, uu, vv, _ = field_display(Exs, Eys)
        im.set_data(dmap)
        quiver.set_UVC(uu[::QUIVER_STEP, ::QUIVER_STEP], vv[::QUIVER_STEP, ::QUIVER_STEP])

        Ev = np.hypot(*f["vel"])
        Er = np.hypot(*f["rad"])
        mvel = float(np.max(Ev)); mrad = float(np.max(Er))
        den = max(mvel, mrad, 1e-12)
        bars[0].set_width(mvel / den)
        bars[1].set_width(mrad / den)

    def update_polar():
        ang, p, pn = patron_radiacion_angular(361)
        lobe_line.set_data(ang, pn)
        am = np.hypot(sim["ax"], sim["ay"])
        vm = np.hypot(sim["vx"], sim["vy"])
        aa = np.arctan2(sim["ay"], sim["ax"]) if am > 1e-12 else 0.0
        va = np.arctan2(sim["vy"], sim["vx"]) if vm > 1e-12 else 0.0
        acc_ray.set_data([aa, aa], [0, 1 if am > 1e-12 else 0])
        vel_ray.set_data([va, va], [0, .84 if vm > 1e-12 else 0])
        no_rad.set_visible(float(np.max(pn)) < 1e-10)

    def update_status():
        v = np.hypot(sim["vx"], sim["vy"])
        a = np.hypot(sim["ax"], sim["ay"])
        info_text.set_text(
            rf"$\beta={v/C:.3f}$    $|v|={v:.2f}$    $|a|={a:.2f}$" "\n"
            rf"$r=({sim['x']:+.2f},{sim['y']:+.2f})$    $t={sim['t']:.2f}\,s$"
        )

    # ------------------------------------------------------------------
    # Renderizado por capas
    # ------------------------------------------------------------------
    # En el panel principal el mapa/quiver cambian a ~9 Hz, mientras que la
    # carga y su trayectoria pueden moverse a ~30 Hz. Si se redibujara el
    # mapa completo para cada desplazamiento del marcador, Matplotlib se vuelve
    # innecesariamente pesado. Por eso se conservan dos fondos: uno sin el
    # campo y otro que ya contiene el campo más reciente.
    field_layer = [im, quiver]
    charge_layer = [charge, target, trajectory]
    polar_layer = [lobe_line, acc_ray, vel_ray, no_rad]
    scale_layer = list(bars)
    info_layer = [info_text]
    dynamic_all = field_layer + charge_layer + polar_layer + scale_layer + info_layer
    for art in dynamic_all:
        art.set_animated(True)

    cache.update(base={}, field_bg=None, blit_ready=False)

    def cache_base_backgrounds():
        cache["base"] = {
            ax_field: fig.canvas.copy_from_bbox(ax_field.bbox),
            ax_polar: fig.canvas.copy_from_bbox(ax_polar.bbox),
            ax_scale: fig.canvas.copy_from_bbox(ax_scale.bbox),
            ax_info: fig.canvas.copy_from_bbox(ax_info.bbox),
        }
        cache["blit_ready"] = True
        # Construye el fondo del panel izquierdo incluyendo el campo actual,
        # pero todavía sin la carga/objetivo/trayectoria.
        fig.canvas.restore_region(cache["base"][ax_field])
        for art in field_layer:
            ax_field.draw_artist(art)
        cache["field_bg"] = fig.canvas.copy_from_bbox(ax_field.bbox)

    def render_field_and_charge():
        if not cache["blit_ready"] or not getattr(fig.canvas, "supports_blit", False):
            fig.canvas.draw_idle(); return
        fig.canvas.restore_region(cache["base"][ax_field])
        for art in field_layer:
            ax_field.draw_artist(art)
        cache["field_bg"] = fig.canvas.copy_from_bbox(ax_field.bbox)
        for art in charge_layer:
            ax_field.draw_artist(art)
        fig.canvas.blit(ax_field.bbox)

    def render_charge_only():
        if not cache["blit_ready"] or cache["field_bg"] is None or not getattr(fig.canvas, "supports_blit", False):
            fig.canvas.draw_idle(); return
        fig.canvas.restore_region(cache["field_bg"])
        for art in charge_layer:
            ax_field.draw_artist(art)
        fig.canvas.blit(ax_field.bbox)

    def render_simple(ax_obj, artists):
        if not cache["blit_ready"] or not getattr(fig.canvas, "supports_blit", False):
            fig.canvas.draw_idle(); return
        fig.canvas.restore_region(cache["base"][ax_obj])
        for art in artists:
            ax_obj.draw_artist(art)
        fig.canvas.blit(ax_obj.bbox)

    def full_redraw():
        cache["blit_ready"] = False
        fig.canvas.draw()
        cache_base_backgrounds()
        render_field_and_charge()
        render_simple(ax_polar, polar_layer)
        render_simple(ax_scale, scale_layer)
        render_simple(ax_info, info_layer)
        fig.canvas.flush_events()

    def tick():
        now = perf_counter()
        elapsed = min(now - last["wall"], 0.06)
        last["wall"] = now

        if not sim["paused"]:
            nstep = max(1, min(3, int(np.ceil(elapsed / DT))))
            for _ in range(nstep):
                advance_charge(DT)
            update_trail()

        charge.set_data([sim["x"]], [sim["y"]])
        target.set_data([sim["target_x"]], [sim["target_y"]])

        field_changed = False
        polar_changed = False
        scale_changed = False
        info_changed = False

        if now - last["field"] >= FIELD_PERIOD:
            update_field(); last["field"] = now
            field_changed = True; scale_changed = True
        if now - last["polar"] >= POLAR_PERIOD:
            update_polar(); last["polar"] = now
            polar_changed = True
        if now - last["status"] >= STATUS_PERIOD:
            update_status(); last["status"] = now
            info_changed = True

        if now - last["render"] >= RENDER_PERIOD:
            # Si el campo no cambió, solo se repintan tres artistas livianos.
            if field_changed:
                render_field_and_charge()
            else:
                render_charge_only()
            if polar_changed:
                render_simple(ax_polar, polar_layer)
            if scale_changed:
                render_simple(ax_scale, scale_layer)
            if info_changed:
                render_simple(ax_info, info_layer)
            fig.canvas.flush_events()
            last["render"] = now
        return True

    timer = fig.canvas.new_timer(interval=TIMER_MS)
    timer.add_callback(tick)

    def set_target(event):
        if event.inaxes is ax_field and event.xdata is not None and event.ydata is not None:
            sim["target_x"] = float(np.clip(event.xdata, -DOMAIN + .35, DOMAIN - .35))
            sim["target_y"] = float(np.clip(event.ydata, -DOMAIN + .35, DOMAIN - .35))

    def on_press(event):
        if event.inaxes is ax_field and event.button == 1:
            sim["drag"] = True; set_target(event)

    def on_motion(event):
        if sim["drag"]: set_target(event)

    def on_release(_event):
        sim["drag"] = False

    def on_radio(label):
        mode["key"] = mode_labels[label]
        update_field()
        render_field_and_charge()
        render_simple(ax_scale, scale_layer)

    def on_pause(_event):
        sim["paused"] = not sim["paused"]
        btn_pause.label.set_text("Continuar" if sim["paused"] else "Pausar")
        full_redraw()

    def on_reset(_event):
        reset_simulation(); trail_x.clear(); trail_y.clear()
        mode["key"] = "tot"
        radio.set_active(0)
        update_field(); update_polar(); update_status()
        full_redraw()

    def on_draw(_event):
        # Un resize o una actualización completa invalida los fondos de blit.
        # El evento ya ocurre después del draw estático, por lo que basta copiar.
        if not cache.get("_caching", False):
            cache["_caching"] = True
            try:
                cache_base_backgrounds()
            finally:
                cache["_caching"] = False

    fig.canvas.mpl_connect("button_press_event", on_press)
    fig.canvas.mpl_connect("motion_notify_event", on_motion)
    fig.canvas.mpl_connect("button_release_event", on_release)
    fig.canvas.mpl_connect("draw_event", on_draw)
    radio.on_clicked(on_radio)
    btn_pause.on_clicked(on_pause)
    btn_reset.on_clicked(on_reset)

    update_field(); update_polar(); update_status()
    full_redraw()

    backend = str(matplotlib.get_backend()).lower()
    interactive = any(s in backend for s in (
        "tkagg", "qtagg", "qt5agg", "wxagg", "gtk3agg", "gtk4agg",
        "macosx", "nbagg", "webagg", "widget"
    ))
    print(f"Matplotlib backend: {matplotlib.get_backend()}")

    if not interactive:
        # Preview con movimiento no trivial.
        sim["target_x"], sim["target_y"] = 2.0, 1.25
        for _ in range(24):
            advance_charge(DT)
        update_trail(); update_field(); update_polar(); update_status()
        # Para savefig los artistas animados deben volver a participar del draw.
        for art in dynamic_all:
            art.set_animated(False)
        fig.canvas.draw()
        preview = Path(__file__).with_name("tarea4_preview.png")
        fig.savefig(preview, dpi=190, bbox_inches="tight", facecolor=PAPER)
        print(f"Backend no interactivo: preview guardado en {preview}")
        plt.close(fig)
        return

    timer.start()
    plt.show(block=True)


if __name__ == "__main__":
    main()
