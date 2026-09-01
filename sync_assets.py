#!/usr/bin/env python3
"""Synchronise les assets client vers artcadres-site/assets/.
Lancer depuis artcadres-site/ :  python3 sync_assets.py
"""
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.join(ROOT, "..", "ArtCadres-refs")
WT = os.path.join(REFS, "WeTransfer_photos_site")
AS = os.path.join(ROOT, "assets")


def resize(src, dst, max_px=1400):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.isfile(src):
        print("MISS:", src)
        return False
    try:
        subprocess.run(
            ["sips", "-Z", str(max_px), src, "--out", dst],
            check=True, capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        shutil.copy2(src, dst)
    print("OK:", os.path.basename(dst))
    return True


def wt(n):
    for ext in (".jpeg", ".jpg", ".png", ".JPEG"):
        p = os.path.join(WT, f"image{n:05d}{ext}")
        if os.path.isfile(p):
            return p
    return None


# Galerie WT → gal-XX.jpg (ordre éditorial)
GAL = [
    (5, "Encadrement contemporain en intérieur"),
    (15, "Composition murale sur mesure"),
    (11, "Pop-art encadré · pièce signature"),
    (17, "Aquarelle et passe-partout museum"),
    (32, "Street-art · cadre aluminium"),
    (9, "Art graphique · finition Nielsen"),
    (22, "Triptyque photographique"),
    (33, "Série iconographique encadrée"),
    (6, "Encadrement minimaliste"),
    (43, "Galerie privée · mise en scène"),
    (20, "Format paysage · salon"),
    (46, "Vue urbaine · cadre sur mesure"),
    (13, "Botanique · passe-partout crème"),
    (1, "Encadrement classique bois"),
    (42, "Art contemporain · caisse américaine"),
    (47, "Collection · harmonie chromatique"),
    (21, "Série limitée encadrée"),
    (25, "Encadrement museum · verre anti-UV"),
    (38, "Monument parisien · intérieur"),
    (40, "Cuisine design · œuvre encadrée"),
    (16, "Encadrement couleur · chambre"),
    (28, "Atelier · baguettes et moulures"),
    (36, "Chevalet et finitions artisanales"),
    (14, "Détail passe-partout biseauté"),
]

REF_FILES = [
    (os.path.join(REFS, "Fwd_Deloitte__b2ac321c0c", "IMG_7843.jpeg"), "ref-deloitte-install.jpg", 1400),
    (os.path.join(REFS, "Fwd_Deloitte__b2ac321c0c", "IMG_7846.jpeg"), "kathia-grand-format.jpg", 1400),
    (os.path.join(REFS, "Fwd_Avec_Mr_chat__cddc9f9eb2", "IMG_2435.jpg"), "kathia-fondatrice.jpg", 1200),
    (os.path.join(REFS, "Fwd__a4191fb079", "IMG_1585.jpg"), "ref-sodikart-maillot.jpg", 1200),
    (os.path.join(REFS, "Fwd_SES__590afadec1", "IMG_5065.jpeg"), "ref-ses.jpg", 1200),
    (os.path.join(REFS, "Fwd_Htel_mercure__2baea2e3d5", "IMG_8814.jpeg"), "ref-accor.jpg", 1200),
    (os.path.join(REFS, "Fwd_Deloitte__b2ac321c0c", "IMG_7852.jpeg"), "gf-deloitte-2.jpg", 1400),
    (os.path.join(REFS, "Fwd_Deloitte__b2ac321c0c", "IMG_7843.jpeg"), "gf-deloitte-1.jpg", 1400),
]

HERO_CANDIDATES = [46, 40, 38]


def main():
    for i, (wt_num, _cap) in enumerate(GAL, start=1):
        src = wt(wt_num)
        if src:
            resize(src, os.path.join(AS, f"gal-{i:02d}.jpg"))

    for src, name, px in REF_FILES:
        resize(src, os.path.join(AS, name), px)

    for n in HERO_CANDIDATES:
        src = wt(n)
        if src:
            resize(src, os.path.join(AS, "ac-accueil.jpg"), 1920)
            break

    print("Sync terminé.")


if __name__ == "__main__":
    main()
