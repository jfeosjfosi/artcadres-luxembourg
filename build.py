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
# Canonical = repo d'origine (Pages). Ne PAS mettre artcadres.lu tant que le
# WordPress y est encore live (sinon Google consoliderait vers l'ancien site).
# Au cutover DNS : SITE_URL = "https://artcadres.lu" + 301 (voir SEO/REDIRECTIONS-301.md).
SITE_URL = "https://jfeosjfosi.github.io/artcadres-luxembourg"
DATE_PUBLISHED = "2026-09-01"
TEL_SCHEMA = "+352-27-84-94-88"
TEL_E164 = "+35227849488"

NAV = [
    ("Accueil", "index.html"),
    ("Restauration", "dorures-restauration.html"),
    ("Institutions", "institutions-entreprises.html"),
    ("Galerie", "notre-galerie.html"),
    ("Histoire", "notre-histoire.html"),
]
NAV_FRAME = [
    ("Sur mesure", "encadrement-sur-mesure.html"),
    ("Standard", "encadrement-standard.html"),
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
    """CTA orange — Contact / rendez-vous, plus exception devis configurateur."""
    return btn(label, href, cls="btn")


def btn_plain(label, href, arrow=True):
    """Lien discret (configurateur, liens secondaires)."""
    tgt = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    arw = f" {ARROW}" if arrow else ""
    return f'<a class="btn2" href="{href}"{tgt}>{e(label)}{arw}</a>'


def header(active):
    frame_on = active in {href for _, href in NAV_FRAME}
    links = ""
    for label, href in NAV:
        if label == "Accueil":
            cur = ' aria-current="page"' if href == active else ""
            links += f'<a href="{href}"{cur}><span>{e(label)}</span></a>'
            cur_f = ' aria-current="page"' if frame_on else ""
            parts = []
            for lab, h in NAV_FRAME:
                ac = ' aria-current="page"' if h == active else ""
                parts.append(f'<a href="{h}"{ac}>{e(lab)}</a>')
            items = "".join(parts)
            links += (
                f'<div class="nav-dd">'
                f'<button type="button" class="nav-dd__btn"{cur_f} aria-expanded="false" aria-haspopup="true">'
                f'<span>Encadrement</span></button>'
                f'<div class="nav-dd__menu">{items}</div></div>'
            )
            continue
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
        ("shield", "Un savoir-faire depuis 1972", "Trente ans d'atelier, transmis à Luxembourg.", "notre-histoire.html"),
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
      <p>Encadrement sur mesure, cadres standards, dorure et restauration de tableaux. 2 bis rue de la toison d'or, L-2342 Luxembourg (Hollerich). Pose sur site à Howald et dans un rayon de 25 km.</p>
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
      <a href="encadrement-grand-format.html">Grands formats</a>
      <a href="glossaire-encadrement.html">Glossaire</a>
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
  <div class="footer-bottom">© 2026 Art'Cadres Luxembourg · Un savoir-faire d'encadrement depuis 1972.</div>
</div></footer>'''


def schema_local():
    data = {
        "@context": "https://schema.org",
        "@type": ["ProfessionalService", "LocalBusiness"],
        "@id": SITE_URL + "/#localbusiness",
        "name": "Art'Cadres Luxembourg",
        "alternateName": "Art'Cadres Encadrement",
        "description": "Encadreur d'art à Luxembourg : sur mesure, cadres Nielsen, dorure, restauration de tableaux et galerie. Un savoir-faire depuis 1972.",
        "url": SITE_URL + "/",
        "image": SITE_URL + "/assets/ac-contact.jpg",
        "telephone": TEL_SCHEMA,
        "email": "contact@artcadres.lu",
        "foundingDate": "1972",
        "priceRange": "€€€",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "2 bis rue de la toison d'or",
            "addressLocality": "Luxembourg",
            "addressRegion": "Luxembourg",
            "postalCode": "L-2342",
            "addressCountry": "LU",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 49.5974, "longitude": 6.1183},
        "hasMap": "https://www.google.com/maps?cid=961735473174028194",
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "10:00",
            "closes": "18:00",
        }],
        "areaServed": [
            {"@type": "City", "name": "Luxembourg"},
            {"@type": "Place", "name": "Hollerich"},
            {"@type": "Place", "name": "Howald"},
            {"@type": "AdministrativeArea", "name": "Grande Région"},
        ],
        "founder": {"@id": SITE_URL + "/#kathia"},
        "employee": [
            {"@id": SITE_URL + "/#kathia"},
            {"@id": SITE_URL + "/#sylvie"},
        ],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {
                "@type": "Service", "@id": SITE_URL + "/encadrement-sur-mesure.html#service",
                "name": "Encadrement sur mesure",
                "url": SITE_URL + "/encadrement-sur-mesure.html",
            }},
            {"@type": "Offer", "itemOffered": {
                "@type": "Service", "@id": SITE_URL + "/encadrement-standard.html#service",
                "name": "Cadres Nielsen",
                "url": SITE_URL + "/encadrement-standard.html",
            }},
            {"@type": "Offer", "itemOffered": {
                "@type": "Service", "@id": SITE_URL + "/dorures-restauration.html#service",
                "name": "Restauration de tableaux et dorure",
                "url": SITE_URL + "/dorures-restauration.html",
            }},
            {"@type": "Offer", "itemOffered": {
                "@type": "Service", "@id": SITE_URL + "/institutions-entreprises.html#service",
                "name": "Encadrement institutions et entreprises",
                "url": SITE_URL + "/institutions-entreprises.html",
            }},
        ],
        "sameAs": ["https://www.facebook.com/maisonneumann"],
        "knowsAbout": [
            "Encadrement d'art", "Restauration de tableaux", "Dorure à la feuille",
            "Cadres Nielsen", "Pose grand format",
        ],
    }
    people = [
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "@id": SITE_URL + "/#kathia",
            "name": "Kathia Neumann",
            "jobTitle": "Fondatrice, encadreur d'art",
            "worksFor": {"@id": SITE_URL + "/#localbusiness"},
            "image": SITE_URL + "/assets/kathia-portrait.jpg",
            "url": SITE_URL + "/notre-histoire.html",
        },
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "@id": SITE_URL + "/#sylvie",
            "name": "Sylvie Schied",
            "jobTitle": "Restauratrice agréée monuments historiques",
            "worksFor": {"@id": SITE_URL + "/#localbusiness"},
            "url": SITE_URL + "/dorures-restauration.html",
        },
    ]
    tags = [f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>']
    for p in people:
        tags.append(f'<script type="application/ld+json">{json.dumps(p, ensure_ascii=False)}</script>')
    tags.append(schema_organization())
    tags.append(schema_website())
    return "\n  ".join(tags)


def schema_organization():
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": SITE_URL + "/#organization",
        "name": "Art'Cadres Luxembourg",
        "alternateName": "Art'Cadres Encadrement",
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/assets/logo-artcadres-fonce.svg",
        "sameAs": ["https://www.facebook.com/maisonneumann"],
        "parentOrganization": {
            "@type": "Organization",
            "name": "Maison Neumann",
            "url": "https://maisonneumann.com/",
        },
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def schema_website():
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": SITE_URL + "/#website",
        "url": SITE_URL + "/",
        "name": "Art'Cadres Luxembourg",
        "inLanguage": "fr-LU",
        "publisher": {"@id": SITE_URL + "/#organization"},
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def provider_entity():
    return {
        "@id": SITE_URL + "/#localbusiness",
        "@type": "LocalBusiness",
        "name": "Art'Cadres Luxembourg",
        "url": SITE_URL + "/",
        "telephone": TEL_SCHEMA,
    }


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


CRUMBS = {
    "index.html": [("Accueil", "index.html")],
    "encadrement-sur-mesure.html": [("Accueil", "index.html"), ("Sur mesure", "encadrement-sur-mesure.html")],
    "encadrement-standard.html": [("Accueil", "index.html"), ("Standards", "encadrement-standard.html")],
    "dorures-restauration.html": [("Accueil", "index.html"), ("Restauration", "dorures-restauration.html")],
    "institutions-entreprises.html": [("Accueil", "index.html"), ("Institutions", "institutions-entreprises.html")],
    "notre-galerie.html": [("Accueil", "index.html"), ("Galerie", "notre-galerie.html")],
    "notre-histoire.html": [("Accueil", "index.html"), ("Histoire", "notre-histoire.html")],
    "configurateur.html": [("Accueil", "index.html"), ("Configurateur", "configurateur.html")],
    "contact.html": [("Accueil", "index.html"), ("Contact", "contact.html")],
    "encadrement-grand-format.html": [("Accueil", "index.html"), ("Grands formats", "encadrement-grand-format.html")],
    "glossaire-encadrement.html": [("Accueil", "index.html"), ("Glossaire", "glossaire-encadrement.html")],
    "404.html": [("Accueil", "index.html"), ("Page introuvable", "404.html")],
}


def schema_breadcrumb(active):
    trail = CRUMBS.get(active) or CRUMBS["index.html"]
    items = []
    for i, (name, href) in enumerate(trail, 1):
        loc = SITE_URL + ("/" if href == "index.html" else "/" + href)
        items.append({"@type": "ListItem", "position": i, "name": name, "item": loc})
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def schema_service(name, desc, page_file):
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": SITE_URL + "/" + page_file + "#service",
        "name": name,
        "description": desc,
        "url": SITE_URL + "/" + page_file,
        "provider": provider_entity(),
        "areaServed": [
            {"@type": "City", "name": "Luxembourg"},
            {"@type": "Place", "name": "Hollerich"},
            {"@type": "Place", "name": "Howald"},
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def schema_images(items):
    """items = (contentUrl_path, name)."""
    data = {
        "@context": "https://schema.org",
        "@type": "ImageGallery",
        "name": "Galerie Art'Cadres Luxembourg",
        "url": SITE_URL + "/notre-galerie.html",
        "image": [
            {
                "@type": "ImageObject",
                "contentUrl": SITE_URL + "/" + src,
                "name": name,
                "creator": {"@id": SITE_URL + "/#organization"},
                "copyrightHolder": {"@id": SITE_URL + "/#organization"},
            }
            for src, name in items
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def faq_markup(items):
    return "".join(
        f'<details class="faq-item"><summary>{e(q)}</summary>'
        f'<div class="faq-a"><div class="faq-a__in"><p>{e(a)}</p></div></div></details>'
        for q, a in items
    )


def compare_table(caption, headers, rows):
    th = "".join(f"<th>{e(h)}</th>" for h in headers)
    trs = "".join(
        "<tr>" + "".join(f"<td>{e(c)}</td>" for c in row) + "</tr>" for row in rows
    )
    cap = f'<p class="p-table-cap">{e(caption)}</p>' if caption else ""
    return (
        f'<div class="p-table-wrap reveal">{cap}'
        f'<table class="p-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'
    )


def faq_section(title, items):
    return (
        f'<div class="p-faq-block reveal"><h2 class="p-h2">{e(title)}</h2>'
        f'<div class="faq">{faq_markup(items)}</div></div>'
    )


def crumbs_nav(active):
    trail = CRUMBS.get(active)
    if not trail or len(trail) < 2:
        return ""
    parts = []
    for i, (label, href) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<span aria-current="page">{e(label)}</span>')
        else:
            parts.append(f'<a href="{href}">{e(label)}</a>')
    sep = '<span class="crumbs__sep" aria-hidden="true">/</span>'
    return f'<nav class="crumbs" aria-label="Fil d\'Ariane">{sep.join(parts)}</nav>'


def page(title, description, body, active, extra_head="", og_image=None, json_ld=""):
    slug = "" if active == "index.html" else active
    canonical = SITE_URL + ("/" if not slug else "/" + slug)
    og_img = og_image or (SITE_URL + "/assets/ac-contact.jpg")
    head_extra = f"\n  {extra_head}" if extra_head else ""
    if json_ld:
        head_extra += f"\n  {json_ld}"
    if active in CRUMBS:
        head_extra += f"\n  {schema_breadcrumb(active)}"
    crumb_html = crumbs_nav(active)
    return f'''<!DOCTYPE html>
<html lang="fr-LU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#2c1f17">
  <meta property="article:published_time" content="{DATE_PUBLISHED}">
  <meta property="article:modified_time" content="{date.today().isoformat()}">
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
{crumb_html}
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
    """Mosaïque atelier : 2 tuiles larges + compactes. items = (img, title, line, href, featured).
    featured True = --lg, 'band' = bandeau pleine largeur (tirage photo)."""
    cells = ""
    for img, t, d, href, featured in items:
        extra = ""
        if featured is True:
            extra = " metier__item--lg"
        elif featured == "band":
            extra = " metier__item--band"
        cells += (
            f'<a class="metier__item{extra}" href="{href}">'
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
        alt = ""
        if captions and i < len(captions):
            alt = captions[i]
            cap = f'<figcaption class="p-cap p-cap--lg">{e(captions[i])}</figcaption>'
        lg = " p-scell--lg" if large else ""
        cells += (f'<figure class="p-scell{lg}"><div class="p-frame"><img src="{s}" alt="{e(alt)}" '
                  f'width="800" height="1000" loading="{load}"></div>{cap}</figure>')
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
        f'<img src="{src}" alt="{e(title + " - " + cap)}" width="900" height="1125" loading="lazy"></div>'
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
        '<div class="rest-work rest-work--lead reveal">'
        '<h2 class="p-h2">Avant, pendant, après</h2>'
        f'<div class="rest-steps">{cells}</div>'
        f'{pair}'
        '</div>'
    )


def content_hero(eyebrow, heading, lead_html, image, caption, solo=False, eager_img=False, wide=False):
    if solo:
        fig = ""
    else:
        cap = f'<figcaption class="p-cap p-cap--lg">{e(caption)}</figcaption>' if caption else ""
        load = "eager" if eager_img else "lazy"
        fig = (f'<figure class="reveal" style="--d:120ms"><div class="p-frame">'
               f'<img src="{image}" alt="{e(heading)}" width="1200" height="900" loading="{load}"></div>{cap}</figure>')
    solo_cls = " p-hero-solo" if solo else ""
    wide_cls = " p-hero--wide" if wide else ""
    return (f'<div class="p-hero{solo_cls}{wide_cls}"><div class="p-intro reveal">'
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
    """Pile de polaroids 4:5 qui se chevauchent (hero)."""
    figs = []
    for i, (src, alt) in enumerate(items):
        load = "eager" if i == 0 else "lazy"
        figs.append(
            f'<figure class="polaroid" data-home="{i}" data-slot="{i}"><img src="{src}" alt="{e(alt)}" '
            f'width="640" height="800" loading="{load}" draggable="false"></figure>'
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


def icon_row(items, extra=""):
    """Ligne d'icônes + texte court (pages services)."""
    cells = "".join(
        f'<div class="p-ico"><div class="p-ico__mark">{ICON[ic]}</div>'
        f'<h3>{e(t)}</h3><p>{e(d)}</p></div>' for ic, t, d in items)
    cls = f"p-icos{extra} reveal"
    return f'<div class="{cls}">{cells}</div>'


def matters_block():
    return (
        '<h2 class="p-h2 reveal">Les trois choix qui font un cadre</h2>'
        '<div class="matters reveal">'
        "<article><h3>Le passe-partout</h3>"
        "<p>Le carton biseauté placé entre l'œuvre et le verre. Il empêche le papier de toucher le verre et il donne de l'air au sujet. Contrecollé PH neutre, sans acide.</p></article>"
        "<article><h3>Le verre</h3>"
        "<p>Il protège l'œuvre, et on la regarde à travers. Selon la pièce, on cherche moins de reflets, plus de filtrage UV, ou les deux. Le détail figure dans le tableau ci-dessous.</p></article>"
        "<article><h3>La baguette</h3>"
        "<p>Le cadre lui-même. Moulures Nielsen ou bois, choisies à l'atelier devant les échantillons, pour le sujet comme pour le mur où il sera accroché.</p></article>"
        "</div>"
    )


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
     "Le prix d'un encadrement sur mesure au Luxembourg dépend du format, de la baguette, du passe-partout et du verre. Pour les cadres Nielsen courants, notre configurateur calcule le tarif en direct : vous voyez le montant avant de vous déplacer à Hollerich. Un montage museum, une Marie-Louise biseautée, une caisse américaine, un objet en volume ou un verre anti-UV à 99 % sortent du catalogue : nous établissons alors un devis à l'atelier, sans engagement. Les grands formats et les séries d'entreprise suivent un chiffrage à part, avec pose sur site si besoin. Apportez l'œuvre ou les cotes : nous vous indiquons une fourchette dès le premier rendez-vous."),
    ("Quel est le délai ?",
     "Un cadre standard Nielsen se retire souvent en Click & Collect dans l'heure, selon le stock à l'atelier. Un encadrement sur mesure prend en général quelques jours : le temps de commander la baguette, de couper les cartons et de monter le verre. Les montages museum, les objets et les très grands formats demandent davantage de préparation. Une restauration de tableau suit un planning propre, convenu après diagnostic, car le séchage des vernis et des apprêts ne se précipite pas. Pour une commande institutionnelle (portraits officiels, série d'hôtel, panneaux Deloitte), nous verrouillons les dates de pose avec vous dès le devis."),
    ("Faut-il prendre rendez-vous ?",
     "Oui. Nous vous accueillons sur rendez-vous, mercredi au samedi de 10 h à 18 h, au 2 bis rue de la toison d'or à Hollerich (L-2342 Luxembourg). Le rendez-vous permet de sortir les échantillons, de regarder l'œuvre à la lumière de l'atelier et de parler budget sans file d'attente. Appelez le +352 27 84 94 88 ou écrivez à contact@artcadres.lu : nous répondons sous 48 h ouvrées. Indiquez si possible le format, le type de pièce (papier, toile, objet, restauration) et si vous souhaitez un Click & Collect Nielsen ou un montage artisanal. Parking de quartier à proximité."),
    ("Puis-je composer mon cadre en ligne sans venir ?",
     "Oui, pour les formats courants Nielsen. Choisissez baguette, passe-partout et verre dans le configurateur : le prix s'affiche tout de suite, sans engagement. Le retrait se fait à l'atelier (pas d'envoi postal). Pour une œuvre fragile, un objet, une médaille, un textile, un verre de conservation ou un format hors catalogue, un passage à Hollerich reste le plus sûr. Le configurateur ne voit pas le grain du papier ni l'épaisseur d'un relief : ces choix se font autour de la table, avec les échantillons. Vous pouvez commencer en ligne, puis nous affiner le montage sur place."),
    ("Encadrez-vous les très grands formats ?",
     "Oui. Des médailles aux panneaux muraux de plusieurs mètres : nous encadrons et installons sur site, dans un rayon d'environ 25 km autour de Luxembourg-Ville, plus loin pour les comptes suivis (Betzdorf, Metz). Deloitte, Accor, SES, la Bibliothèque nationale et la Cour grand-ducale nous ont confié des pièces monumentales et des séries protocolaires. Le grand format n'est pas un cadre agrandi : il faut un châssis adapté, un verre ou un plexi calculé, et une pose à deux. Particuliers artistes et collectionneurs : même atelier, même exigence. Voir la page dédiée aux grands formats."),
    ("Restaurez-vous les tableaux, ou uniquement l'encadrement ?",
     "Nous restaurons aussi. Vernis jaunis, salissures, petites déchirures, soulèvements de couche picturale : le diagnostic se fait à l'atelier avec Sylvie Schied, restauratrice agréée monuments historiques. L'agrément MH est une reconnaissance de l'État français pour intervenir sur le patrimoine classé : il engage une méthode, pas une retouche décorative. Nous ne repeignons pas une œuvre au neuf. L'encadrement et la dorure à la feuille viennent ensuite, quand la pièce le demande. Apportez le tableau sans le démonter vous-même. Devis écrit, aucune intervention sans votre accord."),
    ("Quelle est la différence avec un cadre prêt-à-poser ?",
     "Un cadre de grande surface se choisit au format du commerce. Chez nous, la baguette, le carton PH neutre et le verre sont choisis pour l'œuvre, sa lumière et le mur. Conservation, ajustement au millimètre, finition atelier : ce n'est pas le même métier. Un kit 40 × 50 convient à une affiche. Une aquarelle, une lithographie ou un pastel ont besoin d'un passe-partout sans acide et souvent d'un verre anti-UV. L'express 48 h d'une chaîne limite le catalogue. Nous combinons le Click & Collect Nielsen pour les formats simples et le sur-mesure pour tout ce qui sort de la boîte."),
    ("Quels verres proposez-vous ?",
     "Verre minéral standard (2 mm, chants polis), verre anti-reflet pour le confort visuel, et verres de conservation anti-UV de 55 % à 99 % selon l'œuvre et le budget. Le verre musée (souvent appelé museum) coupe presque tout le rayonnement ultraviolet et réduit les reflets : il est indiqué pour les photographies, les aquarelles et les pièces à transmettre. Un tirage récent en intérieur peu exposé peut rester en verre standard. Nous posons le verre à l'atelier, jamais en kit collé. Le choix se fait autour des échantillons, à Hollerich, en tenant compte de la lumière du lieu d'accrochage."),
    ("Établissez-vous des factures pour les entreprises ?",
     "Oui. Devis, facture et pose sur site pour les directions communication, architectes d'intérieur, hôtels et collections corporate. Confidentialité et planning adaptés aux institutions (sièges, palais, bibliothèques). Nous travaillons déjà avec Deloitte, Accor (ibis Styles, Mercure, MGallery), SES à Betzdorf, la Bibliothèque nationale du Luxembourg et la Cour grand-ducale (plus de 200 portraits officiels). Un e-mail avec les cotes, le lieu de pose et le volume suffit à ouvrir le dossier. Paiement et mentions légales : voir nos CGV. Page dédiée : institutions et entreprises."),
    ("Où se trouve l'atelier ?",
     "Art'Cadres est à Hollerich, Luxembourg-Ville : 2 bis rue de la toison d'or, L-2342. Tél. +352 27 84 94 88. E-mail contact@artcadres.lu. Horaires : mercredi au samedi, 10 h à 18 h, sur rendez-vous. Un savoir-faire d'encadrement transmis depuis 1972 par Kathia Neumann. Pose des grands formats dans un rayon d'environ 25 km (Howald, Kirchberg, et au-delà pour les comptes suivis). L'atelier réunit encadrement, restauration, dorure et une galerie. Plan Google Maps sur la page Contact."),
]
faq_html = faq_markup(FAQ_HOME)

gf_objs = [("obj-medailles", "Médailles & décorations"),
           ("obj-vegetal", "Cadres végétaux"),
           ("obj-cuillere", "Objets (couverts, souvenirs)"),
           ("obj-trefle", "Porte-bonheur & petites pièces")]
gf_objs_html = "".join(
    f'<div class="p-obj"><div class="p-frame"><img src="assets/{s}.jpg" alt="{e(l)}" loading="lazy"></div>'
    f'<span><b>{e(l)}</b></span></div>' for s, l in gf_objs)

avis = [
    ("LuZ De Lor", "Google", "Une adresse de confiance pour tous vos travaux d'encadrement. Mes œuvres ont toutes été parfaitement mises en valeur grâce aux conseils et au travail des artisans."),
    ("Anthony S.", "Google", "J'ai confié l'agrandissement et la mise en cadre d'une photo, je suis ravi du résultat. Travail soigné, de très haute qualité, service impeccable."),
    ("Claudine Arendt", "Google", "Charmant accueil dans un cadre chaleureux, conseil personnalisé et professionnel. Vaste choix de cadres sur mesure, finition de qualité."),
    ("Samuel Gori", "Google", "Parfait du début à la fin. Un travail de grande qualité, de très bons conseils et une vraie attention du détail, tout en maîtrisant le coût final."),
    ("Catherine Christmann", "Google", "L'encadrement de notre lithographie est juste parfait. Votre savoir-faire a sublimé l'œuvre. Merci pour la qualité et le soin des finitions."),
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
    <div class="p-gtrusts">
    <a class="p-gtrust" href="#avis">
      <span class="p-gtrust__stars" aria-hidden="true">★★★★★</span>
      <strong>4,7/5</strong>
      <span>Art'Cadres Luxembourg · 12 avis</span>
    </a>
    </div>
    <h1 class="p-h1">Encadreur d'art à Luxembourg</h1>
    <div class="p-lead"><p>Nous encadrons, dorons et restaurons vos œuvres, du dessin de famille aux 200 portraits officiels de la Cour grand-ducale. Un savoir-faire d'atelier perfectionné depuis 1972, à Hollerich.</p></div>
    <div class="p-btns">{btn_orange("Prendre rendez-vous à l'atelier", "contact.html")} {btn_plain("Voir le prix de mon cadre en ligne", "configurateur.html")}</div>
  </div>
  {polaroid_stack(POLAROIDS)}
</div>
<div class="p-w">
  <div class="p-services reveal-in">{svc_html}</div>
  <div class="p-story reveal">
    <div class="p-intro"><h2>Un savoir-faire transmis depuis 1972</h2><div class="p-body"><p>Le savoir-faire remonte à 1972, à Metz. Après plus de trente ans d'atelier, Kathia Neumann a voulu le porter plus loin et a créé Art'Cadres à Hollerich.</p><p>Particuliers, artistes, collectionneurs, architectes, décorateurs et institutions y trouvent un accompagnement personnalisé, du petit cadre aux très grandes pièces. Nous réalisons aussi vos tirages photo, petits et grands formats.</p></div></div>
    <figure><div class="p-frame"><img src="assets/histoire-mchat.jpg" alt="Un savoir-faire transmis depuis 1972" width="1200" height="900" loading="eager"></div></figure>
  </div>
  {metier_grid("Art'Cadres Luxembourg", [
    ("assets/histoire-atelier-1.jpg", "Encadrement sur mesure",
     "Baguette, passe-partout et verre choisis pour l'œuvre, réalisés à Hollerich.",
     "encadrement-sur-mesure.html", True),
    ("assets/ac-mesure-1.jpg", "Cadres Nielsen",
     "Aluminium ou bois, à composer en ligne, à retirer en une heure.",
     "encadrement-standard.html", False),
    ("assets/kathia-grand-format.jpg", "Grands formats",
     "Des médailles aux panneaux de plusieurs mètres, pose sur site.",
     "encadrement-grand-format.html", False),
    ("assets/rest-apres.jpg", "Restauration de tableaux",
     "Diagnostic avec Sylvie Schied, agréée monuments historiques.",
     "dorures-restauration.html", True),
    ("assets/ac-dorures-4.jpg", "Dorure à la feuille",
     "Cadres, miroirs et objets dorés selon les techniques traditionnelles.",
     "dorures-restauration.html", False),
    ("assets/gal-01.jpg", "Galerie d'art",
     "Une collection choisie, encadrée et mise en lumière.",
     "notre-galerie.html", False),
    ("assets/gal-08.jpg", "Tirage photo",
     "Petits et grands formats, réalisés pour l'encadrement à l'atelier.",
     "encadrement-sur-mesure.html", "band"),
  ])}
  <div class="p-cta p-cta--rich reveal">
    <div class="p-cta__copy">
      <h2>Le prix de votre cadre, tout de suite</h2>
      <p>Choisissez baguette, passe-partout et verre. Le prix s'affiche en direct, sans vous déplacer, sans engagement.</p>
      <div class="p-cta__action">{btn_orange("Composer mon cadre et voir le prix", "configurateur.html")}<p class="p-cta__note">Click &amp; Collect · retrait en 1 h à l'atelier</p></div>
    </div>
    <figure class="p-cta__fig">
      <div class="p-frame"><img src="assets/ac-contact.jpg" alt="Mur de baguettes à l'atelier Art'Cadres, Hollerich" loading="lazy"></div>
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
  <div><p class="p-stat">Du format intime au monumental</p><h2>Nous encadrons et installons sur site</h2><p>Des médailles aux panneaux muraux de plusieurs mètres : nous maîtrisons l'encadrement sur mesure et la pose en entreprise, pour les particuliers comme pour les institutions.</p>{btn_plain("Page grands formats", "encadrement-grand-format.html")}</div>
  <div class="p-imgs"><div class="p-frame"><img src="assets/kathia-grand-format.jpg" alt="Kathia Neumann installe une œuvre grand format" loading="lazy"></div><div class="p-frame"><img src="assets/gf-deloitte-2.jpg" alt="Panneau mural monumental pour Deloitte" loading="lazy"></div></div>
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
    <h3>Art'Cadres Luxembourg</h3>
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
  <div class="p-badge">
    <span class="v">4,7/5</span><span class="s">★★★★★</span>
    <span class="m">Art'Cadres Luxembourg · 12 avis Google</span>
  </div>
</div>
<div class="p-avis reveal">{avis_cards}</div>
</div></section>'''

# ================= NOTRE HISTOIRE =================
hist_body = f'''<section class="section"><div class="p-w">
{content_hero("Art'Cadres · Luxembourg", "Notre histoire", "<p>Art'Cadres Luxembourg réunit en un même lieu l'encadrement sur mesure, la restauration de tableaux, la dorure et une galerie d'art. L'atelier de Hollerich perpétue un savoir-faire né à Metz en 1972.</p>", "assets/ac-histoire.jpg", "L'atelier Art'Cadres, au cœur de Luxembourg-Ville", eager_img=True, wide=True)}
<div class="hist-stats reveal">
  <div><span class="hist-stats__n">1972</span><span class="hist-stats__l">Les débuts de l'atelier</span></div>
  <div><span class="hist-stats__n">30+</span><span class="hist-stats__l">ans d'expérience</span></div>
  <div><span class="hist-stats__n">MH</span><span class="hist-stats__l">agrément Sylvie Schied</span></div>
  <div><span class="hist-stats__n">4,7</span><span class="hist-stats__l">avis Google Luxembourg</span></div>
</div>
{content_story("De Metz à Luxembourg", [
    "L'atelier d'encadrement ouvre à Metz en 1972. Kathia Neumann y travaille plus de trente ans, puis elle installe Art'Cadres à Hollerich.",
    "Rue de la toison d'or, nous faisons le sur-mesure, les cadres Nielsen en Click & Collect, la dorure à la feuille, et la restauration avec Sylvie Schied, agréée monuments historiques. Il y a aussi une galerie. Nous travaillons en français. Pose dans un rayon d'environ 25 km.",
    "L'atelier de Metz reste ouvert, avec sa propre fiche Google : 4,9/5 sur 76 avis. Art'Cadres Luxembourg : 4,7/5 sur 12 avis.",
])}
<div class="p-list reveal">{content_list("Repères", [
    ("1972", "Fondation de l'atelier d'encadrement à Metz."),
    ("30+ ans", "Kathia Neumann encadre, forme l'antenne Luxembourg."),
    ("Hollerich", "Atelier, galerie, Click & Collect, rendez-vous mercredi au samedi."),
    ("Agréée MH", "Sylvie Schied restaure à l'atelier, devis écrit avant le geste."),
])}</div>
<div class="bio-grid reveal">
  <article class="bio-card">
    <h2>Kathia Neumann</h2>
    <p class="bio-card__role">Fondatrice · Encadreur d'art</p>
    <p>Kathia Neumann dirige l'antenne luxembourgeoise. Plus de trente ans de métier : lecture de l'œuvre, choix des moulures, montages museum, suivi des commandes institutionnelles. Elle a formé l'atelier de Hollerich sur le modèle de Metz : conseil à la table, pas de cadre anonyme de grande surface. Les séries Deloitte, Accor, SES et les portraits de la Cour grand-ducale passent par cet interlocuteur unique.</p>
  </article>
  <article class="bio-card">
    <h2>Sylvie Schied</h2>
    <p class="bio-card__role">Restauratrice agréée monuments historiques</p>
    <p>Sylvie Schied restaure les tableaux à l'atelier. L'agrément monuments historiques reconnaît une méthode : diagnostic, tests de nettoyage, consolidations mesurées. Elle n'efface pas l'histoire d'une pièce pour la rendre « neuve ». Vernis jaunis, salissures, petites déchirures, dorure à la feuille : le travail se décide avec vous, par écrit, avant la première intervention. Page dédiée : dorure et restauration.</p>
  </article>
</div>
{icon_row([
    ("ruler", "Encadrement sur mesure", "Baguette, passe-partout et verre choisis pour sublimer chaque œuvre."),
    ("photo", "Restauration de tableaux", "Conservation et remise en valeur des pièces anciennes."),
    ("frame", "Dorure à la feuille", "Cadres, miroirs et objets dorés selon les techniques traditionnelles."),
    ("bag", "Galerie d'art", "Une collection coup de cœur, encadrée et mise en lumière."),
], extra=" p-icos--4")}
{strip(["assets/kathia-portrait.jpg", "assets/histoire-atelier-2.jpg", "assets/histoire-atelier-1.jpg"], 3, ["Kathia Neumann · fondatrice", "Commande prête à livrer, cadres sous film", "Atelier d'encadrement sur mesure"], large=True)}
<div class="hist-end">
  <p class="p-note">Particuliers, artistes, collectionneurs, architectes, décorateurs, entreprises et institutions : un accompagnement confidentiel, à l'atelier.</p>
  {btn_orange("Prendre rendez-vous", "contact.html")}
</div>
</div></section>'''

# ================= ENCADREMENT SUR MESURE =================
FAQ_MESURE = [
    ("Combien coûte un cadre sur mesure à Luxembourg ?",
     "Le tarif suit le format, la baguette, le passe-partout et le verre. Un Nielsen courant se chiffre en ligne. Un montage museum, une Marie-Louise, un objet ou un grand format se devisent à l'atelier, sans engagement."),
    ("Quelle est la différence avec un cadre Nielsen prêt-à-poser ?",
     "Le standard Nielsen convient aux formats du catalogue, retrait en 1 h. Le sur-mesure commence quand le format, l'épaisseur, le verre de conservation ou l'objet sortent de cette boîte."),
    ("Quels délais pour un encadrement artisanal ?",
     "Quelques jours pour une baguette en stock. Plusieurs semaines si la moulure se commande, si le verre musée arrive, ou si la pièce demande un châssis hors norme."),
    ("Encadrez-vous les objets, médailles et textiles ?",
     "Oui : médailles, maillots, végétaux, couverts, pièces en relief. La rehausse maintient le verre au-dessus du volume. Apportez l'objet, ne le forcez pas dans un cadre plat."),
]
mesure_body = f'''<section class="section"><div class="p-w">
{content_hero("Sur mesure", "Encadrement sur mesure au Luxembourg", "<p>L'encadrement d'art est avant tout de l'artisanat, et il existe des centaines de possibilités. L'originalité et la subtilité de l'encadrement font toute la différence dans la mise en valeur de vos œuvres.</p>", "assets/histoire-atelier-1.jpg", "Encadrement sur mesure à l'atelier, Hollerich", eager_img=True)}
{icon_row([("frame", "Étude personnalisée", "Chaque œuvre est analysée avec vous : style, conservation, budget."), ("ruler", "Techniques artisanales", "Marie-Louise, caisse américaine, rehausse et montages museum."), ("size", "Du petit au monumental", "Médailles, objets, tableaux et panneaux muraux pour entreprises.")])}
<div class="p-story reveal">
  <div class="p-intro"><h2>Mise en valeur, selon votre budget</h2><div class="p-body"><p>Nous choisissons la baguette pour l'œuvre, le mur et votre budget : moulures contemporaines ou classiques, du filet discret à l'or. Pros, particuliers, architectes et décorateurs : le même atelier, y compris pour des pièces exposées au Centre Pompidou.</p><p>Le rendez-vous à Hollerich sert à ça : sortir les échantillons, poser l'œuvre sur la table, parler lumière du salon ou du hall d'accueil. Un passe-partout PH neutre (sans acide) protège le papier dans le temps. Un carton bas de gamme jaunit et attaque l'aquarelle. Nous ne le proposons pas.</p></div></div>
  <figure><div class="p-frame"><img src="assets/ac-contact.jpg" alt="Échantillons de moulures à l'atelier" width="1200" height="900" loading="lazy"></div></figure>
</div>
<h3 class="p-listh reveal">Finitions de baguettes disponibles à l'atelier</h3>
<ul class="p-chips reveal"><li>Modernes</li><li>Noir</li><li>Blanc</li><li>Chêne</li><li>Or</li><li>Wengé</li><li>Gris</li><li>Couleurs</li></ul>
{matters_block()}
{compare_table("Types de verre proposés à l'atelier",
    ["Verre", "Usage", "Filtrage UV", "Reflets"],
    [
        ("Minéral 2 mm", "Affiches, tirages récents peu exposés", "Faible", "Présents"),
        ("Anti-reflet", "Intérieurs lumineux, confort visuel", "Variable", "Atténués"),
        ("Conservation 55 à 99 %", "Aquarelles, photos, pièces à transmettre", "Élevé", "Selon gamme"),
        ("Musée (museum)", "Œuvres sensibles, collections", "Jusqu'à 99 %", "Très faibles"),
    ])}
<div class="p-list reveal">{content_list("Du rendez-vous au cadre", [("À l'atelier", "Vous apportez l'œuvre, ou les cotes. Nous regardons le sujet, la lumière et le budget."), ("Quand Nielsen ne suffit plus", "Format hors série, objet, verre de conservation, passe-partout profond."), ("Délais", "Quelques jours à plusieurs semaines, selon la baguette et la charge de l'atelier.")])}</div>
<h2 class="p-h2 reveal">Quelques techniques du sur-mesure</h2>
{tech_cards([
    ("assets/gal-15.jpg", "La Marie-Louise biseautée",
     "Le haut de gamme du passe-partout : un biseau qui crée de la profondeur autour du sujet, en montage traditionnel comme contemporain."),
    ("assets/histoire-atelier-1.jpg", "La caisse américaine",
     "L'œuvre flotte dans le cadre, en léger retrait. Une mise en valeur nette, très demandée pour l'art contemporain et la photographie."),
    ("assets/ac-contact.jpg", "Moulures et baguettes",
     "Des centaines d'échantillons à l'atelier : or, bois, aluminium, patines. Nous choisissons avec vous la baguette qui sert l'œuvre."),
    ("assets/gal-24.jpg", "La technique de rehausse",
     "Le verre reste en suspension au-dessus du sujet. Idéal pour les objets, les pièces en volume et les montages museum."),
])}
{strip(["assets/gal-03.jpg", "assets/gal-08.jpg", "assets/gal-11.jpg", "assets/gal-18.jpg"], 4, ["Pop-art encadré", "Triptyque photographique", "Galerie privée", "Verre museum"], large=True)}
<h3 class="p-objh reveal">Nous encadrons tout type d'objet</h3>
<div class="p-objs reveal">{gf_objs_html}</div>
{faq_section("Questions sur le sur-mesure", FAQ_MESURE)}
<div class="p-cta reveal">{btn_plain("Composer votre cadre en ligne", "configurateur.html")} {btn_orange("Demander un conseil", "contact.html")} {btn_plain("Dorure & restauration", "dorures-restauration.html")}</div>
</div></section>'''

# ================= ENCADREMENT STANDARD =================
FAQ_STANDARD = [
    ("Mon format n'entre pas dans le catalogue, que faire ?",
     "Nous passons au sur-mesure. La baguette est coupée à vos cotes à l'atelier, avec le passe-partout et le verre choisis pour l'œuvre. Le prix se décide alors sur devis à Hollerich, et non dans le configurateur."),
    ("Bois ou aluminium : que choisir ?",
     "L'aluminium se démonte et se remonte facilement (tournettes rivetées, verre minéral 2 mm). Le bois offre davantage de styles : doré, brut, couleur. Les deux sont Nielsen, FSC®, fabriqués en Allemagne."),
    ("Puis-je voir les baguettes avant de commander ?",
     "Oui. Le configurateur donne le prix. Les échantillons sont au mur de l'atelier. Un rendez-vous de dix minutes évite souvent un échange de teinte."),
]
standard_body = f'''<section class="section"><div class="p-w">
{content_hero("Cadres standards", "Cadres standards Nielsen au Luxembourg", "<p>Une qualité qui fait la différence : tous les cadres Nielsen, en aluminium comme en bois, sont réalisés avec des matériaux de grande qualité. Devis en ligne, retrait Click & Collect à Hollerich, souvent dans l'heure.</p>", "assets/ac-mesure-1.jpg", "Passe-partout et cartons Nielsen à l'atelier, Hollerich", eager_img=True)}
{icon_row([("bag", "Click & Collect 1 h", "Retrait à l'atelier Hollerich après commande en ligne."), ("doc", "Devis instantané", "Configurez baguette, passe-partout et verre en direct."), ("shield", "Qualité Nielsen", "Cadre certifié FSC®. Fabrication allemande.")])}
<div class="p-list reveal">{content_list("Une qualité qui fait la différence", [("Les cadres bois", "Des dorés aux couleurs vives en passant par les bois bruts : une large palette de styles."), ("Les cadres aluminium", "Simples à charger, démonter et remonter ; tournettes rivetées sur dos MDF, verre minéral 2 mm à chants polis, aucun risque de blessure."), ("Cadre certifié FSC®", "Conçus par Nielsen Design. La certification FSC® garantit une gestion responsable des forêts."), ("Fabriqués en Allemagne", "Nielsen, marque de référence : une expertise sur le cadre, le verre et le contrecollé.")])}</div>
<div class="p-story reveal">
  <div class="p-intro"><h2>Composez, retirez en 1 h</h2><div class="p-body"><p>Vous composez baguette, passe-partout et verre en ligne. Le prix s'affiche tout de suite. Le retrait se fait à Hollerich, souvent dans l'heure selon le stock. Si le format sort du catalogue, nous passons au sur-mesure.</p><p>Nielsen n'est pas un cadre de grande surface : le verre est minéral, les cartons sont conçus pour l'encadrement, le bois est certifié FSC®. C'est le bon choix pour une photographie, une affiche, un diplôme, un tirage dont le format entre dans la grille. Ce n'est pas le bon choix pour une médaille, un pastel fragile ou un panneau de trois mètres : là, l'atelier reprend la main.</p><p>Le Click & Collect évite l'attente d'un sur-mesure quand le format est connu. Vous pouvez commander le matin, passer l'après-midi. Si la teinte hésite, dix minutes à l'atelier devant le mur de baguettes valent mieux qu'un échange de messages. Revendeur Nielsen à Luxembourg : les quatre univers (Nature, Color, Design, Charme) sont ceux du configurateur et ceux du stock Hollerich.</p></div></div>
  <figure><div class="p-frame"><img src="assets/gal-08.jpg" alt="Photographies encadrées à l'atelier" width="1200" height="900" loading="lazy"></div></figure>
</div>
{compare_table("Cadre Nielsen ou sur-mesure : lequel vous faut-il ?",
    ["", "Cadre Nielsen, en ligne", "Sur-mesure, à l'atelier"],
    [
        ("Pour quelle œuvre", "Photo, affiche, diplôme, tirage dont le format entre dans la grille Nielsen", "Œuvre fragile, objet en volume, médaille, très grand format, pièce à transmettre"),
        ("Délai", "Souvent dans l'heure, selon le stock à Hollerich", "De quelques jours à plusieurs semaines"),
        ("Prix", "Affiché en direct dans le configurateur", "Sur devis, établi à l'atelier une fois l'œuvre vue"),
        ("Verre et passe-partout", "Parmi les options proposées par le configurateur", "Choisis pour l'œuvre : verre de conservation, carton sans acide, Marie-Louise"),
        ("Où cela se décide", "En ligne, puis retrait à Hollerich", "Autour de la table, devant les échantillons"),
    ])}
{strip(["assets/histoire-atelier-1.jpg", "assets/ac-contact.jpg"], 2, ["Échantillons à l'atelier Hollerich", "Mur de baguettes Nielsen"])}
{faq_section("Questions cadres Nielsen", FAQ_STANDARD)}
<div class="p-cta p-cta--cfg reveal">{btn_orange("Accéder au configurateur", "configurateur.html")}<p class="p-cta__note">Click &amp; Collect · retrait en 1 h à l'atelier</p></div>
</div></section>'''

# ================= DORURES & RESTAURATION =================
FAQ_DORURES = [
    ("Qu'est-ce que l'agrément monuments historiques ?",
     "C'est une reconnaissance officielle de compétence pour intervenir sur le patrimoine classé. Sylvie Schied l'a obtenu. Il n'autorise pas n'importe quelle retouche : il engage une méthode (diagnostic, réversibilité, matériaux adaptés). Au Luxembourg, cet agrément reste un signal rare pour un atelier d'encadreur."),
    ("Combien coûte une restauration de tableau ?",
     "Le prix suit l'état, pas le format seul. Un vernis jauni n'est pas une déchirure, une déchirure n'est pas un soulèvement de couche. Diagnostic à l'atelier, devis écrit, aucune intervention sans votre accord. Merci de ne pas démonter le cadre vous-même."),
    ("Restaurez-vous aussi les cadres dorés ?",
     "Oui. Dorure à la feuille d'or (apprêts, bol, brunissoir), pas une peinture métallisée. Cadres, miroirs, consoles, statues, ferronnerie. Nous ne remplaçons pas un cadre ancien par du plastique doré."),
    ("En combien de temps ?",
     "Après diagnostic. Les séchages ne se précipitent pas. Un nettoyage de vernis et une dorure locale se comptent en semaines, pas en 48 h. Nous posons un planning avec vous dès le devis."),
]
dorures_body = f'''<section id="dor" class="section"><div class="p-w">
{content_hero("Dorure & restauration", "Restauration de tableaux au Luxembourg", "<p>Le temps laisse son empreinte : vernis jaunis, salissures, poussière, petites déchirures ou altérations peuvent ternir la beauté d'un tableau ancien. À Hollerich, Sylvie Schied, restauratrice agréée monuments historiques, établit le diagnostic avant toute intervention.</p>", "assets/rest-apres.jpg", "Tableau restauré et cadre doré à la feuille", eager_img=True)}
{icon_row([("shield", "Diagnostic sur place", "Nous étudions chaque œuvre avant toute intervention."), ("photo", "Restauration tableaux", "Nettoyage, consolidation et harmonisation avec agrément monuments historiques."), ("frame", "Dorure à la feuille", "Cadres, miroirs et objets dorés selon les techniques traditionnelles.")])}
{rest_gallery()}
{content_story("Le diagnostic, avant le geste", [
    "Apportez le tableau à l'atelier, sans le démonter. Un cadre mal retiré arrache parfois la toile ou le papier. Sylvie Schied regarde la couche picturale, le châssis, les soulèvements, les manques, le vernis. Elle dit ce qui se fait, ce qui se discute, et ce que nous refusons : repeindre une œuvre « au neuf », masquer une lacune sous un aplomb décoratif, remplacer un cadre ancien par une imitation plastique.",
    "Le devis est écrit. Aucune intervention sans votre accord. Les étapes classiques, selon l'état : dépoussiérage, tests de solubilité, allègement de vernis jauni, consolidation d'une déchirure, masticage ponctuel, réintégration mesurée, vernis final. Chaque geste vise à retrouver la présence de la pièce, pas à inventer un tableau plus jeune que son auteur.",
])}
<div class="p-list reveal">{content_list("Diagnostic, dorure, limites", [("Diagnostic", "Sylvie Schied, agréée monuments historiques. Devis écrit, aucune intervention sans votre accord."), ("Dorure", "Feuille d'or sur cadres, miroirs, consoles, statues et ferronnerie. Apprêts, bol, brunissoir : pas une peinture métallisée."), ("Ce que nous ne faisons pas", "Nous ne repeignons pas une œuvre au neuf. Nous ne remplaçons pas un cadre ancien par du plastique doré.")])}</div>
<div class="bio-card bio-card--solo reveal">
  <h2>Sylvie Schied, restauratrice agréée MH</h2>
  <p>L'agrément monuments historiques est délivré en France après examen des compétences. Il distingue une restauratrice formée à la conservation du patrimoine d'un atelier qui « rafraîchit » les tableaux. À Luxembourg, cet agrément est l'argument le plus rare du métier : il protège les familles qui confient un portrait d'ancêtre autant que les pièces destinées à une collection. Sylvie travaille à Hollerich, dans le même lieu que l'encadrement : une fois la restauration stabilisée, le cadre et le verre se décident sans transporter l'œuvre une seconde fois.</p>
</div>
<div class="p-story reveal">
  <div class="p-intro"><h2>Préservation du patrimoine</h2><div class="p-body"><p>Nettoyage et restauration avec Sylvie Schied, agréée monuments historiques. Chaque œuvre est étudiée avant d'intervenir, pour retrouver l'éclat sans trahir les matériaux ni l'intention de l'artiste. La dorure à la feuille (or, parfois argent ou or blanc selon le cadre) reprend les techniques d'atelier : apprêts, bol, pose de la feuille, brunissoir. Ce n'est pas une bombe métallisée. Un miroir, une console, un cadre baroque : le même soin.</p></div></div>
</div>
{faq_section("Questions restauration et dorure", FAQ_DORURES)}
<div class="p-note reveal"><p>Apportez votre tableau pour un diagnostic et un devis. Merci de ne pas le démonter vous-même.</p></div>
<div class="p-cta reveal">{btn_orange("Demander un diagnostic", "contact.html")}</div>
</div></section>'''

# ================= INSTITUTIONS & ENTREPRISES =================
INST_CASES = [
    ("assets/ref-deloitte-install.jpg", "Deloitte Luxembourg", "Grand compte · B2B",
     "Panneaux muraux monumentaux et œuvres contemporaines : étude atelier, fabrication sur mesure et pose sur site dans les bureaux du Grand-Duché. Le grand format n'est pas un cadre agrandi : châssis, verre ou plexi, accrochage à deux. Confidentialité de chantier, planning hors heures d'ouverture si le hall l'exige."),
    ("assets/ref-accor.jpg", "Accor · ibis Styles, Mercure, MGallery", "Hôtellerie",
     "Encadrements pour plusieurs établissements : art contemporain et photographies dans espaces communs et chambres. Finitions pensées pour le flux hôtelier (maintenance, séries identiques, remplacement d'une pièce sans tout recommencer). Facture et suivi par site."),
    ("assets/ref-maisonheler.jpg", "Maison Heler, Metz", "Hôtellerie premium",
     "Le bar de l'hôtel signé Philippe Starck : moulures et finitions artisanales pour un lieu iconique de l'hôtellerie lorraine. Preuve que l'atelier de Hollerich travaille aussi hors frontière."),
    ("assets/ref-ses.jpg", "SES", "Satellites · Betzdorf", "Fournisseur sur site du groupe satellite : cadres et présentations pour les espaces corporate et collections d'entreprise. Betzdorf est hors du rayon 25 km courant : nous y allons pour les comptes suivis."),
    ("assets/ref-bibliotheque.jpg", "Bibliothèque nationale du Luxembourg", "Institution culturelle",
     "Grand format en situ : nous maîtrisons l'encadrement et la pose de pièces monumentales pour les institutions patrimoniales. Conservation du papier, verre adapté, discrétion dans les salles."),
    ("assets/ref-courducale.jpg", "Cour grand-ducale & mairies", "Institution officielle",
     "Plus de 200 portraits officiels encadrés lors des changements protocolaires. Un niveau d'exigence que nous assumons avec discrétion : séries homogènes, délais tenus, interlocuteur unique."),
    ("assets/ref-sodikart-maillot.jpg", "SODIKART", "Sport · mémorabilia",
     "Maillots signés, pièces de collection et objets sportifs encadrés avec des montages museum adaptés aux pièces de valeur. Rehausse, fond, verre : le textile ne touche pas la glace."),
    ("assets/ref-mchat.jpg", "M.Chat · Thoma Vuille", "Artiste",
     "Collaboration avec l'artiste : encadrements sur mesure pour des œuvres iconiques du street-art international. Caisse américaine et aluminium selon la pièce, pour la galerie comme pour le collectionneur."),
]

institutions_body = f'''<section class="section"><div class="p-w">
{content_hero("Institutions & entreprises", "Encadrement pour entreprises et institutions",
"<p>Nous accompagnons les directions communication, les architectes d'intérieur et les responsables de collections corporate. Du petit format au panneau monumental, nous étudions, encadrons et installons sur site.</p><p>Un savoir-faire d'atelier depuis 1972. La même exigence artisanale pour Deloitte, Accor, SES, la Bibliothèque nationale du Luxembourg et la Cour grand-ducale.</p>",
"assets/histoire-atelier-2.jpg", "Commande institutionnelle · portraits officiels prêts à livrer", eager_img=True)}
{logo_block(REF_LOGOS)}
<h2 class="p-h2 reveal">Références nommées</h2>
<p class="p-sub reveal">Huit références que nous pouvons citer. Chacune a suivi le même chemin : un devis chiffré, une fabrication à l'atelier de Hollerich, une pose sur site.</p>
{client_cards(INST_CASES)}
<h2 class="p-h2 reveal">Comment nous travaillons</h2>
{icon_row([
    ("ruler", "1. Le brief", "Volumes, délais, lieux de pose, charte graphique. Nous travaillons sous confidentialité pour les sièges et les institutions."),
    ("doc", "2. Le devis", "Quantités, baguettes, verre, fonds et pose, chiffrés ligne par ligne. Un e-mail avec les cotes et le lieu suffit à ouvrir le dossier."),
    ("frame", "3. La pose", "Sur site, dans un rayon d'environ 25 km autour de Luxembourg-Ville, plus loin pour les comptes suivis (Betzdorf, Metz)."),
])}
{faq_section("Questions entreprises", [
    ("Facturez-vous les sociétés et les institutions ?",
     "Oui. Devis, facture, interlocuteur unique. Confidentialité de chantier. Planning adapté aux halls, aux musées et aux sièges."),
    ("Intervenez-vous à Kirchberg et Howald ?",
     "Oui. Hollerich est l'atelier. La pose se fait sur site dans un rayon d'environ 25 km, et au-delà pour les comptes suivis."),
    ("Gérez-vous les séries et les remplacements ?",
     "Oui. Portraits officiels, chambres d'hôtel, open spaces : même baguette, même verre, pièces de rechange possibles."),
])}
<div class="p-note reveal"><p>Nous intervenons sur rendez-vous à Luxembourg-Ville, Hollerich et dans un rayon de 25 km. Pour un projet institutionnel : devis, confidentialité, planning.</p></div>
<div class="p-cta reveal">{btn_orange("Demander un devis institutionnel", "contact.html")} {btn_plain("Voir la galerie", "notre-galerie.html")} {btn_plain("Grands formats", "encadrement-grand-format.html")}</div>
</div></section>'''

# ================= PARTENAIRES =================
partners = [
    ("logo-part-lencadreheure.png", "L'encadr'heure", "Bordeaux"),
    ("logo-part-anglesvar.png", "Angles Var", "La Garde"),
    ("logo-part-cadresdesophie.png", "Les cadres de Sophie", "Tassin-la-Demi-Lune"),
    ("", "Art et Cadres", "Toulouse"),
    ("", "Une histoire de cadre", "Mulhouse"),
    ("", "Cadre Roussin", "Paris 15e"),
    ("", "L'encadreur aux cadres", "Caen"),
    ("", "Claude Samuel", "Paris 12e"),
    ("logo-part-cadrepassepartout.png", "Le cadre passe-partout", "Reims"),
    ("logo-part-misterblad.svg", "Misterblad", "Clichy"),
    ("logo-part-chatrrouge.svg", "Le Chat Rouge", "Pau"),
    ("logo-part-lccadres.svg", "LC Cadres", "Enghien-les-Bains"),
    ("logo-part-tetecadre.svg", "La tête dans le cadre", "Saint-Berthevin"),
]


def partner_strip(items):
    logo_dir = os.path.join(os.path.dirname(__file__), "assets", "logos")
    tiles = []
    for fname, name, city in items:
        src = os.path.join(logo_dir, fname) if fname else ""
        use_img = bool(fname and os.path.isfile(src) and os.path.getsize(src) > 800)
        if use_img:
            mark = (
                f'<img class="logosvg logosvg--partner" src="assets/logos/{fname}" '
                f'alt="{e(name)}" loading="lazy">'
            )
        else:
            mark = f'<span class="partnertile__name">{e(name)}</span>'
        tiles.append(
            f'<div class="partnertile reveal">{mark}'
            f'<span class="partnertile__city">{e(city)}</span></div>'
        )
    return f'<div class="partnergrid">{"".join(tiles)}</div>'


partners_block = f'''<div id="partenaires" class="hist-partners">
<div class="brandfeat reveal">
  <div class="brandfeat__mark"><img class="brandfeat__logo" src="assets/logos/logo-nielsen.svg" alt="Nielsen Design" width="220" height="160"></div>
  <div class="brandfeat__body">
    <h2>Nielsen Design, notre fournisseur de référence</h2>
    <p>Fort d'une expérience de plus de 30 ans dans l'encadrement, Nielsen réunit une équipe de passionnés qui conçoit chaque jour des baguettes et des cadres. Certification FSC®, fabrication allemande. Nous sommes revendeur Nielsen à Luxembourg : configurateur en ligne et Click &amp; Collect à Hollerich, souvent dans l'heure.</p>
    <p>Quand le format sort du catalogue, nous restons dans le même atelier : sur-mesure, museum, restauration.</p>
  </div>
</div>
<h2 class="p-h2 reveal">Ils nous recommandent</h2>
<p class="p-sub reveal">Un réseau d'encadreurs indépendants, de Bordeaux à Paris, nous adresse des clients de passage au Luxembourg. Nous travaillons dans le même esprit : conseil à l'atelier, pas de cadre anonyme de grande surface. Si vous venez d'une de ces maisons, dites-le-nous : nous reprenons le fil du conseil sans tout recommencer.</p>
{partner_strip(partners)}
</div>'''
hist_body = hist_body.replace('<div class="hist-end">', partners_block + '\n<div class="hist-end">', 1)

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
def gal_group(title, items, eager_n=0):
    cells = "".join(
        f'<figure class="g-cell reveal"><div class="g-frame"><img src="{src}" '
        f'alt="{e(cap)}" loading="{"eager" if i < eager_n else "lazy"}"></div>'
        f'<figcaption class="g-cap">{e(cap)}</figcaption></figure>'
        for i, (src, cap) in enumerate(items))
    return f'<h2 class="p-h2 reveal">{e(title)}</h2><div class="g-grid">{cells}</div>'


galerie_body = f'''<section id="gal" class="section"><div class="p-w">
<span class="p-eyebrow">Notre galerie</span>
<h1 class="p-h1">Galerie d'art et réalisations encadrées</h1>
{gal_group("Contemporain, pop-art et street-art", GAL_ITEMS[0:8], eager_n=3)}
{gal_group("Photographie, papier et museum", GAL_ITEMS[8:16])}
{gal_group("Intérieurs et montages classiques", GAL_ITEMS[16:24])}
<div class="g-cta reveal">{btn_orange("Prendre rendez-vous", "contact.html")} {btn_plain("Encadrement sur mesure", "encadrement-sur-mesure.html")}</div>
</div></section>'''

# ================= CONTACT =================
contact_body = f'''<section id="contact" class="section"><div class="p-w">
<span class="p-eyebrow">Nous trouver</span>
<h1 class="p-h1">Contact · Art'Cadres Luxembourg</h1>
<div class="c-lead reveal-in"><p>Encadrement, restauration, cadres Nielsen ou devis institutionnel : un seul atelier, à Hollerich, au cœur de Luxembourg-Ville.</p></div>
<div class="c-grid reveal-in">
  <div>
    <div class="c-info">
      <div class="c-row"><p class="c-lab">Téléphone</p><div class="c-val"><p><a href="tel:+35227849488" style="text-decoration:none;color:inherit">+352 27 84 94 88</a></p></div></div>
      <div class="c-row"><p class="c-lab">E-mail</p><div class="c-val"><p><a href="mailto:contact@artcadres.lu" style="text-decoration:none;color:inherit">contact@artcadres.lu</a></p></div></div>
      <div class="c-row"><p class="c-lab">Adresse</p><div class="c-val"><p>2 bis rue de la toison d'or<br>L-2342 Luxembourg (Hollerich)</p></div></div>
      <div class="c-row"><p class="c-lab">Horaires</p><div class="c-val"><p>Mercredi au samedi<br>de 10 h à 18 h</p></div></div>
    </div>
    <div class="c-book">{btn_orange("Prendre rendez-vous", "tel:+35227849488")} {btn_plain("Écrire un e-mail", "mailto:contact@artcadres.lu", arrow=False)}</div>
    <div class="c-note"><p>Nous répondons sous 48 h ouvrées. Pour un rendez-vous, appelez-nous ou écrivez-nous directement. Merci d'indiquer le format de l'œuvre si vous le connaissez déjà, ainsi que s'il s'agit d'un encadrement, d'une restauration ou d'un projet d'entreprise.</p></div>
  </div>
  <aside class="c-kathia">
    <figure>
      <div class="p-frame"><img src="assets/kathia-solo.jpg" alt="Kathia Neumann, fondatrice d'Art'Cadres Luxembourg" width="800" height="1000" loading="eager" draggable="false"></div>
      <figcaption>
        <h3>Kathia Neumann</h3>
        <p class="c-founder__role">Fondatrice · Encadreur d'art</p>
        <p>Plus de trente ans d'expérience dans l'encadrement d'art. Kathia Neumann perpétue à Luxembourg un savoir-faire né à Metz en 1972, avec la même exigence artisanale.</p>
      </figcaption>
    </figure>
  </aside>
</div>
<div class="c-zone reveal">
  <h2 class="p-h2">Luxembourg-Ville, Hollerich, Howald</h2>
  <p>L'atelier est à Hollerich : 2 bis rue de la toison d'or, L-2342. Rendez-vous mercredi au samedi, 10 h à 18 h. Pose des grands formats dans un rayon d'environ 25 km.</p>
</div>
<div class="c-map reveal">
  <iframe title="Carte Art'Cadres Luxembourg, Hollerich" src="https://maps.google.com/maps?q=2+bis+rue+de+la+toison+d%27or,+L-2342+Luxembourg&amp;hl=fr&amp;z=16&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
</div>
</div></section>'''

# ================= CONFIGURATEUR =================
CFG_URL = "https://nielsen.oxyz.studio/project/new/3b83739c106fa33d171be9a151d26ab9/app"
configurateur_body = f'''<section id="cfg">
<div class="cfg-inner">
  <div class="cfg-head reveal-in">
    <p class="cfg-eyebrow">Sur mesure, en ligne</p>
    <h1 class="cfg-title">Configurateur cadre en ligne · Luxembourg</h1>
    <p class="cfg-intro">Le configurateur Nielsen calcule un devis cadre en ligne pour les formats courants. Baguette, passe-partout, verre : le prix s'affiche tout de suite. Retrait Click &amp; Collect à Hollerich, souvent dans l'heure.</p>
  </div>
  <div class="cfg-stage cfg-stage--crop reveal">
    <div class="cfg-skeleton" aria-hidden="true"></div>
    <iframe class="cfg-frame" src="{CFG_URL}" title="Configurateur d'encadrement sur mesure" loading="lazy" allow="clipboard-write; fullscreen" referrerpolicy="strict-origin-when-cross-origin" onload="var s=this.parentNode.querySelector('.cfg-skeleton'); if(s) s.style.display='none';"></iframe>
  </div>
  <p class="cfg-fallback">Le configurateur ne s'affiche pas ? <a href="{CFG_URL}" target="_blank" rel="noopener">Ouvrez-le dans un nouvel onglet</a>.</p>
  <div class="cfg-seo reveal">
    <h2>À qui s'adresse le devis en ligne</h2>
    <p>Pour les formats courants Nielsen, bois ou aluminium. Vous choisissez baguette, passe-partout et verre : le tarif s'affiche au fur et à mesure. Aucun engagement tant que vous ne validez pas.</p>
    <p>Click &amp; Collect à Hollerich, 2 bis rue de la toison d'or, souvent dans l'heure. Pas d'envoi postal. Pose sur site dans un rayon de 25 km : à part, sur devis.</p>
  </div>
  <div class="cfg-seo reveal">
    <h2>Quand venir à l'atelier</h2>
    <p>Le configurateur ne gère pas les objets, médailles, textiles, papiers fragiles ni les formats hors catalogue. Marie-Louise, caisse américaine, verre museum, restauration : rendez-vous à Hollerich, mercredi au samedi, 10 h à 18 h.</p>
    <p>Série d'entreprise ou pose monumentale : page institutions et page grands formats. Un montage museum ou une pose s'ajoute à l'atelier, sur devis.</p>
  </div>
  {faq_section("Questions configurateur", [
    ("Le prix affiché est-il le prix final ?",
     "Pour les options choisies dans le configurateur Nielsen, oui. Pose sur site, museum, objet ou format hors catalogue s'ajoutent à l'atelier."),
    ("Livrez-vous à domicile ?",
     "Le Click & Collect se retire à Hollerich. Pas d'envoi postal. La pose dans un rayon de 25 km se facture à part."),
    ("Le configurateur voit-il mon œuvre ?",
     "Non. L'iframe calcule un cadre. L'œuvre, son grain et son relief se regardent à l'atelier."),
  ])}
  <div class="cfg-foot reveal">{btn_orange("Une question ? Contactez-nous", "contact.html")}</div>
</div>
</section>'''

# ================= GRANDS FORMATS =================
FAQ_GF = [
    ("Jusqu'à quelle taille encadrez-vous ?",
     "Jusqu'aux panneaux muraux de plusieurs mètres, du type installation Deloitte. Au-delà du catalogue Nielsen, tout passe par l'atelier : châssis, verre ou plexi, pose à deux."),
    ("La pose est-elle incluse ?",
     "La pose sur site se chiffre à part, dans un rayon d'environ 25 km, plus loin pour les comptes suivis. Un particulier collectionneur et une entreprise passent par le même planning."),
    ("Particuliers ou seulement les entreprises ?",
     "Les deux. La page institutions détaille Deloitte, Accor, SES, BnL, Cour. Cette page s'adresse aussi aux artistes et aux collectionneurs."),
]
gf_body = f'''<section class="section"><div class="p-w">
{content_hero("Grands formats", "Encadrement grand format au Luxembourg",
"<p>Des médailles aux panneaux de plusieurs mètres : nous encadrons et installons sur site. Le grand format n'est pas un cadre agrandi. Il demande un châssis calculé, un verre ou un plexi adapté, et une pose à deux.</p>",
"assets/kathia-grand-format.jpg", "Kathia Neumann installe une œuvre grand format", eager_img=True)}
{icon_row([("size", "Du petit au monumental", "Médailles, maillots, toiles, panneaux muraux."), ("shield", "Pose sur site", "Rayon d'environ 25 km, plus loin pour les comptes suivis."), ("bag", "Entreprises et particuliers", "Même atelier, devis et planning dédiés.")])}
{content_story("Ce que le catalogue ne fait pas", [
    "Un cadre Nielsen se retire en une heure quand le format entre dans la grille. Un panneau de deux ou trois mètres, un triptyque, une photographie monumentale pour un hall : le configurateur s'arrête. Nous prenons les cotes sur place ou à l'atelier, nous dessinons le montage, nous fabriquons, nous accrochons.",
    "Deloitte nous a confié des panneaux muraux. La Bibliothèque nationale, des grands formats en situ. Accor, des séries hôtelières. La Cour grand-ducale, plus de 200 portraits officiels. Ces chantiers ont appris à l'atelier le rythme d'un siège, d'un hall, d'un palais : discrétion, planning, pièces de rechange.",
    "Les particuliers et les artistes passent par la même table. Une toile hors norme, une photographie de voyage en très grand, une collection à accrocher d'un seul tenant : nous venons voir le mur. Howald, Kirchberg, Hollerich, et un rayon d'environ 25 km autour de Luxembourg-Ville.",
])}
<div class="p-list reveal">{content_list("Étude, fabrication, pose", [
    ("Relevé", "Cotes du mur, contraintes (spots, climatisation, vitrage). Photos du lieu si vous ne pouvez pas vous déplacer tout de suite."),
    ("Montage", "Châssis, baguette, fond, verre ou plexi. Le poids et la dilatation ne sont pas ceux d'un 40 × 50."),
    ("Pose", "À deux, sur rendez-vous. Facture entreprise possible. Confidentialité pour les sièges."),
])}</div>
<h3 class="p-objh reveal">Du plus petit au plus grand</h3>
<div class="p-objs reveal">{gf_objs_html}</div>
{faq_section("Questions grands formats", FAQ_GF)}
<div class="p-cta reveal">{btn_orange("Demander un devis grand format", "contact.html")} {btn_plain("Institutions & entreprises", "institutions-entreprises.html")}</div>
</div></section>'''

# ================= GLOSSAIRE =================
GLOSS = [
    ("Passe-partout",
     "Carton percé qui entoure l'œuvre dans le cadre. En conservation, il est PH neutre (sans acide) pour ne pas jaunir le papier. La fenêtre se coupe au format du sujet, avec une marge choisie."),
    ("Marie-Louise",
     "Passe-partout haut de gamme, souvent biseauté. Le biseau crée une ombre et une profondeur autour du sujet. Montage traditionnel comme contemporain."),
    ("Caisse américaine",
     "Cadre dans lequel l'œuvre flotte, en léger retrait, sans passe-partout. Très demandée pour l'art contemporain et la photographie. L'œuvre ne touche pas le verre."),
    ("Rehausse",
     "Entretoise qui tient le verre au-dessus d'un sujet en volume (objet, médaille, textile). Sans rehausse, le verre écrase le relief."),
    ("Montage museum",
     "Ensemble de choix de conservation : carton sans acide, charnières adaptées, verre anti-UV, parfois dos clos. Vise le temps long, pas l'effet décoratif seul."),
    ("Verre anti-reflet",
     "Verre traité pour atténuer les reflets d'une fenêtre ou d'un spot. Confort visuel. Le filtrage UV dépend de la gamme, ce n'est pas automatique."),
    ("Verre musée (museum)",
     "Verre de conservation : filtrage UV élevé (souvent jusqu'à 99 %) et reflets très faibles. Indiqué pour aquarelles, photographies, pièces à transmettre."),
    ("PH neutre / sans acide",
     "Qualité d'un carton qui ne dégage pas d'acide dans le temps. Un passe-partout bas de gamme jaunit et attaque le papier. Nous n'en posons pas sur une œuvre à conserver."),
    ("Baguette / moulure",
     "Le profil du cadre, en bois, en aluminium ou en pâte. Nielsen propose quatre univers. L'atelier ajoute les moulures hors catalogue, y compris l'or."),
    ("Dorure à la feuille",
     "Pose de feuille d'or (apprêts, bol, brunissoir). Ce n'est pas une peinture métallisée. Cadres, miroirs, consoles, statues."),
    ("Click & Collect",
     "Commande Nielsen en ligne, retrait à l'atelier Hollerich, souvent dans l'heure. Pas d'envoi postal."),
    ("Agrément monuments historiques",
     "Reconnaissance officielle de compétence pour restaurer le patrimoine classé. Sylvie Schied le détient. Méthode, pas retouche décorative."),
]
gloss_dl = "".join(
    f'<div class="gloss-item"><dt>{e(t)}</dt><dd>{e(d)}</dd></div>' for t, d in GLOSS)
gloss_body = f'''<section class="section"><div class="p-w">
{content_hero("Lexique", "Glossaire de l'encadrement",
"<p>Les mots que nous employons à l'atelier, expliqués sans jargon inutile. Chaque définition renvoie au geste réel : Hollerich, cartons PH neutre, verre musée, dorure à la feuille.</p>",
"", "", solo=True)}
<dl class="gloss reveal">{gloss_dl}</dl>
<div class="p-cta reveal">{btn_orange("En parler à l'atelier", "contact.html")} {btn_plain("Encadrement sur mesure", "encadrement-sur-mesure.html")} {btn_plain("Restauration", "dorures-restauration.html")}</div>
</div></section>'''

# ================= ÉCRITURE =================
INDEX_LD = schema_local() + "\n  " + schema_faq(FAQ_HOME)
CONTACT_LD = schema_local() + "\n  " + schema_contact_page()
INST_LD = (
    schema_institutions_page() + "\n  "
    + schema_service(
        "Encadrement institutions et entreprises",
        "Encadrement B2B, grands formats et pose sur site au Luxembourg. Deloitte, Accor, SES, Bibliothèque nationale, Cour grand-ducale.",
        "institutions-entreprises.html",
    )
)
MESURE_LD = schema_service(
    "Encadrement sur mesure",
    "Encadrement d'art sur mesure à Luxembourg : Marie-Louise, caisse américaine, rehausse, objets et grands formats. Atelier Hollerich.",
    "encadrement-sur-mesure.html",
) + "\n  " + schema_faq(FAQ_MESURE)
STANDARD_LD = schema_service(
    "Cadres Nielsen",
    "Cadres standards Nielsen bois et aluminium à Luxembourg. FSC, fabriqués en Allemagne. Click & Collect en 1 h à Hollerich.",
    "encadrement-standard.html",
) + "\n  " + schema_faq(FAQ_STANDARD)
DORURES_LD = schema_service(
    "Restauration de tableaux et dorure",
    "Restauration de tableaux et dorure à la feuille à Luxembourg, avec Sylvie Schied, agréée monuments historiques.",
    "dorures-restauration.html",
) + "\n  " + schema_faq(FAQ_DORURES)
CFG_LD = schema_service(
    "Devis cadre en ligne Nielsen",
    "Configurateur d'encadrement sur mesure : baguette Nielsen, passe-partout, verre. Prix calculé en direct, retrait Click & Collect à Hollerich.",
    "configurateur.html",
)
GAL_LD = schema_images(GAL_ITEMS)
GF_LD = schema_service(
    "Encadrement grand format",
    "Encadrement et pose de grands formats au Luxembourg : panneaux muraux, triptyques, collections. Atelier Hollerich, pose sur site.",
    "encadrement-grand-format.html",
) + "\n  " + schema_faq(FAQ_GF)

PAGES = [
    ("index.html", "Encadreur d'art à Luxembourg · Art'Cadres",
     "Encadreur d'art à Hollerich : sur mesure, cadres Nielsen, dorure, restauration agréée MH. Institutions Deloitte, Accor, SES. Devis en ligne.",
     accueil_body, "index.html", None, INDEX_LD),
    ("institutions-entreprises.html", "Encadrement entreprises Luxembourg · Art'Cadres",
     "Encadrement B2B au Luxembourg : Deloitte, Accor, SES, Bibliothèque nationale, Cour grand-ducale. Grands formats et installation sur site.",
     institutions_body, "institutions-entreprises.html", SITE_URL + "/assets/histoire-atelier-2.jpg", INST_LD),
    ("notre-histoire.html", "Notre histoire : un savoir-faire depuis 1972 · Art'Cadres",
     "Art'Cadres Luxembourg perpétue un savoir-faire d'encadrement né en 1972 : sur mesure, restauration, dorure et galerie d'art à Hollerich.",
     hist_body, "notre-histoire.html", None, None),
    ("encadrement-sur-mesure.html", "Encadrement sur mesure Luxembourg · Art'Cadres",
     "Encadrement d'art sur mesure à Luxembourg : Marie-Louise, caisse américaine, rehausse, objets et grands formats. Atelier Hollerich.",
     mesure_body, "encadrement-sur-mesure.html", None, MESURE_LD),
    ("encadrement-standard.html", "Cadres Nielsen Luxembourg · Art'Cadres",
     "Cadres standards Nielsen bois et aluminium à Luxembourg. FSC, fabriqués en Allemagne. Devis instantané et retrait en 1 h à Hollerich.",
     standard_body, "encadrement-standard.html", None, STANDARD_LD),
    ("dorures-restauration.html", "Restauration tableau Luxembourg · Art'Cadres",
     "Restauration de tableaux et dorure à la feuille à Luxembourg. Diagnostic, agrément monuments historiques, patrimoine familial.",
     dorures_body, "dorures-restauration.html", None, DORURES_LD),
    ("notre-galerie.html", "Galerie d'art encadrée Luxembourg · Art'Cadres",
     "Galerie Art'Cadres Luxembourg : œuvres encadrées sur mesure, pop-art, photographies et pièces de collection.",
     galerie_body, "notre-galerie.html", SITE_URL + "/assets/gal-01.jpg", GAL_LD),
    ("encadrement-grand-format.html", "Encadrement grand format Luxembourg · Art'Cadres",
     "Encadrement grand format à Luxembourg : panneaux muraux, pose sur site, particuliers et institutions. Atelier Hollerich.",
     gf_body, "encadrement-grand-format.html", SITE_URL + "/assets/kathia-grand-format.jpg", GF_LD),
    ("glossaire-encadrement.html", "Glossaire de l'encadrement · Art'Cadres Luxembourg",
     "Passe-partout, Marie-Louise, caisse américaine, verre musée, dorure à la feuille : le lexique de l'atelier Art'Cadres à Hollerich.",
     gloss_body, "glossaire-encadrement.html", None, None),
    ("contact.html", "Contact Hollerich · Art'Cadres Luxembourg",
     "Contactez Art'Cadres : 2 bis rue de la toison d'or, L-2342 Luxembourg. Tél. +352 27 84 94 88. Rendez-vous avec Kathia Neumann.",
     contact_body, "contact.html", SITE_URL + "/assets/kathia-portrait.jpg", CONTACT_LD),
    ("configurateur.html", "Devis cadre en ligne Luxembourg · Art'Cadres",
     "Composez votre cadre sur mesure en ligne : baguette Nielsen, passe-partout, verre. Prix en direct, retrait Click & Collect 1 h.",
     configurateur_body, "configurateur.html", None, CFG_LD),
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
    f.write(
        "User-agent: *\nAllow: /\n"
        "User-agent: GPTBot\nAllow: /\n"
        "User-agent: ClaudeBot\nAllow: /\n"
        "User-agent: PerplexityBot\nAllow: /\n"
        "User-agent: Google-Extended\nAllow: /\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
print("écrit : robots.txt")

with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(f"""# Art'Cadres Luxembourg
> Encadreur d'art à Luxembourg (Hollerich). Un savoir-faire depuis 1972.

## Pages principales
- {SITE_URL}/ — Encadreur d'art, institutions, grands formats
- {SITE_URL}/institutions-entreprises.html — B2B Deloitte, Accor, SES, BNL
- {SITE_URL}/encadrement-sur-mesure.html — Sur mesure artisanal
- {SITE_URL}/encadrement-standard.html — Cadres Nielsen
- {SITE_URL}/dorures-restauration.html — Restauration & dorure, Sylvie Schied agréée MH
- {SITE_URL}/encadrement-grand-format.html — Grands formats et pose sur site
- {SITE_URL}/glossaire-encadrement.html — Lexique (passe-partout, Marie-Louise, verre musée)
- {SITE_URL}/notre-galerie.html — Galerie et réalisations
- {SITE_URL}/notre-histoire.html : savoir-faire depuis 1972, partenaires Nielsen
- {SITE_URL}/configurateur.html — Devis en ligne Nielsen
- {SITE_URL}/contact.html — Rendez-vous Hollerich

## Contact
contact@artcadres.lu · +352 27 84 94 88
2 bis rue de la toison d'or, L-2342 Luxembourg
""")
print("écrit : llms.txt")

open(os.path.join(OUT, ".nojekyll"), "w").close()
print("écrit : .nojekyll")

INDEXNOW_KEY = "e8c4a91b7d2f46c0a3e5b8d1f6a9c247"
with open(os.path.join(OUT, INDEXNOW_KEY + ".txt"), "w", encoding="utf-8") as f:
    f.write(INDEXNOW_KEY)
print("écrit :", INDEXNOW_KEY + ".txt")

err404 = page(
    "Page introuvable · Art'Cadres Luxembourg",
    "Cette page n'existe pas. Retour à l'atelier Art'Cadres, Hollerich.",
    '''<section class="section"><div class="p-w">
<span class="p-eyebrow">Erreur 404</span>
<h1 class="p-h1">Cette page n'existe pas</h1>
<div class="p-lead"><p>Le lien est ancien, ou l'adresse a changé. L'atelier est toujours à Hollerich : encadrement, restauration, Nielsen, rendez-vous.</p></div>
<div class="p-cta reveal">'''
    + btn_orange("Prendre rendez-vous", "contact.html")
    + " "
    + btn_plain("Retour à l'accueil", "index.html")
    + "</div></div></section>",
    "404.html",
)
err404 = err404.replace('content="index, follow"', 'content="noindex, follow"', 1)
with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
    f.write(err404)
print("écrit : 404.html")

with open(os.path.join(OUT, "partenaires.html"), "w", encoding="utf-8") as f:
    f.write(f'''<!DOCTYPE html>
<html lang="fr-LU">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{SITE_URL}/notre-histoire.html">
  <meta http-equiv="refresh" content="0;url=notre-histoire.html#partenaires">
  <title>Partenaires · Art'Cadres Luxembourg</title>
  <script>location.replace("notre-histoire.html#partenaires");</script>
</head>
<body>
  <p><a href="notre-histoire.html#partenaires">Nos partenaires se trouvent sur Notre histoire.</a></p>
</body>
</html>
''')
print("écrit : partenaires.html (redirection)")

print("OK,", len(PAGES), "pages générées + 404.")
