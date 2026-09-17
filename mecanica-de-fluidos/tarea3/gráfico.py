#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tarea 3 - Mecánica de Fluidos
Problema 3: figura comparativa usada en la entrega.

El programa genera tres paneles:
1. Velocidad compleja.
2. Parte real - i*Parte imaginaria.
3. Separación de variables.

La geometría y los colores reproducen la figura original de la tarea:
- líneas de corriente: morado oscuro;
- fuente: rojo;
- fronteras: negro.

Salidas:
    Grafico.pdf
    Grafico.png
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Parámetros de la configuración graficada
# ---------------------------------------------------------------------------

alpha = np.pi / 2
a = 1.0
r0 = 2.0
theta0 = np.pi / 6
m = 1.0

N = 70

xmin, xmax = 0.0, 3.0
ymin, ymax = -3.0, 3.0
nx, ny = 420, 520

purple = "#440154"
source_red = "#ff0000"
wall_black = "#000000"


def domain_mask(x, y):
    r = np.hypot(x, y)
    theta = np.arctan2(y, x)
    return (r > a) & (np.abs(theta) < alpha / 2)


# ---------------------------------------------------------------------------
# Separación de variables
# ---------------------------------------------------------------------------

def velocity_separation(r, theta, n_modes=N):
    r = np.asarray(r, dtype=float)
    theta = np.asarray(theta, dtype=float)

    ur = (m / (alpha * r)) * (r > r0)
    uth = np.zeros_like(r)

    r_less = np.minimum(r, r0)
    r_greater = np.maximum(r, r0)

    eta = theta + alpha / 2
    eta0 = theta0 + alpha / 2

    for n in range(1, n_modes + 1):
        k = n * np.pi / alpha

        angular = np.cos(k * eta0) * np.cos(k * eta)
        radial = (r_less / r_greater) ** k + (a * a / (r * r0)) ** k

        d_radial = np.empty_like(r)
        inside = r < r0
        d_radial[inside] = (
            -(r[inside] / r0) ** k
            + (a * a / (r[inside] * r0)) ** k
        )
        d_radial[~inside] = (
            (r0 / r[~inside]) ** k
            + (a * a / (r[~inside] * r0)) ** k
        )

        ur += (m / (alpha * r)) * angular * d_radial

        uth += (
            (m / (alpha * r))
            * np.cos(k * eta0)
            * np.sin(k * eta)
            * radial
        )

    return ur, uth


# ---------------------------------------------------------------------------
# Potencial complejo
# ---------------------------------------------------------------------------

def complex_velocity(z):
    """
    Devuelve dw/dz = u_x - i u_y.
    """
    beta = np.pi / alpha

    eta = np.exp(1j * alpha / 2) * z
    zeta = eta ** beta

    z0 = r0 * np.exp(1j * theta0)
    eta0 = np.exp(1j * alpha / 2) * z0
    zeta0 = eta0 ** beta

    b = a ** beta
    image = b * b / np.conjugate(zeta0)

    term = (
        1.0 / (zeta - zeta0)
        + 1.0 / (zeta - np.conjugate(zeta0))
        + 1.0 / (zeta - image)
        + 1.0 / (zeta - np.conjugate(image))
        - 2.0 / zeta
    )

    return (m / (2.0 * alpha)) * (zeta / z) * term


def polar_from_complex(z):
    theta = np.angle(z)
    q = np.exp(1j * theta) * complex_velocity(z)
    ur = np.real(q)
    uth = -np.imag(q)
    return ur, uth


def to_cartesian(ur, uth, theta):
    ux = ur * np.cos(theta) - uth * np.sin(theta)
    uy = ur * np.sin(theta) + uth * np.cos(theta)
    return ux, uy


def build_fields():
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    X, Y = np.meshgrid(x, y)

    R = np.hypot(X, Y)
    TH = np.arctan2(Y, X)
    Z = X + 1j * Y

    mask = domain_mask(X, Y)

    # Valores auxiliares seguros fuera del dominio.
    R_eval = np.where(mask, R, a + 1e-3)
    TH_eval = np.where(mask, TH, 0.0)
    Z_eval = np.where(mask, Z, (a + 1e-3) + 0j)

    x0 = r0 * np.cos(theta0)
    y0 = r0 * np.sin(theta0)
    mask &= np.hypot(X - x0, Y - y0) > 0.075

    # Método complejo
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        ur_c, uth_c = polar_from_complex(Z_eval)
    ux_c, uy_c = to_cartesian(ur_c, uth_c, TH_eval)

    # Mismo campo reconstruido explícitamente desde Re(dw/dz), -Im(dw/dz)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        q = complex_velocity(Z_eval)
    ux_ri = np.real(q)
    uy_ri = -np.imag(q)

    # Separación de variables
    ur_s, uth_s = velocity_separation(R_eval, TH_eval)
    ux_s, uy_s = to_cartesian(ur_s, uth_s, TH_eval)

    for arr in (ux_c, uy_c, ux_ri, uy_ri, ux_s, uy_s):
        arr[~mask] = np.nan
        arr[~np.isfinite(arr)] = np.nan

    return x, y, ux_c, uy_c, ux_ri, uy_ri, ux_s, uy_s


def draw_geometry(ax):
    # Rectas theta = +/- alpha/2
    rr = np.linspace(0.0, 4.0, 300)
    for sgn in (-1, 1):
        th = sgn * alpha / 2
        ax.plot(
            rr * np.cos(th),
            rr * np.sin(th),
            color=wall_black,
            linewidth=2.0,
            zorder=4,
        )

    # Pared circular r=a
    th = np.linspace(-alpha / 2, alpha / 2, 300)
    ax.plot(
        a * np.cos(th),
        a * np.sin(th),
        color=wall_black,
        linewidth=2.0,
        zorder=4,
    )

    x0 = r0 * np.cos(theta0)
    y0 = r0 * np.sin(theta0)
    ax.scatter(
        [x0],
        [y0],
        color=source_red,
        s=30,
        label="Fuente",
        zorder=7,
    )

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("auto")
    ax.set_xlabel("x")
    ax.grid(True, color="0.65", linewidth=0.7, alpha=0.75)
    ax.legend(loc="upper left", frameon=True)


def main():
    x, y, ux_c, uy_c, ux_ri, uy_ri, ux_s, uy_s = build_fields()

    fig, axes = plt.subplots(1, 3, figsize=(13.7, 5.5), sharey=True)

    panels = [
        ("Velocidad compleja", ux_c, uy_c),
        ("Parte real - i*Parte imaginaria", ux_ri, uy_ri),
        ("Separación de variables", ux_s, uy_s),
    ]

    for ax, (title, ux, uy) in zip(axes, panels):
        ax.streamplot(
            x,
            y,
            ux,
            uy,
            color=plt.cm.viridis(0.0),
            density=1.35,
            linewidth=0.80,
            arrowsize=1.0,
            minlength=0.08,
            maxlength=5.0,
            integration_direction="both",
        )
        draw_geometry(ax)
        ax.set_title(title)

    axes[0].set_ylabel("y")
    for ax in axes[1:]:
        ax.tick_params(labelleft=False)


    out = Path(__file__).resolve().parent
    fig.savefig(out / "Grafico.pdf")
    fig.savefig(out / "Grafico.png", dpi=220)
    plt.close(fig)

    print(out / "Grafico.pdf")
    print(out / "Grafico.png")


if __name__ == "__main__":
    main()
