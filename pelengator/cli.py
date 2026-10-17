"""Buyruq qatori: simulyatsiya qilingan signal bo'yicha pelengni ko'rsatish."""

from __future__ import annotations

import argparse

import math

from .array import C, uniform_circular_array
from .doa import estimate_doa
from .simulate import simulate_snapshots


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="pelengator", description=__doc__)
    p.add_argument("--freq", type=float, default=433e6, help="chastota, Hz")
    p.add_argument("--elements", type=int, default=5, help="antennalar soni")
    p.add_argument("--azimuth", type=float, nargs="+", default=[42.0], help="manba azimutlari (simulyatsiya)")
    p.add_argument("--snr", type=float, default=15.0)
    p.add_argument("--method", choices=["music", "bartlett"], default="music")
    args = p.parse_args(argv)

    # qo'shni antennalar orasi ~ yarim to'lqin
    radius = 0.5 * (C / args.freq) / (2 * math.sin(math.pi / args.elements))
    array = uniform_circular_array(args.elements, radius)
    x = simulate_snapshots(array, args.freq, args.azimuth, snr_db=args.snr, seed=0)
    est = estimate_doa(x, array, args.freq, len(args.azimuth), args.method)
    print("Haqiqiy azimut:", args.azimuth)
    print("Baholangan azimut:", [f"{a:.1f}°" for a in est])


if __name__ == "__main__":
    main()
