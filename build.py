#!/usr/bin/env python3
"""Generateur du site statique Art'Cadres Luxembourg.
Produit des fichiers .html autonomes (header/footer partages) a cote de ce script.
Lancer :  python3 build.py
"""
import html
import json
import os
from datetime import date

OUT = os.path.dirname(os.path.abspath(__file__))
# URL live tant que le DNS artcadres.lu n'est pas basculé vers GitHub Pages
SITE_URL = "https://jfeosjfosi.github.io/artcadres-preview"

NAV = [
    ("Accueil", "index.html"),
    ("Sur mesure", "encadrement-sur-mesure.html"),
    ("Standards", "encadrement-standard.html"),
    ("Restauration", "dorures-restauration.html"),
    ("Institutions", "institutions-entreprises.html"),
    ("Galerie", "notre-galerie.html"),
    ("Histoire", "notre-histoire.html"),
    ("Partenaires", "partenaires.html"),
]
NAV_CFG = ("Configurateur", "configurateur.html")
NAV_CTA = ("Contact", "contact.html")

ICON = {
    "frame": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="1"/><rect x="7.5" y="7.5" width="9" height="9"/></svg>',
    "ruler": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 20.5V3.5h5.5v11.5H20.5v5.5H3.5z"/><path d="M9 8H5.2M9 12H5.2M9 16H5.2M12 20.5v-3M16 20.5v-3"/></svg>',
    "photo": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="1.5"/><circle cx="9" cy="11" r="1.8"/><path d="M21 16.2l-5.2-5.2-3.8 3.8-2.4-2.4-6.6 6.6"/></svg>',
    "bag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 8h12l1.15 12.2H4.85L6 8z"/><path d="M9.2 8V6.3a2.8 2.8 0 0 1 5.6 0V8"/></svg>',
    "bars": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 7h14M5 12h14M5 17h14"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3.5h8.5L20 8v12.5H7z"/><path d="M15.5 3.5V8H20M10 12.5h7M10 16.5h7"/></svg>',
    "size": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V4M20 20H4M20 20V8M20 20h-6"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg>',
}

ARROW = ('<span class="arw"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/>'
         '</svg></span>')


def e(s):
    return html.escape(s, quote=True)


def btn(label, href, cls="btn"):
    tgt = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return f'<a class="{cls}" href="{href}"{tgt}>{e(label)} {ARROW}</a>'


def btn_orange(label, href):
    """CTA orange — réservé à Contact / rendez-vous."""
    return btn(label, href, cls="btn")


def btn_plain(label, href, arrow=True):
    """Lien discret (configurateur, liens secondaires)."""
    tgt = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    arw = f" {ARROW}" if arrow else ""
    return f'<a class="btn2" href="{href}"{tgt}>{e(label)}{arw}</a>'


def header(active):
    links = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += f'<a href="{href}"{cur}><span>{e(label)}</span></a>'
    cur = ' aria-current="page"' if NAV_CFG[1] == active else ""
    links += f'<a href="{NAV_CFG[1]}"{cur}><span>{e(NAV_CFG[0])}</span></a>'
    cur = ' aria-current="page"' if NAV_CTA[1] == active else ""
    links += f'<a class="cta" href="{NAV_CTA[1]}"{cur}><span>{e(NAV_CTA[0])}</span></a>'
    return f'''<div class="announce"><a href="{NAV_CTA[1]}">Votre artisan encadreur vous accueille sur rendez-vous.</a></div>
<header class="site-header">
  <div class="bar">
    <a class="logo" href="index.html"><img src="assets/logo-artcadres-fonce.svg" alt="Art'Cadres Luxembourg"></a>
    <button class="nav-toggle" aria-label="Ouvrir le menu" onclick="document.body.classList.toggle('nav-open')">
      <svg viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav">
      <button class="nav-toggle nav-close" aria-label="Fermer le menu" onclick="document.body.classList.remove('nav-open')">
        <svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
      {links}
    </nav>
    <div class="nav-backdrop" onclick="document.body.classList.remove('nav-open')"></div>
  </div>
</header>'''


def footer():
    trust = [
        ("shield", "Maison Neumann depuis 1972", "Tradition artisanale à Metz · antenne Luxembourg.", "notre-histoire.html"),
        ("size", "Grands formats & institutions", "Panneaux monumentaux · pose sur site.", "institutions-entreprises.html"),
        ("photo", "Restauration agréée MH", "Tableaux et patrimoine familial.", "dorures-restauration.html"),
        ("doc", "Devis en ligne Nielsen", "Configurateur · retrait en 1 h à Hollerich.", "configurateur.html"),
    ]
    trust_html = "".join(
        f'<a class="trust__item trust__link" href="{href}"><div class="trust__ico">{ICON[k]}</div>'
        f'<h4>{t}</h4><p>{d}</p></a>' for k, t, d, href in trust)
    return f'''<section class="trust trust--icons"><div class="trust__grid">{trust_html}</div></section>
<footer class="site-footer"><div class="fw">
  <div class="footer-cols">
    <div class="fcol footer-logo">
      <img src="assets/logo-artcadres-blanc.svg" alt="Art'Cadres Luxembourg">
      <p>Encadrement sur mesure, cadres standards, dorure et restauration de tableaux. 2 bis rue de la toison d'or, L-2342 Luxembourg (Hollerich).</p>
    </div>
    <div class="fcol"><h3>Nos prestations</h3><div class="flinks">
      <a href="encadrement-sur-mesure.html">Encadrement sur mesure</a>
      <a href="encadrement-standard.html">Cadres standards</a>
      <a href="dorures-restauration.html">Dorure &amp; restauration</a>
      <a href="configurateur.html">Composer votre cadre</a>
    </div></div>
    <div class="fcol"><h3>Explorer</h3><div class="flinks">
      <a href="index.html">Accueil</a>
      <a href="notre-histoire.html">Notre histoire</a>
      <a href="notre-galerie.html">Notre galerie</a>
      <a href="institutions-entreprises.html">Institutions &amp; entreprises</a>
      <a href="partenaires.html">Partenaires</a>
      <a href="contact.html">Contact</a>
    </div></div>
    <div class="fcol"><h3>Nous contacter</h3>
      <p>Une œuvre à encadrer, restaurer, ou une question ? <a href="contact.html">Écrivez-nous</a>.</p>
      <p><a href="mailto:contact@artcadres.lu">contact@artcadres.lu</a><br>
      <a href="tel:+35227849488">+352 27 84 94 88</a><br>
      2 bis rue de la toison d'or, L-2342 Luxembourg</p>
    </div>
  </div>
  <div class="footer-legal">
    <a href="mentions-legales.html">Mentions légales</a>
    <a href="conditions-generales-de-vente.html">CGV</a>
    <a href="politique-de-confidentialite.html">Confidentialité</a>
    <a href="politique-des-cookies.html">Cookies</a>
  </div>
  <div class="footer-bottom">© 2026 Art'Cadres Luxembourg. Maison Neumann depuis 1972.</div>
</div></footer>'''


def schema_local():
    data = {
        "@context": "https://schema.org",
        "@type": ["ProfessionalService", "LocalBusiness"],
        "@id": SITE_URL + "/#localbusiness",
        "name": "Art'Cadres Luxembourg",
        "alternateName": "Maison Neumann Luxembourg",
        "description": "Encadreur d'art à Luxembourg : sur mesure, cadres Nielsen, dorure, restauration de tableaux et galerie. Maison Neumann depuis 1972.",
        "url": SITE_URL + "/",
        "image": SITE_URL + "/assets/ac-contact.jpg",
        "telephone": "+352-27-84-94-88",
        "email": "contact@artcadres.lu",
        "foundingDate": "1972",
        "priceRange": "€€€",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "2 bis rue de la toison d'or",
            "addressLocality": "Luxembourg",
            "postalCode": "L-2342",
            "addressCountry": "LU",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 49.597, "longitude": 6.118},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "10:00",
            "closes": "18:00",
        }],
        "areaServed": {"@type": "Country", "name": "Luxembourg"},
        "sameAs": ["https://www.facebook.com/maisonneumann"],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def schema_contact_page():
    data = {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact Art'Cadres Luxembourg",
        "url": SITE_URL + "/contact.html",
        "mainEntity": {"@id": SITE_URL + "/#localbusiness"},
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def schema_institutions_page():
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Encadrement entreprises et institutions au Luxembourg",
        "url": SITE_URL + "/institutions-entreprises.html",
        "description": "Références B2B : Deloitte, Accor, SES, Bibliothèque nationale, Cour grand-ducale.",
        "about": {"@id": SITE_URL + "/#localbusiness"},
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def schema_faq(items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def page(title, description, body, active, extra_head="", og_image=None, json_ld=""):
    slug = "" if active == "index.html" else active
    canonical = SITE_URL + ("/" if not slug else "/" + slug)
    og_img = og_image or (SITE_URL + "/assets/ac-contact.jpg")
    head_extra = f"\n  {extra_head}" if extra_head else ""
    if json_ld:
        head_extra += f"\n  {json_ld}"
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#2c1f17">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_LU">
  <meta property="og:site_name" content="Art'Cadres Luxembourg">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_img}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">{head_extra}
</head>
<body>
{header(active)}
<main>
{body}
</main>
{footer()}
<script defer src="script.js"></script>
</body>
</html>'''


# ---------- Fragments reutilisables ----------
def content_list(title, items, spaced=False):
    lis = "".join(f'<li><span class="t">{e(t)}</span><span class="d">{e(d)}</span></li>'
                  for t, d in items)
    h = f'<h3 class="p-listh">{e(title)}</h3>' if title else ""
    if spaced:
        return f'<div class="p-list-block reveal">{h}<ul>{lis}</ul></div>'
    return f'{h}<ul>{lis}</ul>'


def metier_grid(title, items):
    """Mosaïque atelier : 2 tuiles larges + 4 compactes. items = (img, title, line, href, featured)."""
    cells = ""
    for img, t, d, href, featured in items:
        lg = " metier__item--lg" if featured else ""
        cells += (
            f'<a class="metier__item{lg}" href="{href}">'
            f'<div class="p-frame"><img src="{img}" alt="{e(t)}" loading="lazy"></div>'
            f'<h3>{e(t)}</h3><p>{e(d)}</p></a>'
        )
    return (
        f'<div class="metier reveal">'
        f'<h2 class="metier__h">{e(title)}</h2>'
        f'<div class="metier__grid">{cells}</div></div>'
    )


def strip(imgs, cols, captions=None, large=False):
    cells = ""
    for i, s in enumerate(imgs):
        load = "eager" if i == 0 else "lazy"
        cap = ""
        if captions and i < len(captions):
            cap = f'<figcaption class="p-cap p-cap--lg">{e(captions[i])}</figcaption>'
        lg = " p-scell--lg" if large else ""
        cells += (f'<figure class="p-scell{lg}"><div class="p-frame"><img src="{s}" alt="" '
                  f'loading="{load}"></div>{cap}</figure>')
    lg_cls = " p-strip--lg" if large else ""
    return f'<div class="p-strip strip-{cols}{lg_cls} reveal">{cells}</div>'


def rest_gallery():
    """Avant / pendant / après en grand, puis un second tableau avant-après."""
    steps = [
        ("assets/rest-avant.jpg", "Avant", "Vernis jauni, toile percée, couleurs ensevelies."),
        ("assets/rest-pendant.jpg", "Pendant", "Consolidation et tests de nettoyage à l'atelier."),
        ("assets/rest-apres.jpg", "Après", "Éclat retrouvé, cadre doré à la feuille."),
    ]
    cells = "".join(
        f'<figure class="rest-step"><div class="p-frame">'
        f'<img src="{src}" alt="{e(title + " — " + cap)}" loading="lazy"></div>'
        f'<figcaption class="p-cap p-cap--lg"><strong>{e(title)}</strong> · {e(cap)}</figcaption>'
        f'</figure>'
        for src, title, cap in steps)
    pair = (
        '<div class="rest-ba">'
        '<figure class="rest-step"><div class="p-frame">'
        '<img src="assets/ac-dorures-3.jpg" alt="Tableau de 1912 avant restauration, pertes de matière" loading="lazy">'
        '</div><figcaption class="p-cap p-cap--lg"><strong>Avant</strong> · Écaillage et pertes de matière</figcaption></figure>'
        '<figure class="rest-step"><div class="p-frame">'
        '<img src="assets/ac-dorures-4.jpg" alt="Tableau de 1910 après restauration à l\'atelier" loading="lazy">'
        '</div><figcaption class="p-cap p-cap--lg"><strong>Après</strong> · Remise en valeur du tableau</figcaption></figure>'
        '</div>'
    )
    return (
        '<div class="rest-work reveal">'
        '<h2 class="p-h2">Le travail, en images</h2>'
        f'<div class="rest-steps">{cells}</div>'
        f'{pair}'
        '</div>'
    )


def content_hero(eyebrow, heading, lead_html, image, caption, solo=False, eager_img=False):
    if solo:
        fig = ""
    else:
        cap = f'<figcaption class="p-cap p-cap--lg">{e(caption)}</figcaption>' if caption else ""
        load = "eager" if eager_img else "lazy"
        fig = (f'<figure class="reveal" style="--d:120ms"><div class="p-frame">'
               f'<img src="{image}" alt="{e(heading)}" loading="{load}"></div>{cap}</figure>')
    solo_cls = " p-hero-solo" if solo else ""
    return (f'<div class="p-hero{solo_cls}"><div class="p-intro reveal">'
            f'<span class="p-eyebrow">{e(eyebrow)}</span>'
            f'<h1 class="p-h1">{e(heading)}</h1>'
            f'<div class="p-lead">{lead_html}</div></div>{fig}</div>')


def content_story(title, paras):
    body = "".join(f"<p>{p}</p>" for p in paras)
    return (f'<div class="p-story reveal"><h2>{e(title)}</h2>'
            f'<div class="p-body">{body}</div></div>')


def logo_wall(items, flex=False):
    tiles = "".join(
        f'<div class="logotile"><div class="logomark">{e(m)}</div>'
        f'<span class="lname">{e(n)}</span>'
        + (f'<span class="lsub">{e(s)}</span>' if s else "")
        + "</div>" for m, n, s in items)
    cls = "logowall flex reveal" if flex else "logowall cols-4 reveal"
    return f'<div class="{cls}">{tiles}</div>'


def legal_page(slug, title, description, html_file):
    root = os.path.join(os.path.dirname(__file__), "..", "contenu-a-coller", html_file)
    with open(root, encoding="utf-8") as f:
        body_html = f.read()
    body = f'''<section class="section legal"><div class="p-w">
<span class="p-eyebrow">Informations</span>
<h1 class="p-h1">{e(title)}</h1>
<div class="legal__body">{body_html}</div>
</div></section>'''
    return (slug, f"{title} | Art'Cadres Luxembourg", description, body)


def ref_logo_strip(items):
    """Bande logos clients. items = ('img', fichier, alt, classe) ou ('word', variante, alt, html)."""
    tiles = []
    for item in items:
        kind = item[0]
        if kind == "img":
            _, fname, alt, cls = item
            tiles.append(
                f'<div class="logotile logotile--brand"><img class="logosvg {cls}" '
                f'src="assets/logos/{fname}" alt="{e(alt)}" loading="lazy"></div>'
            )
        else:
            _, variant, alt, html_inner = item
            tiles.append(
                f'<div class="logotile logotile--brand">'
                f'<span class="logoword logoword--{variant}">{html_inner}</span></div>'
            )
    return f'<div class="logostrip reveal-in">{"".join(tiles)}</div>'


def ref_vignettes(items):
    """Vignettes photo sous le bandeau logos. items = (img, alt, caption)."""
    cells = "".join(
        f'<figure class="ref-showcase__cell"><div class="ref-showcase__frame"><img src="{img}" '
        f'alt="{e(alt)}" loading="lazy"></div>'
        f'<figcaption class="p-cap p-cap--lg"><strong>{e(alt)}</strong> · {e(cap)}</figcaption></figure>'
        for img, alt, cap in items)
    return f'<div class="ref-showcase reveal-in">{cells}</div>'


def polaroid_stack(items):
    """Pile de polaroids carrés qui se chevauchent (hero)."""
    figs = []
    for i, (src, alt) in enumerate(items):
        load = "eager" if i == 0 else "lazy"
        figs.append(
            f'<figure class="polaroid" data-slot="{i}"><img src="{src}" alt="{e(alt)}" '
            f'loading="{load}" draggable="false"></figure>'
        )
    return f'<div class="polaroids">{"".join(figs)}</div>'


def logo_block(items, label="Ils nous font confiance"):
    return (f'<div class="logo-block">'
            f'<p class="logo-block__lab">{e(label)}</p>'
            f'{ref_logo_strip(items)}</div>')


def tech_cards(items):
    cards = "".join(
        f'<article class="tech-card reveal"><figure class="tech-card__img">'
        f'<img src="{img}" alt="{e(title)}" loading="lazy"></figure>'
        f'<h3>{e(title)}</h3><p>{e(txt)}</p></article>'
        for img, title, txt in items)
    return f'<div class="tech-grid">{cards}</div>'


def icon_row(items):
    """Ligne d'icônes + texte court (pages services)."""
    cells = "".join(
        f'<div class="p-ico"><div class="p-ico__mark">{ICON[ic]}</div>'
        f'<h3>{e(t)}</h3><p>{e(d)}</p></div>' for ic, t, d in items)
    return f'<div class="p-icos reveal">{cells}</div>'


def client_cards(items):
    cards = "".join(
        f'<article class="inst-card reveal"><figure class="inst-card__img"><img src="{img}" '
        f'alt="{e(name)}" loading="lazy"></figure>'
        f'<div class="inst-card__body"><h3>{e(name)}</h3><p class="inst-card__tag">{e(tag)}</p>'
        f'<p>{e(txt)}</p></div></article>'
        for img, name, tag, txt in items)
    return f'<div class="inst-grid">{cards}</div>'


# ================= ACCUEIL =================
services = [
    ("frame", "01", "Cadres standards",
     "Aluminium anodisé ou bois Nielsen, prêts à l'emploi. Une sélection permanente à l'atelier, à composer aussi en ligne et à retirer en une heure à Hollerich.",
     "encadrement-standard.html"),
    ("ruler", "02", "Cadres sur mesure",
     "Chaque œuvre dicte sa baguette, son passe-partout et son verre. Nous étudions le format, la lumière et le lieu, puis nous réalisons le cadre à l'atelier.",
     "encadrement-sur-mesure.html"),
    ("photo", "03", "Dorure & restauration",
     "Tableaux, dorure à la feuille et patrimoine familial. Diagnostic à l'atelier, agrément monuments historiques, interventions mesurées pour rendre à la pièce sa présence.",
     "dorures-restauration.html"),
    ("bag", "04", "Institutions & entreprises",
     "Collections corporate, hôtellerie et institutions. Grands formats, séries et pose sur site, du Luxembourg à la Grande Région.",
     "institutions-entreprises.html"),
]
svc_html = "".join(
    f'<a class="p-svc" href="{href}"><div class="p-svc__head">'
    f'<div class="p-svc__ico">{ICON[ic]}</div><span class="n">{n}</span></div>'
    f'<h3>{e(t)}</h3><p>{e(d)}</p></a>'
    for ic, n, t, d, href in services)

REF_LOGOS = [
    ("img", "logo-ref-deloitte.svg", "Deloitte", "logosvg--deloitte"),
    ("img", "logo-ref-accor.svg", "Accor", "logosvg--accor"),
    ("img", "logo-ref-ses.svg", "SES", "logosvg--ses"),
    ("word", "cour", "Cour grand-ducale du Luxembourg",
     "<b>COUR</b><small>grand-ducale</small>"),
    ("word", "bnl", "Bibliothèque nationale du Luxembourg", "BnL"),
    ("word", "heler", "Maison Heler", "Maison Heler"),
    ("word", "sodikart", "SODIKART", "SODIKART"),
    ("word", "mchat", "M.Chat", "M.CHAT"),
]
conf_hl = [
    ("ref-deloitte-install", "Deloitte Luxembourg", "Panneaux muraux et œuvres pour les bureaux"),
    ("ref-accor", "Accor · ibis Styles & Mercure", "Encadrements pour l'hôtellerie"),
    ("ref-maisonheler", "Maison Heler, Metz", "Le bar de l'hôtel signé Philippe Starck"),
    ("ref-mchat", "M.Chat", "Collaboration avec l'artiste Thoma Vuille"),
]
conf_hl_html = "".join(
    f'<figure class="p-scell"><div class="p-frame"><img src="assets/{s}.jpg" '
    f'alt="{e(n)}" loading="lazy"></div><figcaption class="p-cap p-cap--lg">'
    f'<strong>{e(n)}</strong> · {e(d)}.</figcaption></figure>' for s, n, d in conf_hl)

REF_VIGNETTES = [
    ("assets/ref-deloitte-install.jpg", "Deloitte", "Installation grand format sur site"),
    ("assets/ref-accor.jpg", "Accor", "Hôtels ibis Styles, Mercure et MGallery"),
    ("assets/ref-ses.jpg", "SES", "Fournisseur sur site · Betzdorf"),
    ("assets/ref-bibliotheque.jpg", "Bibliothèque nationale", "Grand format en situ"),
]

GAL_TEASER = [(f"assets/gal-{i:02d}.jpg", cap) for i, cap in [
    (1, "Encadrement contemporain"), (3, "Pop-art encadré"), (4, "Aquarelle museum"),
    (8, "Triptyque photographique"), (11, "Galerie privée"), (15, "Encadrement classique"),
    (18, "Série limitée"), (2, "Portrait contemporain"), (23, "Estampe encadrée"),
]]
gal_teaser_html = "".join(
    f'<a class="gal-teaser__cell" href="notre-galerie.html"><img src="{img}" alt="{e(cap)}" loading="lazy"></a>'
    for img, cap in GAL_TEASER)

FAQ_HOME = [
    ("Combien coûte un encadrement sur mesure ?",
     "Le prix dépend du format, de la baguette, du passe-partout et du verre. Notre configurateur calcule le tarif en direct pour les cadres Nielsen. Pour une restauration, un grand format ou un montage museum, nous établissons un devis à l'atelier, sans engagement."),
    ("Quel est le délai ?",
     "Un cadre standard Nielsen se retire souvent en Click & Collect dans l'heure. Un sur-mesure prend en général quelques jours, selon la complexité. Les restaurations et les commandes institutionnelles suivent un planning convenu avec vous."),
    ("Faut-il prendre rendez-vous ?",
     "Oui, nous vous accueillons sur rendez-vous, mercredi au samedi de 10 h à 18 h, au 2 bis rue de la toison d'or à Hollerich. Appelez-nous ou écrivez-nous : nous répondons sous 48 h ouvrées."),
    ("Puis-je composer mon cadre en ligne sans venir ?",
     "Oui. Choisissez baguette, passe-partout et verre dans le configurateur, obtenez le prix tout de suite, puis retirez la pièce à l'atelier. Pour une œuvre fragile, un objet ou un grand format, un passage à l'atelier reste le plus sûr."),
    ("Encadrez-vous les très grands formats ?",
     "Oui. Des médailles aux panneaux muraux de plusieurs mètres : nous encadrons et installons sur site, pour les particuliers comme pour Deloitte, Accor, SES ou la Cour grand-ducale."),
    ("Restaurez-vous les tableaux, ou uniquement l'encadrement ?",
     "Nous restaurons aussi. Vernis jaunis, salissures, petites déchirures : diagnostic à l'atelier, agrément monuments historiques, dorure à la feuille. L'encadrement vient ensuite, quand la pièce le demande."),
    ("Quelle est la différence avec un cadre prêt-à-poser ?",
     "Un cadre de grande surface se choisit au format. Chez nous, la baguette, le carton et le verre sont choisis pour l'œuvre, sa lumière et le mur. Conservation, ajustement au millimètre, finition atelier : ce n'est pas le même métier."),
    ("Quels verres proposez-vous ?",
     "Verre minéral standard, anti-reflet et verres de conservation anti-UV, selon l'œuvre et le budget. Nous vous conseillons sur place pour les photographies, les aquarelles et les pièces à protéger dans le temps."),
    ("Établissez-vous des factures pour les entreprises ?",
     "Oui. Devis, facture et pose sur site pour les directions communication, architectes d'intérieur et collections corporate. Confidentialité et planning adaptés aux institutions."),
    ("Où se trouve l'atelier ?",
     "Art'Cadres est à Hollerich, Luxembourg-Ville : 2 bis rue de la toison d'or, L-2342. Tél. +352 27 84 94 88. Maison Neumann depuis 1972, antenne luxembourgeoise de Kathia Neumann."),
]
faq_html = "".join(
    f'<details class="faq-item"><summary>{e(q)}</summary>'
    f'<div class="faq-a"><div class="faq-a__in"><p>{e(a)}</p></div></div></details>'
    for q, a in FAQ_HOME)

gf_objs = [("obj-medailles", "Médailles & décorations"),
           ("obj-vegetal", "Cadres végétaux"),
           ("obj-cuillere", "Objets (couverts, souvenirs)"),
           ("obj-trefle", "Porte-bonheur & petites pièces")]
gf_objs_html = "".join(
    f'<div class="p-obj"><img src="assets/{s}.jpg" alt="{e(l)}" loading="lazy">'
    f'<span><b>{e(l)}</b></span></div>' for s, l in gf_objs)

avis = [
    ("LuZ De Lor", "Google", "Une adresse de confiance pour tous vos travaux d'encadrement. Mes œuvres ont toutes été parfaitement mises en valeur grâce aux conseils et au travail des artisans."),
    ("Anthony S.", "Google", "J'ai confié l'agrandissement et la mise en cadre d'une photo, je suis ravi du résultat. Travail soigné, de très haute qualité, service impeccable."),
    ("Claudine Arendt", "Google", "Charmant accueil dans un cadre chaleureux, conseil personnalisé et professionnel. Vaste choix de cadres sur mesure, finition de qualité."),
    ("Samuel Gori", "Google", "Parfait du début à la fin. Un travail de grande qualité, de très bons conseils et une vraie attention du détail, tout en maîtrisant le coût final."),
    ("Catherine Christmann", "Google", "L'encadrement de notre lithographie est juste parfait. Votre savoir-faire a sublimé l'œuvre. Merci pour la qualité et le soin des finitions."),
    ("Sandrine Vaglio", "Facebook", "J'en ai rêvé et la Maison Neumann l'a fait ! Le reste est du grand art. Merci à Katia et à son équipe."),
]
avis_cards = "".join(
    f'<div class="p-card"><div class="p-stars">★★★★★</div>'
    f'<p class="p-avquote">« {e(t)} »</p><div class="p-meta">'
    f'<span class="name">{e(n)}</span><span class="p-src">· {e(s)}</span></div></div>'
    for n, s, t in avis)

POLAROIDS = [
    ("assets/kathia-portrait.jpg", "Kathia Neumann à l'atelier"),
    ("assets/ac-contact.jpg", "Mur de baguettes à l'atelier Art'Cadres, Hollerich"),
    ("assets/histoire-atelier-1.jpg", "Œuvre encadrée sur chevalet à l'atelier"),
    ("assets/histoire-atelier-2.jpg", "Commande institutionnelle prête à livrer"),
    ("assets/ac-mesure-2.jpg", "Échantillons de moulures à l'atelier"),
]

accueil_body = f'''<section id="acc">
<div class="p-hero-home">
  <div class="p-hw">
    <a class="p-gtrust" href="#avis">
      <span class="p-gtrust__stars" aria-hidden="true">★★★★★</span>
      <strong>4,9/5</strong>
      <span>Google · 88 avis</span>
    </a>
    <h1 class="p-h1">Encadreur d'art à Luxembourg</h1>
    <div class="p-lead"><p>Encadrement d'art et restauration agréée monuments historiques pour institutions et grands comptes. Maison Neumann depuis 1972, à Hollerich.</p></div>
    <div class="p-btns">{btn_orange("Demander un rendez-vous", "contact.html")} {btn_plain("Composer votre cadre en ligne", "configurateur.html")}</div>
  </div>
  {polaroid_stack(POLAROIDS)}
</div>
<div class="p-w">
  <div class="p-services reveal-in">{svc_html}</div>
  <div class="p-story reveal">
    <div class="p-intro"><h2>Un savoir-faire transmis depuis 1972</h2><div class="p-body"><p>La Maison Neumann encadre et restaure à Metz depuis 1972. Après plus de 30 ans d'expérience, Kathia Neumann a souhaité développer ce savoir-faire au-delà des frontières en créant une antenne à Luxembourg.</p><p>Particuliers, artistes, collectionneurs, architectes, décorateurs et institutions y trouvent un accompagnement personnalisé, du petit cadre aux très grandes pièces.</p></div></div>
    <figure><div class="p-frame"><img src="assets/histoire-mchat.jpg" alt="Un savoir-faire transmis depuis 1972" loading="eager"></div></figure>
  </div>
  {metier_grid("À l'atelier", [
    ("assets/ac-mesure.jpg", "Encadrement sur mesure",
     "Baguette, passe-partout et verre choisis pour l'œuvre, réalisés à Hollerich.",
     "encadrement-sur-mesure.html", True),
    ("assets/ac-standard.jpg", "Cadres Nielsen",
     "Aluminium ou bois, à composer en ligne, à retirer en une heure.",
     "encadrement-standard.html", False),
    ("assets/kathia-grand-format.jpg", "Grands formats",
     "Des médailles aux panneaux de plusieurs mètres, pose sur site.",
     "institutions-entreprises.html", False),
    ("assets/rest-apres.jpg", "Restauration de tableaux",
     "Diagnostic, agrément monuments historiques, interventions mesurées.",
     "dorures-restauration.html", True),
    ("assets/ac-dorures-4.jpg", "Dorure à la feuille",
     "Cadres, miroirs et objets dorés selon les techniques traditionnelles.",
     "dorures-restauration.html", False),
    ("assets/gal-01.jpg", "Galerie d'art",
     "Une collection choisie, encadrée et mise en lumière.",
     "notre-galerie.html", False),
  ])}
  <div class="p-cta p-cta--rich reveal">
    <div class="p-cta__copy">
      <h2>Votre devis, en quelques clics</h2>
      <p>Composez votre cadre en ligne : baguette, passe-partout, verre. Le prix se calcule en direct, sans engagement.</p>
      <div class="p-cta__action">{btn_plain("Accéder au configurateur", "configurateur.html")}<p class="p-cta__note">Click &amp; Collect · retrait en 1 h à l'atelier</p></div>
    </div>
    <figure class="p-cta__fig">
      <div class="p-frame"><img src="assets/ac-mesure-2.jpg" alt="Échantillons de baguettes à l'atelier Art'Cadres" loading="lazy"></div>
    </figure>
  </div>
</div>
</section>
<section id="conf" class="section"><div class="p-w">
<h2 class="p-h2 reveal-in">Des institutions, des marques et des artistes nous confient leurs œuvres</h2>
<p class="p-sub reveal-in">Deloitte, Accor, SES, la Bibliothèque nationale du Luxembourg, la Cour grand-ducale, SODIKART et M.Chat : nous encadrons leurs collections avec la même exigence artisanale.</p>
{ref_logo_strip(REF_LOGOS)}
{ref_vignettes(REF_VIGNETTES)}
<div class="p-cta reveal-in">{btn_orange("Demander un devis institutionnel", "contact.html")} {btn_plain("Voir toutes nos références", "institutions-entreprises.html")}</div>
</div></section>
<section id="gf" class="section"><div class="p-w">
<div class="p-feat reveal">
  <div><p class="p-stat">Du format intime au monumental</p><h2>Nous encadrons et installons sur site</h2><p>Des médailles aux panneaux muraux de plusieurs mètres : nous maîtrisons l'encadrement sur mesure et la pose en entreprise, pour les particuliers comme pour les institutions.</p></div>
  <div class="p-imgs"><div class="p-fr"><img src="assets/kathia-grand-format.jpg" alt="Kathia Neumann installe une œuvre grand format" loading="lazy"></div><div class="p-fr"><img src="assets/gf-deloitte-2.jpg" alt="Panneau mural monumental pour Deloitte" loading="lazy"></div></div>
</div>
<h3 class="p-objh reveal">Nous encadrons tout type d'objet</h3>
<div class="p-objs reveal">{gf_objs_html}</div>
</div></section>
<section id="real" class="section section--alt"><div class="p-w">
<h2 class="p-h2 reveal">Réalisations encadrées</h2>
<p class="p-sub reveal">Pop-art, street-art, aquarelles, photographies et pièces de collection : découvrez une sélection de nos encadrements sur mesure.</p>
<div class="gal-teaser reveal">{gal_teaser_html}</div>
<div class="p-cta reveal">{btn_orange("Explorer la galerie", "notre-galerie.html")}</div>
</div></section>
<section id="faq" class="section"><div class="p-w">
<div class="faq-split reveal">
  <div class="faq-main">
    <h2 class="p-h2">Questions fréquentes</h2>
    <div class="faq">{faq_html}</div>
  </div>
  <aside class="faq-aside">
    <h3>Atelier Hollerich</h3>
    <p class="faq-aside__lead">Nous vous accueillons sur rendez-vous, mercredi au samedi.</p>
    <dl class="faq-aside__dl">
      <div><dt>Téléphone</dt><dd><a href="tel:+35227849488">+352 27 84 94 88</a></dd></div>
      <div><dt>E-mail</dt><dd><a href="mailto:contact@artcadres.lu">contact@artcadres.lu</a></dd></div>
      <div><dt>Adresse</dt><dd>2 bis rue de la toison d'or<br>L-2342 Luxembourg</dd></div>
      <div><dt>Horaires</dt><dd>Mercredi au samedi<br>10 h à 18 h</dd></div>
    </dl>
    <div class="faq-aside__cta">{btn_orange("Prendre rendez-vous", "contact.html")}</div>
  </aside>
</div>
</div></section>
<section id="avis" class="section"><div class="p-w">
<h2 class="p-h2 reveal">Ils nous ont fait confiance, ils en parlent</h2>
<div class="p-badges reveal">
  <div class="p-badge"><span class="v">4,9/5</span><span class="s">★★★★★</span><span class="m">88 avis vérifiés · projets sur mesure au Luxembourg</span></div>
</div>
<div class="p-avis reveal">{avis_cards}</div>
</div></section>'''

# ================= NOTRE HISTOIRE =================
hist_body = f'''<section class="section"><div class="p-w">
{content_hero("Art'Cadres · Luxembourg", "Notre histoire", "<p>Art'Cadres Luxembourg réunit en un même lieu l'encadrement sur mesure, la restauration de tableaux, la dorure et une galerie d'art. Un espace unique où savoir-faire artisanal, conseil personnalisé et passion de l'art se rencontrent.</p>", "assets/ac-histoire.jpg", "L'atelier Art'Cadres, au cœur de Luxembourg-Ville", eager_img=True)}
<div class="hist-stats reveal">
  <div><span class="hist-stats__n">1972</span><span class="hist-stats__l">Maison Neumann</span></div>
  <div><span class="hist-stats__n">30+</span><span class="hist-stats__l">ans d'expérience</span></div>
  <div><span class="hist-stats__n">4</span><span class="hist-stats__l">métiers réunis</span></div>
  <div><span class="hist-stats__n">88</span><span class="hist-stats__l">avis vérifiés</span></div>
</div>
{content_story("L'excellence de l'encadrement sur mesure", ["Chez Art'Cadres Luxembourg, chaque œuvre mérite une présentation à la hauteur de son histoire, de sa valeur et de son caractère.", "Forte de plus de 30 années d'expérience, Kathia Neumann met son expertise artisanale et son regard esthétique au service de créations entièrement sur mesure. Chaque projet fait l'objet d'une étude attentive, pour un encadrement en parfaite harmonie avec l'œuvre, son environnement et la sensibilité de son propriétaire.", "Moulures contemporaines ou classiques, finitions raffinées, verres de protection, passe-partout et techniques traditionnelles : chaque détail est sélectionné avec exigence pour donner naissance à une pièce unique."])}
<div class="p-list reveal">{content_list("Nos métiers réunis en un même lieu", [("Encadrement sur mesure", "Baguette, passe-partout et verre choisis pour sublimer chaque œuvre."), ("Restauration de tableaux", "Conservation et remise en valeur des pièces anciennes."), ("Dorure à la feuille", "Cadres, miroirs et objets dorés selon les techniques traditionnelles."), ("Galerie d'art", "Une collection coup de cœur, encadrée et mise en lumière.")], spaced=True)}</div>
{strip(["assets/kathia-fondatrice.jpg", "assets/kathia-grand-format.jpg", "assets/histoire-atelier-1.jpg"], 3, ["Kathia Neumann · fondatrice", "Installation grand format en entreprise", "Atelier d'encadrement sur mesure"], large=True)}
<figure class="p-quote reveal"><blockquote>« Chaque œuvre mérite une présentation à la hauteur de son histoire. »</blockquote><figcaption>Kathia Neumann, Art'Cadres Luxembourg</figcaption></figure>
<div class="p-note reveal"><p>Particuliers, artistes, collectionneurs, architectes, décorateurs, entreprises et institutions bénéficient d'un accompagnement confidentiel, personnalisé et exigeant.</p></div>
<div class="p-cta reveal">{btn_orange("Prendre rendez-vous", "contact.html")}</div>
</div></section>'''

# ================= ENCADREMENT SUR MESURE =================
mesure_body = f'''<section class="section"><div class="p-w">
{content_hero("Sur mesure", "Encadrement sur mesure au Luxembourg", "<p>L'encadrement d'art est avant tout de l'artisanat, et il existe des centaines de possibilités. L'originalité et la subtilité de l'encadrement font toute la différence dans la mise en valeur de vos œuvres.</p>", "assets/ac-mesure.jpg", "Encadrement sur mesure à l'atelier", eager_img=True)}
{icon_row([("frame", "Étude personnalisée", "Chaque œuvre est analysée avec vous : style, conservation, budget."), ("ruler", "Techniques artisanales", "Marie-Louise, caisse américaine, rehausse et montages museum."), ("size", "Du petit au monumental", "Médailles, objets, tableaux et panneaux muraux pour entreprises.")])}
{content_story("Mettre l'œuvre en valeur, selon votre budget", ["Notre objectif principal est la mise en valeur de l'œuvre, en tenant compte de la sensibilité de chacun, avec un budget adapté grâce à une gamme étendue de moulures tous styles, du contemporain au classique.", "Styles de nos moulures : modernes, noir, blanc, chêne, or, wengé, gris, couleurs."])}
<h2 class="p-h2 reveal">Quelques techniques du sur-mesure</h2>
{tech_cards([
    ("assets/gal-15.jpg", "La Marie-Louise biseautée",
     "Le haut de gamme du passe-partout : un biseau qui crée de la profondeur autour du sujet, en montage traditionnel comme contemporain."),
    ("assets/histoire-atelier-1.jpg", "La caisse américaine",
     "L'œuvre flotte dans le cadre, en léger retrait. Une mise en valeur nette, très demandée pour l'art contemporain et la photographie."),
    ("assets/ac-mesure-2.jpg", "Moulures et baguettes",
     "Des centaines d'échantillons à l'atelier : or, bois, aluminium, patines. Nous choisissons avec vous la baguette qui sert l'œuvre."),
    ("assets/gal-24.jpg", "La technique de rehausse",
     "Le verre reste en suspension au-dessus du sujet. Idéal pour les objets, les pièces en volume et les montages museum."),
])}
{strip(["assets/gal-03.jpg", "assets/gal-08.jpg", "assets/gal-11.jpg", "assets/gal-18.jpg"], 4, ["Pop-art encadré", "Triptyque photographique", "Galerie privée", "Verre museum"], large=True)}
<div class="p-list p-list2 reveal">{content_list("Les baguettes Nielsen, 4 univers", [("Nature", "Bois naturel, massif et placage."), ("Color", "Un monde tout en couleur : vives ou pastel, mates ou brillantes."), ("Design", "Des lignes pures, associées à des finitions sobres ou métallisées."), ("Charme", "L'univers des dorures, des patines à l'ancienne et des finitions blanchies.")])}</div>
{strip(["assets/obj-medailles.jpg", "assets/obj-vegetal.jpg", "assets/obj-cuillere.jpg"], 3, ["Médailles et décorations", "Cadres végétaux", "Objets et souvenirs"], large=True)}
<div class="p-cta reveal">{btn_plain("Composer votre cadre en ligne", "configurateur.html")} {btn_orange("Demander un conseil", "contact.html")}</div>
</div></section>'''

# ================= ENCADREMENT STANDARD =================
standard_body = f'''<section class="section"><div class="p-w">
{content_hero("Cadres standards", "Cadres standards Nielsen au Luxembourg", "<p>Une qualité qui fait la différence : tous les cadres Nielsen, en aluminium comme en bois, sont réalisés avec des matériaux de grande qualité.</p>", "assets/ac-standard.jpg", "Cadres Nielsen, bois et aluminium", eager_img=True)}
{icon_row([("bag", "Click & Collect 1 h", "Retrait à l'atelier Hollerich après commande en ligne."), ("doc", "Devis instantané", "Configurez baguette, passe-partout et verre en direct."), ("shield", "Qualité Nielsen", "Fabrication allemande, certification FSC sur les cadres bois.")])}
<div class="p-list reveal">{content_list("Une qualité qui fait la différence", [("Les cadres bois", "Des dorés aux couleurs vives en passant par les bois bruts : une large palette de styles."), ("Les cadres aluminium", "Simples à charger, démonter et remonter ; tournettes rivetées sur dos MDF, verre minéral 2 mm à chants polis, aucun risque de blessure."), ("Conçus par Nielsen Design", "La certification FSC garantit une gestion responsable des forêts. La plupart de nos cadres bois sont éco-responsables."), ("Fabriqués en Allemagne", "Nielsen, marque de référence de l'encadrement : une expertise sur le cadre, le verre et le contrecollé.")])}</div>
{strip(["assets/ac-standard-1.jpg", "assets/ac-standard-2.jpg"], 2)}
<div class="p-cta reveal">{btn_plain("Composer votre cadre en ligne", "configurateur.html")}</div>
</div></section>'''

# ================= DORURES & RESTAURATION =================
dorures_body = f'''<section id="dor" class="section"><div class="p-w">
{content_hero("Dorure & restauration", "Restauration de tableaux au Luxembourg", "<p>Le temps laisse son empreinte : vernis jaunis, salissures, poussière, petites déchirures ou altérations peuvent ternir la beauté d'un tableau ancien.</p>", "assets/rest-apres.jpg", "Tableau restauré et cadre doré à la feuille", eager_img=True)}
{icon_row([("shield", "Diagnostic sur place", "Nous étudions chaque œuvre avant toute intervention."), ("photo", "Restauration tableaux", "Nettoyage, consolidation et harmonisation avec agrément monuments historiques."), ("frame", "Dorure à la feuille", "Cadres, miroirs et objets dorés selon les techniques traditionnelles.")])}
{content_story("La préservation de votre patrimoine", ["Chez Art'Cadres, nous vous accompagnons dans la préservation de votre patrimoine artistique grâce à des prestations de nettoyage et de restauration réalisées avec le plus grand soin, en collaboration avec Sylvie Schied, restauratrice agréée monuments historiques.", "Chaque œuvre est étudiée avant toute intervention afin de lui redonner son éclat tout en respectant son histoire, ses matériaux et l'intention de l'artiste. Un tableau est bien plus qu'un objet décoratif : c'est un souvenir de famille, un héritage ou une pièce de collection qui mérite d'être préservée pour les générations futures."])}
{rest_gallery()}
<div class="p-note reveal"><p>N'hésitez pas à nous apporter votre tableau pour un diagnostic et un devis personnalisés.</p></div>
<div class="p-cta reveal">{btn_orange("Demander un diagnostic", "contact.html")}</div>
</div></section>'''

# ================= INSTITUTIONS & ENTREPRISES =================
INST_CASES = [
    ("assets/ref-deloitte-install.jpg", "Deloitte Luxembourg", "Grand compte · B2B",
     "Panneaux muraux monumentaux et œuvres contemporaines : étude atelier, fabrication sur mesure et pose sur site dans les bureaux du Grand-Duché."),
    ("assets/ref-accor.jpg", "Accor · ibis Styles, Mercure, MGallery", "Hôtellerie",
     "Encadrements pour plusieurs établissements : art contemporain et photographies dans espaces communs et chambres, avec finitions adaptées au flux hôtelier."),
    ("assets/ref-maisonheler.jpg", "Maison Heler, Metz", "Hôtellerie premium",
     "Le bar de l'hôtel signé Philippe Starck : moulures et finitions artisanales pour un lieu iconique de l'hôtellerie lorraine."),
    ("assets/ref-ses.jpg", "SES", "Satellites · Betzdorf", "Fournisseur sur site du groupe satellite : cadres et présentations pour les espaces corporate et collections d'entreprise."),
    ("assets/ref-bibliotheque.jpg", "Bibliothèque nationale du Luxembourg", "Institution culturelle",
     "Grand format en situ : nous maîtrisons l'encadrement et la pose de pièces monumentales pour les institutions patrimoniales."),
    ("assets/ref-courducale.jpg", "Cour grand-ducale & mairies", "Institution officielle",
     "Plus de 200 portraits officiels encadrés lors des changements protocolaires — un niveau d'exigence que nous assumons avec discrétion."),
    ("assets/ref-sodikart-maillot.jpg", "SODIKART", "Sport · mémorabilia",
     "Maillots signés, pièces de collection et objets sportifs encadrés avec des montages museum adaptés aux pièces de valeur."),
    ("assets/ref-mchat.jpg", "M.Chat · Thoma Vuille", "Artiste",
     "Collaboration avec l'artiste : encadrements sur mesure pour des œuvres iconiques du street-art international."),
]

institutions_body = f'''<section class="section"><div class="p-w">
{content_hero("Institutions & entreprises", "Encadrement pour entreprises et institutions",
"<p>Nous accompagnons les directions communication, les architectes d'intérieur et les responsables de collections corporate. Du petit format au panneau monumental, nous étudions, encadrons et installons sur site.</p><p>Maison Neumann depuis 1972. La même exigence artisanale pour Deloitte, Accor, SES, la Bibliothèque nationale du Luxembourg et la Cour grand-ducale.</p>",
"assets/histoire-atelier-2.jpg", "Commande institutionnelle · portraits officiels prêts à livrer", eager_img=True)}
{logo_block(REF_LOGOS)}
{client_cards(INST_CASES)}
<div class="p-note reveal"><p>Nous intervenons sur rendez-vous à Luxembourg-Ville, Hollerich et dans un rayon de 25 km. Pour un projet institutionnel, contactez-nous directement : devis personnalisé, confidentialité et planning adaptés.</p></div>
<div class="p-cta reveal">{btn_orange("Demander un devis institutionnel", "contact.html")} {btn_plain("Voir la galerie", "notre-galerie.html")}</div>
</div></section>'''

# ================= PARTENAIRES =================
partners = [
    ("logo-part-lencadreheure.svg", "L'encadr'heure", "Bordeaux"),
    ("logo-part-anglesvar.svg", "Angles Var", "La Garde"),
    ("logo-part-cadresdesophie.svg", "Les cadres de Sophie", "Tassin-la-Demi-Lune"),
    ("logo-part-artetcadres.svg", "Art et Cadres", "Toulouse"),
    ("logo-part-histoirecadre.svg", "Une histoire de cadre", "Mulhouse"),
    ("logo-part-cadreroussin.svg", "Cadre Roussin", "Paris 15e"),
    ("logo-part-encadreurauxcadres.svg", "L'encadreur aux cadres", "Caen"),
    ("logo-part-claudesamuel.svg", "Claude Samuel", "Paris 12e"),
    ("logo-part-cadrepassepartout.svg", "Le cadre passe-partout", "Reims"),
    ("logo-part-misterblad.svg", "Misterblad", "Clichy"),
    ("logo-part-chatrrouge.svg", "Le Chat Rouge", "Pau"),
]

def partner_strip(items):
    tiles = "".join(
        f'<div class="partnertile reveal"><img class="logosvg logosvg--partner" '
        f'src="assets/logos/{fname}" alt="{e(name)}" loading="lazy">'
        f'<span class="partnertile__name">{e(name)}</span>'
        f'<span class="partnertile__city">{e(city)}</span></div>'
        for fname, name, city in items)
    return f'<div class="partnergrid">{tiles}</div>'
partenaires_body = f'''<section class="section"><div class="p-w">
{content_hero("Partenaires & fournisseurs", "Nos partenaires et fournisseurs", "<p>Les maisons avec lesquelles nous travaillons, et les encadreurs qui nous recommandent partout en France.</p>", "", "", solo=True)}
<div class="brandfeat reveal" style="margin-top:clamp(48px,6vw,72px)">
  <div class="brandfeat__mark"><span class="wm">nielsen</span><span class="wmsub">Design</span></div>
  <div class="brandfeat__body">
    <h2>Nielsen Design, notre fournisseur de référence</h2>
    <p>Fort d'une expérience de plus de 30 ans dans l'encadrement, Nielsen réunit une équipe de passionnés qui conçoit chaque jour des baguettes et des cadres pour rendre votre intérieur aussi parfait que possible. Nature, Color, Design, Charme : quatre univers, mille possibilités.</p>
    {btn_plain("Visiter le site Nielsen", "https://www.nielsen-design.com/")}
  </div>
</div>
<h2 class="p-h2 reveal" style="margin-top:clamp(72px,9vw,120px)">Ils nous recommandent</h2>
{partner_strip(partners)}
</div></section>'''

# ================= GALERIE =================
GAL_ITEMS = [
    (f"assets/gal-{i:02d}.jpg", cap) for i, cap in enumerate([
        "Encadrement contemporain en intérieur", "Composition murale sur mesure", "Pop-art encadré · pièce signature",
        "Aquarelle et passe-partout museum", "Street-art · cadre aluminium", "Art graphique · finition Nielsen",
        "Triptyque photographique", "Série iconographique encadrée", "Encadrement minimaliste",
        "Galerie privée · mise en scène", "Format paysage · salon", "Vue urbaine · cadre sur mesure",
        "Botanique · passe-partout crème", "Encadrement classique bois", "Art contemporain · caisse américaine",
        "Collection · harmonie chromatique", "Série limitée encadrée", "Encadrement museum · verre anti-UV",
        "Monument parisien · intérieur", "Cuisine design · œuvre encadrée", "Encadrement couleur · chambre",
        "Estampe limitée · caisse américaine", "Peynet · encadrement classique", "Œuvre contemporaine · cadre noir",
    ], 1)
]
gal_cells = "".join(
    f'<figure class="g-cell reveal"><div class="g-frame"><img src="{src}" '
    f'alt="{e(cap)}" loading="{"eager" if i < 3 else "lazy"}"></div>'
    f'<figcaption class="g-cap">{e(cap)}</figcaption></figure>'
    for i, (src, cap) in enumerate(GAL_ITEMS))
galerie_body = f'''<section id="gal" class="section"><div class="p-w">
<span class="p-eyebrow">Notre galerie</span>
<h1 class="p-h1">Galerie d'art et réalisations encadrées</h1>
<div class="g-lead reveal"><p>Passionnés depuis plus de 30 ans, nous avons construit notre espace galerie autour d'œuvres choisies, encadrées et mises en lumière avec le même soin que celui porté à vos objets.</p></div>
<div class="g-grid">{gal_cells}</div>
<div class="g-cta reveal">{btn_orange("Prendre rendez-vous", "contact.html")}</div>
</div></section>'''

# ================= CONTACT =================
contact_body = f'''<section id="contact" class="section"><div class="p-w">
<span class="p-eyebrow">Nous trouver</span>
<h1 class="p-h1">Contact · Art'Cadres Luxembourg</h1>
<div class="c-lead reveal-in"><p>Votre artisan encadreur vous accueille sur rendez-vous, au cœur de Luxembourg-Ville. Réponse sous 48 h ouvrées.</p></div>
<div class="c-grid reveal-in">
  <div>
    <div class="c-info">
      <div class="c-row"><p class="c-lab">Téléphone</p><div class="c-val"><p><a href="tel:+35227849488" style="text-decoration:none;color:inherit">+352 27 84 94 88</a></p></div></div>
      <div class="c-row"><p class="c-lab">E-mail</p><div class="c-val"><p><a href="mailto:contact@artcadres.lu" style="text-decoration:none;color:inherit">contact@artcadres.lu</a></p></div></div>
      <div class="c-row"><p class="c-lab">Adresse</p><div class="c-val"><p>2 bis rue de la toison d'or<br>L-2342 Luxembourg (Hollerich)</p></div></div>
      <div class="c-row"><p class="c-lab">Horaires</p><div class="c-val"><p>Mercredi au samedi<br>de 10 h à 18 h</p></div></div>
    </div>
    <div class="c-book">{btn_orange("Prendre rendez-vous", "tel:+35227849488")} {btn_plain("Écrire un e-mail", "mailto:contact@artcadres.lu", arrow=False)}</div>
    <div class="c-note"><p>Nous répondons sous 48 h ouvrées. Pour un rendez-vous, appelez-nous ou écrivez-nous directement.</p></div>
  </div>
  <aside class="c-kathia">
    <figure>
      <img src="assets/kathia-portrait.jpg" alt="Kathia Neumann, fondatrice d'Art'Cadres Luxembourg" loading="eager" draggable="false">
      <figcaption>
        <h3>Kathia Neumann</h3>
        <p class="c-founder__role">Fondatrice · Encadreur d'art</p>
        <p>Plus de 30 ans d'expérience dans l'encadrement d'art. Kathia Neumann perpétue le savoir-faire de la Maison Neumann (Metz, 1972) à Luxembourg, avec la même exigence artisanale.</p>
      </figcaption>
    </figure>
  </aside>
</div>
</div></section>'''

# ================= CONFIGURATEUR =================
CFG_URL = "https://nielsen.oxyz.studio/project/new/3b83739c106fa33d171be9a151d26ab9/app"
configurateur_body = f'''<section id="cfg">
<div class="cfg-inner">
  <div class="cfg-head reveal-in">
    <p class="cfg-eyebrow">Sur mesure, en ligne</p>
    <h1 class="cfg-title">Configurateur cadre en ligne · Luxembourg</h1>
    <p class="cfg-intro">Choisissez la baguette, le passe-partout et le verre. Le prix se calcule au fur et à mesure, et vous obtenez votre devis immédiatement.</p>
  </div>
  <div class="cfg-stage cfg-stage--crop reveal">
    <div class="cfg-skeleton" aria-hidden="true"></div>
    <iframe class="cfg-frame" src="{CFG_URL}" title="Configurateur d'encadrement sur mesure" loading="lazy" allow="clipboard-write; fullscreen" referrerpolicy="strict-origin-when-cross-origin" onload="var s=this.parentNode.querySelector('.cfg-skeleton'); if(s) s.style.display='none';"></iframe>
  </div>
  <p class="cfg-fallback">Le configurateur ne s'affiche pas ? <a href="{CFG_URL}" target="_blank" rel="noopener">Ouvrez-le dans un nouvel onglet</a>.</p>
  <div class="cfg-foot reveal">{btn_orange("Une question ? Contactez-nous", "contact.html")}</div>
</div>
</section>'''

# ================= ÉCRITURE =================
INDEX_LD = schema_local() + "\n  " + schema_faq(FAQ_HOME)
CONTACT_LD = schema_contact_page()
INST_LD = schema_institutions_page()

PAGES = [
    ("index.html", "Encadreur d'art à Luxembourg · Art'Cadres (Maison Neumann 1972)",
     "Encadreur d'art à Hollerich : sur mesure, cadres Nielsen, dorure, restauration agréée MH. Institutions Deloitte, Accor, SES. Devis en ligne.",
     accueil_body, "", None, INDEX_LD),
    ("institutions-entreprises.html", "Encadrement entreprises & institutions · Art'Cadres Luxembourg",
     "Encadrement B2B au Luxembourg : Deloitte, Accor, SES, Bibliothèque nationale, Cour grand-ducale. Grands formats et installation sur site.",
     institutions_body, "institutions-entreprises.html", SITE_URL + "/assets/histoire-atelier-2.jpg", INST_LD),
    ("notre-histoire.html", "Notre histoire · Maison Neumann depuis 1972 · Art'Cadres",
     "Art'Cadres Luxembourg perpétue la Maison Neumann (Metz, 1972) : encadrement sur mesure, restauration, dorure et galerie d'art à Hollerich.",
     hist_body, "notre-histoire.html", None, None),
    ("encadrement-sur-mesure.html", "Encadrement sur mesure Luxembourg · Art'Cadres",
     "Encadrement d'art sur mesure à Luxembourg : Marie-Louise, caisse américaine, rehausse, objets et grands formats. Atelier Hollerich.",
     mesure_body, "encadrement-sur-mesure.html", None, None),
    ("encadrement-standard.html", "Cadres Nielsen Luxembourg · Click & Collect 1 h",
     "Cadres standards Nielsen bois et aluminium à Luxembourg. FSC, fabriqués en Allemagne. Devis instantané et retrait en 1 h à Hollerich.",
     standard_body, "encadrement-standard.html", None, None),
    ("dorures-restauration.html", "Restauration tableau & dorure Luxembourg · Art'Cadres",
     "Restauration de tableaux et dorure à la feuille à Luxembourg. Diagnostic gratuit, agrément monuments historiques, patrimoine familial.",
     dorures_body, "dorures-restauration.html", None, None),
    ("notre-galerie.html", "Galerie d'art & réalisations encadrées · Art'Cadres",
     "Galerie Art'Cadres Luxembourg : œuvres encadrées sur mesure, pop-art, photographies et pièces de collection.",
     galerie_body, "notre-galerie.html", SITE_URL + "/assets/gal-01.jpg", None),
    ("partenaires.html", "Partenaires Nielsen & réseau encadreurs · Art'Cadres",
     "Nielsen Design et réseau d'encadreurs partenaires recommandant Art'Cadres Luxembourg.",
     partenaires_body, "partenaires.html", None, None),
    ("contact.html", "Contact Art'Cadres Luxembourg · Hollerich · RDV",
     "Contactez Art'Cadres : 2 bis rue de la toison d'or, L-2342 Luxembourg. Tél. +352 27 84 94 88. Rendez-vous avec Kathia Neumann.",
     contact_body, "contact.html", SITE_URL + "/assets/kathia-portrait.jpg", CONTACT_LD),
    ("configurateur.html", "Configurateur cadre en ligne · Devis instantané · Art'Cadres",
     "Composez votre cadre sur mesure en ligne : baguette Nielsen, passe-partout, verre. Prix en direct, retrait Click & Collect 1 h.",
     configurateur_body, "configurateur.html", None, None),
]
PAGES.extend([
    legal_page("mentions-legales.html", "Mentions légales",
               "Informations légales du site Art'Cadres Luxembourg.", "mentions-legales.html"),
    legal_page("conditions-generales-de-vente.html", "CGV / CGU",
               "Conditions générales de vente et d'utilisation Art'Cadres Luxembourg.",
               "conditions-generales-de-vente.html"),
    legal_page("politique-de-confidentialite.html", "Politique de confidentialité",
               "Politique de confidentialité et protection des données Art'Cadres Luxembourg.",
               "politique-de-confidentialite.html"),
    legal_page("politique-des-cookies.html", "Politique des cookies",
               "Politique des cookies Art'Cadres Luxembourg.", "politique-des-cookies.html"),
])

PAGE_URLS = []

for entry in PAGES:
    if len(entry) == 4:
        fname, title, desc, body = entry
        active, og_image, json_ld = fname, None, ""
    else:
        fname, title, desc, body, active, og_image, json_ld = entry
        if json_ld is None:
            json_ld = ""
    extra = ""
    if fname == "index.html":
        extra = '<link rel="preload" as="image" href="assets/ac-contact.jpg">'
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(page(title, desc, body, active, extra, og_image=og_image, json_ld=json_ld))
    print("écrit :", fname)
    if not fname.startswith("politique") and "mentions" not in fname and "conditions" not in fname:
        PAGE_URLS.append(fname)

# sitemap.xml
today = date.today().isoformat()
urls_xml = "".join(
    f"  <url><loc>{SITE_URL}/{'' if u == 'index.html' else u}</loc>"
    f"<lastmod>{today}</lastmod><changefreq>monthly</changefreq>"
    f"<priority>{'1.0' if u == 'index.html' else '0.8'}</priority></url>\n"
    for u in PAGE_URLS)
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls_xml}</urlset>\n')
print("écrit : sitemap.xml")

with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print("écrit : robots.txt")

with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(f"""# Art'Cadres Luxembourg
> Encadreur d'art à Luxembourg (Hollerich). Maison Neumann depuis 1972.

## Pages principales
- {SITE_URL}/ — Encadreur d'art, institutions, grands formats
- {SITE_URL}/institutions-entreprises.html — B2B Deloitte, Accor, SES, BNL
- {SITE_URL}/encadrement-sur-mesure.html — Sur mesure artisanal
- {SITE_URL}/encadrement-standard.html — Cadres Nielsen
- {SITE_URL}/dorures-restauration.html — Restauration & dorure agréée MH
- {SITE_URL}/notre-galerie.html — Galerie et réalisations
- {SITE_URL}/notre-histoire.html — Maison Neumann depuis 1972
- {SITE_URL}/partenaires.html — Réseau Nielsen
- {SITE_URL}/configurateur.html — Devis en ligne Nielsen
- {SITE_URL}/contact.html — Rendez-vous Hollerich

## Contact
contact@artcadres.lu · +352 27 84 94 88
2 bis rue de la toison d'or, L-2342 Luxembourg
""")
print("écrit : llms.txt")

open(os.path.join(OUT, ".nojekyll"), "w").close()
print("écrit : .nojekyll")

print("OK,", len(PAGES), "pages générées.")
