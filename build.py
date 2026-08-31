#!/usr/bin/env python3
"""Generateur du site statique Art'Cadres Luxembourg.
Produit des fichiers .html autonomes (header/footer partages) a cote de ce script.
Lancer :  python3 build.py
"""
import html
import os

OUT = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("Accueil", "index.html"),
    ("Sur mesure", "encadrement-sur-mesure.html"),
    ("Cadres standards", "encadrement-standard.html"),
    ("Dorure & restauration", "dorures-restauration.html"),
    ("Galerie", "notre-galerie.html"),
    ("Histoire", "notre-histoire.html"),
    ("Partenaires", "partenaires.html"),
    ("Contact", "contact.html"),
]
CTA = ("Devis en ligne", "configurateur.html")

ARROW = ('<span class="arw"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/>'
         '</svg></span>')


def e(s):
    return html.escape(s, quote=True)


def btn(label, href, cls="btn"):
    tgt = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return f'<a class="{cls}" href="{href}"{tgt}>{e(label)} {ARROW}</a>'


def header(active):
    links = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += f'<a href="{href}"{cur}><span>{e(label)}</span></a>'
    cur = ' aria-current="page"' if CTA[1] == active else ""
    links += f'<a class="cta" href="{CTA[1]}"{cur}><span>{e(CTA[0])}</span></a>'
    return f'''<div class="announce"><a href="contact.html">Votre artisan encadreur vous accueille sur rendez-vous.</a></div>
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
    parts = ["Encadrement sur mesure", "Restauration de tableaux",
             "Click &amp; Collect en 1h", "Devis instantané en ligne"]
    seq = "".join(f'<span>{p}</span><span class="sep">·</span>' for p in parts)
    track = seq * 2
    return f'''<section class="marquee" aria-hidden="true"><div class="marquee__track">{track}</div></section>
<section class="trust"><div class="trust__grid">
  <div><h4>Click &amp; Collect en 1h</h4><p>Retrait à l'atelier, à Hollerich.</p></div>
  <div><h4>Devis instantané</h4><p>Votre prix en ligne, via le configurateur.</p></div>
  <div><h4>Sur mesure &amp; grands formats</h4><p>Des petits cadres aux très grandes pièces.</p></div>
  <div><h4>Restauration de tableaux</h4><p>Diagnostic et devis personnalisés.</p></div>
</div></section>
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
      <a href="configurateur.html">Devis en ligne</a>
    </div></div>
    <div class="fcol"><h3>Explorer</h3><div class="flinks">
      <a href="index.html">Accueil</a>
      <a href="notre-histoire.html">Notre histoire</a>
      <a href="notre-galerie.html">Notre galerie</a>
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
  <div class="footer-bottom">© 2026 Art'Cadres Luxembourg. Maison Neumann depuis 1972.</div>
</div></footer>'''


def page(title, description, body, active):
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
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
def content_list(title, items):
    lis = "".join(f'<li><span class="t">{e(t)}</span><span class="d">{e(d)}</span></li>'
                  for t, d in items)
    h = f'<h3 class="p-listh">{e(title)}</h3>' if title else ""
    return f'{h}<ul>{lis}</ul>'


def strip(imgs, cols):
    cells = "".join(f'<div class="p-scell"><div class="p-frame"><img src="{s}" alt="" '
                    f'loading="lazy"></div></div>' for s in imgs)
    return f'<div class="p-strip strip-{cols} reveal">{cells}</div>'


def content_hero(eyebrow, heading, lead_html, image, caption, solo=False):
    if solo:
        fig = ""
    else:
        cap = f'<figcaption class="p-cap">{e(caption)}</figcaption>' if caption else ""
        fig = (f'<figure class="reveal" style="--d:120ms"><div class="p-frame">'
               f'<img src="{image}" alt="{e(heading)}" loading="lazy"></div>{cap}</figure>')
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


# ================= ACCUEIL =================
services = [("01", "Cadres standards", "Aluminium ou bois, prêts à l'emploi."),
            ("02", "Cadres sur mesure", "Conçus selon vos goûts et votre œuvre."),
            ("03", "Tirage photo", "Petits et grands formats."),
            ("04", "Click & Collect", "Prêt en 1h, à emporter à l'atelier.")]
svc_html = "".join(f'<div class="p-svc"><span class="n">{n}</span><h3>{e(t)}</h3>'
                   f'<p>{e(d)}</p></div>' for n, t, d in services)

conf_logos = [
    ("D", "Deloitte", "Œuvres & grand format"),
    ("A", "Accor", "ibis Styles, Mercure, MGallery"),
    ("SES", "SES", "Fournisseur sur site"),
    ("CG", "Cour grand-ducale", "200+ portraits officiels"),
    ("BnL", "Bibliothèque nationale", "Grand format en situ"),
    ("MH", "Maison Heler", "Hôtel signé Philippe Starck"),
    ("SK", "SODIKART", "Maillots & pièces signés"),
    ("MC", "M.Chat", "Avec Thoma Vuille"),
]
conf_hl = [
    ("ref-courducale", "Cour grand-ducale", "Plus de 200 portraits officiels"),
    ("ref-maisonheler", "Maison Heler, Metz", "Le bar de l'hôtel signé Philippe Starck"),
    ("ref-mchat", "M.Chat", "Collaboration avec l'artiste Thoma Vuille"),
]
conf_hl_html = "".join(
    f'<figure class="p-scell"><div class="p-frame"><img src="assets/{s}.jpg" '
    f'alt="{e(n)}" loading="lazy"></div><figcaption class="p-cap">{e(n)}. {e(d)}.'
    f'</figcaption></figure>' for s, n, d in conf_hl)

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

accueil_body = f'''<section id="acc">
<div class="p-herobg" style="background-image:url(assets/ac-accueil.jpg);">
  <div class="p-hw">
    <span class="p-eyebrow">Art'Cadres · Luxembourg</span>
    <h1 class="p-h1">Encadreur d'art à Luxembourg</h1>
    <div class="p-lead"><p>L'encadrement sur mesure, les cadres standards, le tirage photo, la restauration de tableaux, la dorure et une galerie d'art, réunis en un même lieu, à Hollerich.</p></div>
    <div class="p-btns">{btn("Composer votre cadre en ligne", "configurateur.html")}<a class="btn2" href="notre-histoire.html">Découvrir l'atelier</a></div>
  </div>
</div>
<div class="p-w">
  <div class="p-services reveal">{svc_html}</div>
  <div class="p-story reveal">
    <div class="p-intro"><h2>Un savoir-faire transmis depuis 1972</h2><div class="p-body"><p>La Maison Neumann encadre et restaure à Metz depuis 1972. Après plus de 30 ans d'expérience, Kathia Neumann a souhaité développer ce savoir-faire au-delà des frontières en créant une antenne à Luxembourg.</p><p>Particuliers, artistes, collectionneurs, architectes, décorateurs et institutions y trouvent un accompagnement personnalisé, du petit cadre aux très grandes pièces.</p></div></div>
    <figure><div class="p-frame"><img src="assets/histoire-mchat.jpg" alt="Un savoir-faire transmis depuis 1972" loading="lazy"></div></figure>
  </div>
  <div class="p-cta reveal"><h2>Votre devis, tout de suite</h2><p>Composez votre cadre en ligne et obtenez un prix instantané, sans engagement.</p>{btn("Ouvrir le configurateur", "configurateur.html")}</div>
</div>
</section>
<section id="conf" class="section"><div class="p-w">
<h2 class="p-h2 reveal">Des institutions, des marques et des artistes nous confient leurs œuvres</h2>
{logo_wall(conf_logos)}
<div class="p-strip strip-3 reveal" style="margin-top:clamp(40px,5vw,60px)">{conf_hl_html}</div>
</div></section>
<section id="gf" class="section"><div class="p-w">
<div class="p-feat reveal">
  <div><div class="big">≈ 3 m</div><h2>Du petit cadre au format monumental</h2><p>Nous encadrons et installons sur site des œuvres de très grandes dimensions, jusqu'à environ 3 mètres, comme ce panneau mural réalisé pour les bureaux de Deloitte.</p></div>
  <div class="p-imgs"><div class="p-fr"><img src="assets/gf-deloitte-1.jpg" alt="Œuvre grand format installée sur site" loading="lazy"></div><div class="p-fr"><img src="assets/gf-deloitte-2.jpg" alt="Panneau mural monumental" loading="lazy"></div></div>
</div>
<h3 class="p-objh reveal">On peut tout encadrer</h3>
<div class="p-objs reveal">{gf_objs_html}</div>
</div></section>
<section id="avis" class="section"><div class="p-w">
<h2 class="p-h2 reveal">Ils nous ont fait confiance, ils en parlent</h2>
<div class="p-badges reveal">
  <div class="p-badge"><span class="v">4,9/5</span><span class="s">★★★★★</span><span class="m">88 avis vérifiés, Art'Cadres Luxembourg</span></div>
</div>
<div class="p-avis reveal">{avis_cards}</div>
</div></section>'''

# ================= NOTRE HISTOIRE =================
hist_body = f'''<section class="section"><div class="p-w">
{content_hero("Art'Cadres · Luxembourg", "Notre histoire", "<p>Art'Cadres Luxembourg réunit en un même lieu l'encadrement sur mesure, la restauration de tableaux, la dorure et une galerie d'art. Un espace unique où savoir-faire artisanal, conseil personnalisé et passion de l'art se rencontrent.</p>", "assets/ac-histoire.jpg", "L'atelier Art'Cadres, au cœur de Luxembourg-Ville")}
{content_story("L'excellence de l'encadrement sur mesure", ["Chez Art'Cadres Luxembourg, chaque œuvre mérite une présentation à la hauteur de son histoire, de sa valeur et de son caractère.", "Forte de plus de 30 années d'expérience, Kathia Neumann met son expertise artisanale et son regard esthétique au service de créations entièrement sur mesure. Chaque projet fait l'objet d'une étude attentive, pour un encadrement en parfaite harmonie avec l'œuvre, son environnement et la sensibilité de son propriétaire.", "Moulures contemporaines ou classiques, finitions raffinées, verres de protection, passe-partout et techniques traditionnelles : chaque détail est sélectionné avec exigence pour donner naissance à une pièce unique."])}
<div class="p-list reveal">{content_list("Nos métiers réunis en un même lieu", [("Encadrement sur mesure", "Baguette, passe-partout et verre choisis pour sublimer chaque œuvre."), ("Restauration de tableaux", "Conservation et remise en valeur des pièces anciennes."), ("Dorure à la feuille", "Cadres, miroirs et objets dorés selon les techniques traditionnelles."), ("Galerie d'art", "Une collection coup de cœur, encadrée et mise en lumière.")])}</div>
{strip(["assets/histoire-mchat.jpg", "assets/histoire-atelier-1.jpg", "assets/histoire-atelier-2.jpg"], 3)}
<figure class="p-quote reveal"><blockquote>« Chaque œuvre mérite une présentation à la hauteur de son histoire. »</blockquote><figcaption>Kathia Neumann, Art'Cadres Luxembourg</figcaption></figure>
<div class="p-note reveal"><p>Particuliers, artistes, collectionneurs, architectes, décorateurs, entreprises et institutions bénéficient d'un accompagnement confidentiel, personnalisé et exigeant.</p></div>
<div class="p-cta reveal">{btn("Prendre rendez-vous", "contact.html")}</div>
</div></section>'''

# ================= ENCADREMENT SUR MESURE =================
mesure_body = f'''<section class="section"><div class="p-w">
{content_hero("Sur mesure", "Encadrement sur mesure au Luxembourg", "<p>L'encadrement d'art est avant tout de l'artisanat, et il existe des centaines de possibilités. L'originalité et la subtilité de l'encadrement font toute la différence dans la mise en valeur de vos œuvres.</p>", "assets/ac-mesure.jpg", "Encadrement sur mesure à l'atelier")}
{content_story("Mettre l'œuvre en valeur, selon votre budget", ["Notre objectif principal est la mise en valeur de l'œuvre, en tenant compte de la sensibilité de chacun, avec un budget adapté grâce à une gamme étendue de moulures tous styles, du contemporain au classique.", "Styles de nos moulures : modernes, noir, blanc, chêne, or, wengé, gris, couleurs."])}
<div class="p-list reveal">{content_list("Quelques techniques du sur-mesure", [("La Marie-Louise biseautée", "Le haut de gamme du passe-partout : elle crée une profondeur sur vos sujets, montage traditionnel et moderne à la fois."), ("La caisse américaine", "Le type d'encadrement le plus répandu au monde : une mise en valeur par effet de suspension, l'œuvre flotte dans le cadre."), ("La technique de rehausse", "Un sujet, un verre de protection, une moulure et une rehausse pour que le verre soit en suspension au-dessus du sujet.")])}</div>
<div class="p-list p-list2 reveal">{content_list("Les baguettes Nielsen, 4 univers", [("Nature", "Bois naturel, massif et placage."), ("Color", "Un monde tout en couleur : vives ou pastel, mates ou brillantes."), ("Design", "Des lignes pures, associées à des finitions sobres ou métallisées."), ("Charme", "L'univers des dorures, des patines à l'ancienne et des finitions blanchies.")])}</div>
{strip(["assets/ac-mesure-1.jpg", "assets/ac-mesure-2.jpg", "assets/ac-mesure-3.jpg"], 3)}
<div class="p-cta reveal">{btn("Composer votre cadre en ligne", "configurateur.html")}</div>
</div></section>'''

# ================= ENCADREMENT STANDARD =================
standard_body = f'''<section class="section"><div class="p-w">
{content_hero("Cadres standards", "Les cadres Nielsen", "<p>Une qualité qui fait la différence : tous les cadres Nielsen, en aluminium comme en bois, sont réalisés avec des matériaux de grande qualité.</p>", "assets/ac-standard.jpg", "Cadres Nielsen, bois et aluminium")}
<div class="p-list reveal">{content_list("Une qualité qui fait la différence", [("Les cadres bois", "Des dorés aux couleurs vives en passant par les bois bruts : une large palette de styles."), ("Les cadres aluminium", "Simples à charger, démonter et remonter ; tournettes rivetées sur dos MDF, verre minéral 2 mm à chants polis, aucun risque de blessure."), ("Conçus par Nielsen Design", "La certification FSC garantit une gestion responsable des forêts. La plupart de nos cadres bois sont éco-responsables."), ("Fabriqués en Allemagne", "Nielsen, marque de référence de l'encadrement : une expertise sur le cadre, le verre et le contrecollé.")])}</div>
{strip(["assets/ac-standard-1.jpg", "assets/ac-standard-2.jpg"], 2)}
<div class="p-cta reveal">{btn("Composer votre cadre en ligne", "configurateur.html")}</div>
</div></section>'''

# ================= DORURES & RESTAURATION =================
dorures_body = f'''<section class="section"><div class="p-w">
{content_hero("Dorure & restauration", "Redonnez vie à vos œuvres d'art", "<p>Le temps laisse son empreinte : vernis jaunis, salissures, poussière, petites déchirures ou altérations peuvent ternir la beauté d'un tableau ancien.</p>", "assets/ac-dorures.jpg", "Restauration d'un tableau à l'atelier")}
{content_story("La préservation de votre patrimoine", ["Chez Art'Cadres, nous vous accompagnons dans la préservation de votre patrimoine artistique grâce à des prestations de nettoyage et de restauration réalisées avec le plus grand soin.", "Chaque œuvre est étudiée avant toute intervention afin de lui redonner son éclat tout en respectant son histoire, ses matériaux et l'intention de l'artiste. Un tableau est bien plus qu'un objet décoratif : c'est un souvenir de famille, un héritage ou une pièce de collection qui mérite d'être préservée pour les générations futures."])}
{strip(["assets/ac-dorures-1.jpg", "assets/ac-dorures-2.jpg", "assets/ac-dorures-3.jpg", "assets/ac-dorures-4.jpg"], 4)}
<div class="p-note reveal"><p>N'hésitez pas à nous apporter votre tableau pour un diagnostic et un devis personnalisés.</p></div>
<div class="p-cta reveal">{btn("Demander un diagnostic", "contact.html")}</div>
</div></section>'''

# ================= PARTENAIRES =================
partners = [
    ("EH", "L'encadr'heure", "Bordeaux"),
    ("AV", "Angles Var", "La Garde"),
    ("CS", "Les cadres de Sophie", "Tassin-la-Demi-Lune"),
    ("AC", "Art et Cadres", "Toulouse"),
    ("HC", "Une histoire de cadre", "Mulhouse"),
    ("CR", "Cadre Roussin", "Paris 15e"),
    ("EC", "L'encadreur aux cadres", "Caen"),
    ("CSa", "Claude Samuel", "Paris 12e"),
    ("PP", "Le cadre passe-partout", "Reims"),
    ("MB", "Misterblad", "Clichy"),
    ("ChR", "Le Chat Rouge", "Pau"),
]
partenaires_body = f'''<section class="section"><div class="p-w">
{content_hero("Partenaires & fournisseurs", "Nos partenaires et fournisseurs", "<p>Les maisons avec lesquelles nous travaillons, et les encadreurs qui nous recommandent partout en France.</p>", "", "", solo=True)}
<div class="brandfeat reveal" style="margin-top:clamp(48px,6vw,72px)">
  <div class="brandfeat__mark"><span class="wm">nielsen</span><span class="wmsub">Design</span></div>
  <div class="brandfeat__body">
    <h2>Nielsen Design, notre fournisseur de référence</h2>
    <p>Fort d'une expérience de plus de 30 ans dans l'encadrement, Nielsen réunit une équipe de passionnés qui conçoit chaque jour des baguettes et des cadres pour rendre votre intérieur aussi parfait que possible. Nature, Color, Design, Charme : quatre univers, mille possibilités.</p>
    {btn("Visiter le site Nielsen", "https://www.nielsen-design.com/")}
  </div>
</div>
<h2 class="p-h2 reveal" style="margin-top:clamp(72px,9vw,120px)">Ils nous recommandent</h2>
{logo_wall(partners, flex=True)}
</div></section>'''

# ================= GALERIE =================
gal_cells = "".join(
    f'<figure class="g-cell reveal"><div class="g-frame"><img src="assets/gal-{i:02d}.jpg" '
    f'alt="Œuvre encadrée par Art\'Cadres Luxembourg" loading="lazy"></div></figure>'
    for i in range(1, 19))
galerie_body = f'''<section id="gal" class="section"><div class="p-w">
<span class="p-eyebrow">Notre galerie</span>
<h2 class="p-h1">Une collection coup de cœur</h2>
<div class="g-lead reveal"><p>Passionnés depuis plus de 30 ans, nous avons construit notre espace galerie autour d'œuvres choisies, encadrées et mises en lumière avec le même soin que celui porté à vos objets.</p></div>
<div class="g-grid">{gal_cells}</div>
<div class="g-cta reveal">{btn("Prendre rendez-vous", "contact.html")}</div>
</div></section>'''

# ================= CONTACT =================
contact_body = '''<section id="contact" class="section"><div class="p-w">
<span class="p-eyebrow">Nous trouver</span>
<h2 class="c-h1">Où trouver la boutique Art'Cadres ?</h2>
<div class="c-lead reveal"><p>Votre artisan encadreur vous accueille sur rendez-vous, au cœur de Luxembourg-Ville.</p></div>
<div class="c-grid">
  <div class="reveal">
    <div class="c-info">
      <div class="c-row"><p class="c-lab">Téléphone</p><div class="c-val"><p><a href="tel:+35227849488" style="text-decoration:none;color:inherit">+352 27 84 94 88</a></p></div></div>
      <div class="c-row"><p class="c-lab">E-mail</p><div class="c-val"><p><a href="mailto:contact@artcadres.lu" style="text-decoration:none;color:inherit">contact@artcadres.lu</a></p></div></div>
      <div class="c-row"><p class="c-lab">Adresse</p><div class="c-val"><p>2 bis rue de la toison d'or<br>L-2342 Luxembourg (Hollerich)</p></div></div>
      <div class="c-row"><p class="c-lab">Horaires</p><div class="c-val"><p>Mercredi au samedi<br>de 10 h à 18 h</p></div></div>
    </div>
    <div class="c-note"><p>Nous répondons sous 48 h ouvrées.</p></div>
  </div>
  <figure class="reveal" style="margin:0;--d:120ms"><div class="c-frame"><img src="assets/ac-contact.jpg" alt="Boutique Art'Cadres Luxembourg" loading="lazy"></div></figure>
</div>
</div></section>'''

# ================= CONFIGURATEUR =================
CFG_URL = "https://nielsen.oxyz.studio/project/new/3b83739c106fa33d171be9a151d26ab9/app"
cfg_points = ["Prix en temps réel", "Devis immédiat", "Ajusté au millimètre"]
cfg_points_html = "".join(
    '<li><svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>' + e(p) + "</li>"
    for p in cfg_points)
configurateur_body = f'''<section id="cfg">
<div class="cfg-inner">
  <div class="cfg-head reveal">
    <p class="cfg-eyebrow">Sur mesure, en ligne</p>
    <h2 class="cfg-title">Composez votre cadre</h2>
    <p class="cfg-intro">Choisissez la baguette, le passe-partout et le verre. Le prix se calcule au fur et à mesure, et vous obtenez votre devis immédiatement.</p>
    <ul class="cfg-points">{cfg_points_html}</ul>
  </div>
  <div class="cfg-stage reveal">
    <div class="cfg-skeleton" aria-hidden="true"></div>
    <iframe class="cfg-frame" src="{CFG_URL}" title="Configurateur d'encadrement sur mesure" loading="lazy" allow="clipboard-write; fullscreen" referrerpolicy="strict-origin-when-cross-origin" onload="var s=this.parentNode.querySelector('.cfg-skeleton'); if(s) s.style.display='none';"></iframe>
  </div>
  <p class="cfg-fallback">Le configurateur ne s'affiche pas ? <a href="{CFG_URL}" target="_blank" rel="noopener">Ouvrez-le dans un nouvel onglet</a>.</p>
</div>
</section>'''

# ================= ÉCRITURE =================
PAGES = [
    ("index.html", "Art'Cadres Luxembourg, encadreur d'art, sur mesure & restauration",
     "Encadreur d'art à Luxembourg (Hollerich) : encadrement sur mesure, cadres standards Nielsen, dorure, restauration de tableaux et galerie. Maison Neumann depuis 1972.",
     accueil_body),
    ("notre-histoire.html", "Notre histoire, Art'Cadres Luxembourg (Maison Neumann)",
     "L'histoire d'Art'Cadres Luxembourg : encadrement sur mesure, restauration, dorure et galerie, dans la tradition de la Maison Neumann.",
     hist_body),
    ("encadrement-sur-mesure.html", "Encadrement sur mesure à Luxembourg, Art'Cadres",
     "Encadrement d'art sur mesure à Luxembourg : Marie-Louise, caisse américaine, rehausse et baguettes Nielsen.",
     mesure_body),
    ("encadrement-standard.html", "Cadres standards Nielsen, Art'Cadres Luxembourg",
     "Cadres Nielsen en bois et aluminium : qualité, finitions et certification FSC, fabriqués en Allemagne.",
     standard_body),
    ("dorures-restauration.html", "Dorure & restauration de tableaux, Art'Cadres Luxembourg",
     "Nettoyage, restauration de tableaux et dorure à Luxembourg. Diagnostic et devis personnalisés.",
     dorures_body),
    ("notre-galerie.html", "Notre galerie, Art'Cadres Luxembourg",
     "La galerie d'Art'Cadres Luxembourg : une collection d'œuvres choisies, encadrées et mises en lumière.",
     galerie_body),
    ("partenaires.html", "Nos partenaires et fournisseurs, Art'Cadres Luxembourg",
     "Nielsen Design et un réseau d'encadreurs partenaires qui recommandent Art'Cadres Luxembourg.",
     partenaires_body),
    ("contact.html", "Contact, Art'Cadres Luxembourg (Hollerich)",
     "Contactez Art'Cadres Luxembourg : 2 bis rue de la toison d'or, L-2342 Luxembourg. Tél. +352 27 84 94 88.",
     contact_body),
    ("configurateur.html", "Composez votre cadre, devis en ligne, Art'Cadres Luxembourg",
     "Composez votre cadre sur mesure en ligne et obtenez un devis immédiat : baguette, passe-partout et verre.",
     configurateur_body),
]

for fname, title, desc, body in PAGES:
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(page(title, desc, body, fname))
    print("écrit :", fname)

print("OK,", len(PAGES), "pages générées.")
