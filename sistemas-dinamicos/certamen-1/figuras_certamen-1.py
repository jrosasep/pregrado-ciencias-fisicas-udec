#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

warnings.filterwarnings("ignore", category=RuntimeWarning)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.titlesize": 9.5,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 7.5,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "axes.unicode_minus": False,
    "svg.fonttype": "path",
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "grid.color": "0.86",
    "grid.linewidth": 0.45,
    "grid.linestyle": "--",
})

AZUL = "#1f5a85"
ROJO = "#8f2d2d"
VERDE = "#3f7f4f"
MORADO = "#6b4c9a"
NARANJO = "#b66a2c"
GRIS = "0.45"
GRIS_CLARO = "0.92"
NEGRO = "0.10"


def guardar(fig, nombre, carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=0.55)
    fig.savefig(carpeta / f"{nombre}.svg", format="svg", bbox_inches="tight")
    plt.close(fig)


def formato(ax, xlabel, ylabel, grid=True):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if grid:
        ax.grid(True)


def cobweb(ax, f, x0, n, color):
    x = x0
    xs, ys = [x], [0.0]
    for _ in range(n):
        fx = f(x)
        xs.extend([x, fx])
        ys.extend([fx, fx])
        x = fx
        if not np.isfinite(x) or abs(x) > 1e6:
            break
    ax.plot(xs, ys, color=color, lw=0.8, alpha=0.70)


def g1(x, mu=61 / 20):
    return mu * x * (1 - x)


def f3(x):
    return x**3 + x


def f4(x):
    return 2 * x**2 - 5 * x


def g2(x, y):
    return x**2 - 5 * x + y, x**2


def F6(x, y, a, b):
    return y, -b * x + a * y - y**3


def jac6(y, a, b):
    return np.array([[0.0, 1.0], [-b, a - 3 * y**2]])


# Genera p1_cobweb.svg
def figura_p1_cobweb(carpeta):
    mu = 61 / 20
    x = np.linspace(0, 1, 900)
    xf1, xf2 = 0.0, 41 / 61
    p1, p2 = 45 / 61, 36 / 61

    fig, ax = plt.subplots(figsize=(4.8, 3.9))
    ax.plot(x, g1(x, mu), color=NEGRO, lw=1.45, label=r"$g(x)$")
    ax.plot(x, x, color=GRIS, lw=0.9, ls="--", label=r"$y=x$")

    for x0, color in [(0.14, NARANJO), (0.42, VERDE), (0.86, MORADO)]:
        cobweb(ax, lambda z: g1(z, mu), x0, 38, color)

    ax.scatter([xf1, xf2], [xf1, xf2], s=32, color=ROJO, zorder=3, label="puntos fijos")
    ax.scatter([p1, p2], [p1, p2], s=34, marker="s", color=AZUL, zorder=3, label="período 2")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(r"Mapa logístico $g(x)=3{,}05x(1-x)$")
    formato(ax, r"$x$", r"$g(x)$")
    ax.legend(loc="lower right", frameon=True, fancybox=False, framealpha=1.0)
    guardar(fig, "p1_cobweb", carpeta)


# Genera p1_orbita.svg
def figura_p1_orbita(carpeta):
    mu = 61 / 20
    p1, p2 = 45 / 61, 36 / 61
    n = 80
    xs = np.empty(n)
    xs[0] = 0.2
    for k in range(n - 1):
        xs[k + 1] = g1(xs[k], mu)

    fig, ax = plt.subplots(figsize=(5.3, 2.8))
    ax.plot(np.arange(n), xs, color=NEGRO, lw=0.85, marker="o", ms=2.0, mfc="white", mew=0.7)
    ax.axhline(p1, color=AZUL, lw=0.9, ls="--", label=r"$p_1=45/61$")
    ax.axhline(p2, color=AZUL, lw=0.9, ls=":", label=r"$p_2=36/61$")
    ax.set_title(r"Convergencia hacia la órbita de período $2$")
    formato(ax, r"iteración $n$", r"$x_n$")
    ax.legend(frameon=True, fancybox=False, framealpha=1.0)
    guardar(fig, "p1_orbita", carpeta)


# Genera p2_retrato.svg
def figura_p2_retrato(carpeta):
    fig, ax = plt.subplots(figsize=(4.8, 3.9))
    iniciales = [(0.10, 0.02), (0.35, 0.05), (-0.35, 0.20), (2.75, 8.20), (3.12, 9.20)]
    colores = [NARANJO, VERDE, MORADO, AZUL, ROJO]

    for (x0, y0), color in zip(iniciales, colores):
        xs, ys = [x0], [y0]
        for _ in range(22):
            xn, yn = g2(xs[-1], ys[-1])
            if max(abs(xn), abs(yn)) > 70:
                break
            xs.append(xn)
            ys.append(yn)
        ax.plot(xs, ys, color=color, lw=0.75, marker="o", ms=2.2, alpha=0.80)
        ax.scatter([x0], [y0], marker="s", s=18, color=color, zorder=3)

    ax.scatter([0], [0], marker="*", s=115, color=ROJO, label=r"$(0,0)$ saddle", zorder=4)
    ax.scatter([3], [9], marker="*", s=115, color=NEGRO, label=r"$(3,9)$ source", zorder=4)
    ax.annotate(r"$(0,0)$", xy=(0, 0), xytext=(0.35, 0.90), color=ROJO,
                arrowprops=dict(arrowstyle="->", lw=0.7, color=ROJO))
    ax.annotate(r"$(3,9)$", xy=(3, 9), xytext=(3.25, 10.0), color=NEGRO,
                arrowprops=dict(arrowstyle="->", lw=0.7, color=NEGRO))
    ax.set_xlim(-1.1, 4.3)
    ax.set_ylim(-0.7, 12.0)
    ax.set_title(r"Iteraciones del mapa $g(x,y)$")
    formato(ax, r"$x$", r"$y$")
    ax.legend(frameon=True, fancybox=False, framealpha=1.0)
    guardar(fig, "p2_retrato", carpeta)


# Genera p3_cobweb.svg
def figura_p3_cobweb(carpeta):
    x = np.linspace(-1.1, 1.1, 900)
    fig, ax = plt.subplots(figsize=(4.6, 3.9))
    ax.plot(x, f3(x), color=NEGRO, lw=1.45, label=r"$f(x)=x^3+x$")
    ax.plot(x, x, color=GRIS, lw=0.9, ls="--", label=r"$y=x$")

    for x0, color in [(0.18, NARANJO), (0.33, ROJO), (-0.18, VERDE), (-0.33, MORADO)]:
        cobweb(ax, f3, x0, 7, color)

    ax.scatter([0], [0], s=36, color=ROJO, zorder=3, label=r"$x^*=0$")
    ax.set_xlim(-1.08, 1.08)
    ax.set_ylim(-1.50, 1.50)
    ax.set_title(r"Diagrama cobweb para $f(x)=x^3+x$")
    formato(ax, r"$x$", r"$f(x)$")
    ax.legend(loc="upper left", frameon=True, fancybox=False, framealpha=1.0)
    guardar(fig, "p3_cobweb", carpeta)


# Genera p3_diferencia.svg
def figura_p3_diferencia(carpeta):
    x = np.linspace(-1.12, 1.12, 900)
    y = x**3
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    ax.plot(x, y, color=NEGRO, lw=1.35, label=r"$f(x)-x=x^3$")
    ax.fill_between(x[x >= 0], 0, y[x >= 0], color=ROJO, alpha=0.13)
    ax.fill_between(x[x <= 0], 0, y[x <= 0], color=AZUL, alpha=0.13)
    ax.axhline(0, color=GRIS, lw=0.8, ls="--")
    ax.axvline(0, color=GRIS, lw=0.8, ls="--")
    ax.text(0.52, 0.22, r"$f(x)>x$", color=ROJO, ha="center")
    ax.text(-0.52, -0.22, r"$f(x)<x$", color=AZUL, ha="center")
    ax.set_title(r"Signo de $f(x)-x$")
    formato(ax, r"$x$", r"$f(x)-x$")
    ax.legend(frameon=True, fancybox=False, framealpha=1.0)
    guardar(fig, "p3_diferencia", carpeta)


# Genera p4_periodo2.svg
def figura_p4_periodo2(carpeta):
    p1, p2 = 1 + np.sqrt(2), 1 - np.sqrt(2)
    x = np.linspace(-0.85, 3.75, 1000)
    fig, ax = plt.subplots(figsize=(4.9, 3.8))
    ax.plot(x, f4(x), color=NEGRO, lw=1.45, label=r"$f(x)=2x^2-5x$")
    ax.plot(x, x, color=GRIS, lw=0.9, ls="--", label=r"$y=x$")

    for x0, color in [(p1 + 0.02, NARANJO), (p1 - 0.02, ROJO), (p2 + 0.02, VERDE), (p2 - 0.02, MORADO)]:
        cobweb(ax, f4, x0, 8, color)

    ax.scatter([0, 3], [0, 3], color=AZUL, s=32, label="puntos fijos", zorder=3)
    ax.scatter([p1, p2], [p1, p2], color=ROJO, marker="s", s=36, label="período 2", zorder=3)
    ax.set_xlim(-0.85, 3.75)
    ax.set_ylim(-3.0, 4.8)
    ax.set_title(r"Órbita de período $2$ de $f(x)=2x^2-5x$")
    formato(ax, r"$x$", r"$f(x)$")
    ax.legend(frameon=True, fancybox=False, framealpha=1.0)
    guardar(fig, "p4_periodo2", carpeta)


def segmentos_cantor(etapa):
    segmentos = [(0.0, 1.0)]
    for _ in range(etapa):
        nuevos = []
        for a, b in segmentos:
            L = b - a
            nuevos += [(a, a + L / 5), (a + 2 * L / 5, a + 3 * L / 5), (a + 4 * L / 5, b)]
        segmentos = nuevos
    return segmentos


# Genera p5_cantor.svg
def figura_p5_cantor(carpeta):
    etapas = 5
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    h = 0.24

    for n in range(etapas):
        y = etapas - 1 - n
        ax.add_patch(patches.Rectangle((0, y - h / 2), 1, h, fc=GRIS_CLARO, ec="none"))
        for a, b in segmentos_cantor(n):
            ax.add_patch(patches.Rectangle((a, y - h / 2), b - a, h, fc=NEGRO, ec="none"))
        ax.text(-0.035, y, rf"$n={n}$", ha="right", va="center")
        ax.text(1.025, y, rf"$3^{n}$ intervalos, longitud $5^{{-{n}}}$", ha="left", va="center", fontsize=8)

    for xpos, label in [(0, "$0$"), (1/5, "$1/5$"), (2/5, "$2/5$"), (3/5, "$3/5$"), (4/5, "$4/5$"), (1, "$1$")]:
        ax.plot([xpos, xpos], [-0.30, -0.15], color=GRIS, lw=0.7)
        ax.text(xpos, -0.40, label, ha="center", va="top", fontsize=8)

    ax.set_title(r"Construcción de la variante del conjunto de Cantor")
    ax.set_xlim(-0.12, 1.34)
    ax.set_ylim(-0.62, etapas - 0.35)
    ax.axis("off")
    guardar(fig, "p5_cantor", carpeta)


# Genera p6_estabilidad_a2.svg
def figura_p6_estabilidad_a2(carpeta):
    a, b = 2.0, 0.15
    s = np.sqrt(a - b - 1)
    puntos = [(0.0, ROJO, r"$P_0$"), (s, VERDE, r"$P_+$"), (-s, AZUL, r"$P_-$")]

    fig, ax = plt.subplots(figsize=(4.2, 3.7))
    t = np.linspace(0, 2 * np.pi, 500)
    ax.plot(np.cos(t), np.sin(t), color=GRIS, ls="--", lw=0.8, label="círculo unitario")
    for y0, color, label in puntos:
        vals = np.linalg.eigvals(jac6(y0, a, b))
        ax.scatter(vals.real, vals.imag, s=36, color=color, label=label, zorder=3)

    ax.axhline(0, color=GRIS, lw=0.75)
    ax.axvline(0, color=GRIS, lw=0.75)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-2.0, 2.25)
    ax.set_ylim(-1.35, 1.35)
    ax.set_title(r"Valores propios para $a=2{,}0$, $b=0{,}15$")
    formato(ax, r"$\operatorname{Re}(\lambda)$", r"$\operatorname{Im}(\lambda)$")
    ax.legend(loc="lower right", frameon=True, fancybox=False, framealpha=1.0)
    guardar(fig, "p6_estabilidad_a2", carpeta)


def datos_bifurcacion(b=0.15, n_a=360, n_trans=1000, n_keep=45):
    lista_a, lista_x = [], []
    x, y = 0.1, 0.1
    for a in np.linspace(1.5, 2.8, n_a):
        for _ in range(n_trans):
            x, y = F6(x, y, a, b)
            if not np.isfinite(x + y) or max(abs(x), abs(y)) > 1e6:
                x, y = 0.1, 0.1
        for _ in range(n_keep):
            x, y = F6(x, y, a, b)
            if not np.isfinite(x + y) or max(abs(x), abs(y)) > 1e6:
                x, y = 0.1, 0.1
                continue
            lista_a.append(a)
            lista_x.append(x)
    return np.asarray(lista_a), np.asarray(lista_x)


# Genera p6_bifurcacion.svg
def figura_p6_bifurcacion(carpeta):
    b = 0.15
    aa, xx = datos_bifurcacion(b=b)
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.scatter(aa, xx, s=0.28, color=NEGRO, alpha=0.30, linewidths=0, rasterized=True)

    a_rama = np.linspace(1.5, 2.30, 400)
    rama = np.sqrt(a_rama - 1 - b)
    ax.plot(a_rama, rama, color=ROJO, lw=0.95, label="ramas fijas estables")
    ax.plot(a_rama, -rama, color=ROJO, lw=0.95)
    ax.axvline(2.30, color=AZUL, lw=0.85, ls="--", label=r"$a=2{,}30$")
    ax.set_xlim(1.5, 2.8)
    ax.set_ylim(-1.75, 1.75)
    ax.set_title(r"Diagrama de bifurcación para $b=0{,}15$")
    formato(ax, r"parámetro $a$", r"valores asintóticos de $x_n$")
    ax.legend(loc="upper left", frameon=True, fancybox=False, framealpha=1.0)
    guardar(fig, "p6_bifurcacion", carpeta)


def datos_atractor(a=2.75, b=0.15, n_trans=3000, n_keep=10000):
    x, y = 0.1, 0.1
    for _ in range(n_trans):
        x, y = F6(x, y, a, b)
    xs, ys = np.empty(n_keep), np.empty(n_keep)
    for k in range(n_keep):
        x, y = F6(x, y, a, b)
        xs[k], ys[k] = x, y
    return xs, ys


# Genera p6_atractor.svg
def figura_p6_atractor(carpeta):
    xs, ys = datos_atractor()
    fig, ax = plt.subplots(figsize=(4.2, 3.8))
    ax.scatter(xs, ys, s=0.35, color=NEGRO, alpha=0.32, linewidths=0, rasterized=True)
    ax.set_title(r"Atractor para $a=2{,}75$, $b=0{,}15$")
    formato(ax, r"$x_n$", r"$y_n$")
    ax.set_aspect("equal", adjustable="box")
    guardar(fig, "p6_atractor", carpeta)


# Genera p6_serie_temporal.svg
def figura_p6_serie_temporal(carpeta):
    a, b = 2.75, 0.15
    x, y = 0.1, 0.1
    for _ in range(1000):
        x, y = F6(x, y, a, b)

    n = 240
    xs = np.empty(n)
    for k in range(n):
        x, y = F6(x, y, a, b)
        xs[k] = x

    fig, ax = plt.subplots(figsize=(5.8, 2.7))
    ax.plot(np.arange(n), xs, color=NEGRO, lw=0.75)
    ax.set_title(r"Serie temporal de $x_n$ para $a=2{,}75$, $b=0{,}15$")
    formato(ax, r"iteración $n$", r"$x_n$")
    guardar(fig, "p6_serie_temporal", carpeta)


def generar_todo(carpeta):
    for funcion in [
        figura_p1_cobweb,
        figura_p1_orbita,
        figura_p2_retrato,
        figura_p3_cobweb,
        figura_p3_diferencia,
        figura_p4_periodo2,
        figura_p5_cantor,
        figura_p6_estabilidad_a2,
        figura_p6_bifurcacion,
        figura_p6_atractor,
        figura_p6_serie_temporal,
    ]:
        funcion(carpeta)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="figuras")
    args = parser.parse_args()
    carpeta = Path(args.out)
    generar_todo(carpeta)
    print(f"Figuras SVG generadas en {carpeta.resolve()}")


if __name__ == "__main__":
    main()
