#!/usr/bin/env python3
"""Mesure la masse visuelle des logos et génère les scales CSS optiques."""
import json
import os
import subprocess
import tempfile

OUT = os.path.join(os.path.dirname(__file__), "assets", "logos")
TARGET_AREA = 4200  # px² de référence (Deloitte ~baseline)

LOGOS = [
    "logo-ref-deloitte.svg",
    "logo-ref-accor.svg",
    "logo-ref-ses.svg",
    "logo-ref-courducale.svg",
    "logo-ref-bnl.svg",
    "logo-ref-maisonheler.svg",
    "logo-ref-sodikart.svg",
    "logo-ref-mchat.svg",
]


def ink_area(path):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(
            ["magick", "-background", "none", path, "-resize", "400x120",
             "-alpha", "extract", "-threshold", "8%", "-format", "%@", "info:"],
            capture_output=True, text=True, check=True,
        )
        # bbox from alpha
        r = subprocess.run(
            ["magick", "-background", "none", path, "-resize", "400x120",
             "-alpha", "extract", "-threshold", "8%", "-trim", "+repage",
             "-format", "%w %h", "info:"],
            capture_output=True, text=True, check=True,
        )
        w, h = map(int, r.stdout.strip().split())
        return max(w * h, 1)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def main():
    scales = {}
    for name in LOGOS:
        path = os.path.join(OUT, name)
        if not os.path.exists(path):
            print("skip", name)
            continue
        area = ink_area(path)
        scale = (TARGET_AREA / area) ** 0.5
        scale = max(0.72, min(1.35, scale))
        key = name.replace("logo-ref-", "").replace(".svg", "").replace(".png", "")
        scales[key] = round(scale, 3)
        print(f"{name}: area≈{area} scale={scale:.3f}")

    css_path = os.path.join(os.path.dirname(__file__), "logo-scales.css")
    lines = ["/* Généré par optical_logos.py — scales optiques par logo */"]
    for key, sc in scales.items():
        lines.append(f".logosvg--{key}{{transform:scale({sc});}}")
    open(css_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump(scales, open(os.path.join(os.path.dirname(__file__), "logo-scales.json"), "w"), indent=2)
    print("OK ->", css_path)


if __name__ == "__main__":
    main()
