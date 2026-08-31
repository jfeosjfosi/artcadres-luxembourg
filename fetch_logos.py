#!/usr/bin/env python3
"""Télécharge et normalise les logos références (monochrome #2c1f17)."""
import os
import re
import subprocess
import urllib.request

OUT = os.path.join(os.path.dirname(__file__), "assets", "logos")
UA = {"User-Agent": "ArtCadresSiteBot/1.0 (Art'Cadres static site; contact@artcadres.lu)"}
COLOR = "#2c1f17"

SOURCES = {
    "logo-ref-deloitte.svg": "https://upload.wikimedia.org/wikipedia/commons/c/cc/Deloitte_old_blue_logo.svg",
    "logo-ref-accor.svg": "https://upload.wikimedia.org/wikipedia/commons/4/46/AccorHotels_Logo_2016.svg",
    "logo-ref-ses.svg": "https://upload.wikimedia.org/wikipedia/commons/6/67/SES_S.A._logo.svg",
    "logo-ref-bnl.png": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Biblioth%C3%A8que_nationale_de_Luxembourg_logo.png",
}

WORDMARKS = {
    "logo-ref-sodikart.svg": ("SODIKART", 16, 700),
    "logo-ref-maisonheler.svg": ("Maison Heler", 14, 600),
    "logo-ref-mchat.svg": ("M.CHAT", 18, 800),
    "logo-ref-courducale.svg": ("Cour grand-ducale", 13, 700, True),
}


def recolor_svg(text, color=COLOR):
    text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
    text = re.sub(r"<\?xml[\s\S]*?\?>", "", text)
    text = re.sub(r"<!DOCTYPE[^>]*>", "", text, flags=re.I)
    # force single ink on vector shapes
    text = re.sub(r'\sfill="(?!none)[^"]*"', f' fill="{color}"', text)
    text = re.sub(r'\sstroke="(?!none)[^"]*"', f' stroke="{color}"', text)
    text = re.sub(r"style=\"[^\"]*fill:[^;\"]+;?", 'style="fill:' + color + ";", text)
    if "<svg" in text and 'fill="' + color not in text[:800]:
        text = text.replace("<svg", f'<svg fill="{color}"', 1)
    return text


def wordmark_svg(label, size=16, weight=700, stacked=False):
    if stacked:
        w = 200
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 44" role="img" aria-label="{label}">
  <text x="0" y="17" font-family="Manrope, ui-sans-serif, system-ui, sans-serif" font-size="{size + 1}" font-weight="800" fill="{COLOR}" letter-spacing="0.08em">COUR</text>
  <text x="0" y="36" font-family="Manrope, ui-sans-serif, system-ui, sans-serif" font-size="{size}" font-weight="600" fill="{COLOR}" letter-spacing="0.03em">grand-ducale</text>
</svg>'''
    w = max(120, len(label) * (size * 0.62))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} 40" role="img" aria-label="{label}">
  <text x="0" y="28" font-family="Manrope, ui-sans-serif, system-ui, sans-serif" font-size="{size}" font-weight="{weight}" fill="{COLOR}" letter-spacing="0.04em">{label}</text>
</svg>'''


def download(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return dest


def mono_png(src, dest):
    subprocess.run([
        "magick", src,
        "-alpha", "on",
        "-colorspace", "Gray",
        "-fill", COLOR, "-colorize", "100",
        "-trim", "+repage",
        "-background", "none",
        "-gravity", "center",
        "-extent", "280x80",
        dest,
    ], check=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, url in SOURCES.items():
        path = os.path.join(OUT, name)
        print("fetch", name)
        download(url, path)
        if name.endswith(".svg"):
            svg = open(path, encoding="utf-8", errors="replace").read()
            open(path, "w", encoding="utf-8").write(recolor_svg(svg))
        elif name.endswith(".png"):
            tmp = path + ".tmp.png"
            mono_png(path, tmp)
            os.replace(tmp, path)
    for name, spec in WORDMARKS.items():
        path = os.path.join(OUT, name)
        print("wordmark", name)
        if len(spec) == 4:
            open(path, "w", encoding="utf-8").write(wordmark_svg(spec[0], spec[1], spec[2], spec[3]))
        else:
            open(path, "w", encoding="utf-8").write(wordmark_svg(spec[0], spec[1], spec[2]))
    print("OK:", len(os.listdir(OUT)), "fichiers dans assets/logos/")


if __name__ == "__main__":
    main()
