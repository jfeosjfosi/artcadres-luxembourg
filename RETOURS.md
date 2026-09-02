# Retours client — plan par phases

Document vivant. Chaque passe de relecture s’ajoute ici, page par page. On exécute **une phase à la fois**, avec captures desktop 1440×900 et mobile 390×844 avant push.

**Lecture design :** site artisan + B2B (Hollerich), crème / encre / orange, photos réelles d’atelier. Variance 6, motion 4, densité 4. Tokens : `DESIGN.md`. QA : `QA-UI.md`.

**Preview :** https://jfeosjfosi.github.io/artcadres-preview/

---

## Règles globales (tous les phases)

- Copy : « nous », jamais « on ». Pas de tiret cadratin.
- Orange = Contact / rendez-vous. **Exception validée** : le CTA « Accéder au configurateur » du bloc devis accueil passe en orange (conversion Click & Collect). Le bouton hero « Composer votre cadre en ligne » reste contour.
- **Ne pas toucher** la section « Réalisations encadrées » (teaser galerie accueil) ni la page galerie, sauf bug bloquant.
- Cadres photo : un seul traitement `.p-frame` (mat blanc, `--r-frame` 4px, padding `--s2`–`--s3`, ombre `--shadow`). Pas de `.p-fr` nu à côté.
- Images : photos d’atelier / réalisations du stock `assets/`, pas de studio Shutterstock (fog road, salon NY, mur d’escalier lifestyle).
- Vérif obligatoire : Playwright 1440×900 + 390×844, zone touchée, mesures en px. Boucle corriger → recapturer.
- Build : `python3 build.py` si `build.py` ou le HTML généré change. Commit + `git push origin main` et `git push preview main`.

---

## Page 1 — Accueil (`index.html`)

Retours du 2 sept. 2026. Source : `build.py` (`accueil_body`), `styles.css` (`#acc`, `#gf`, `#faq`, `#avis`, footer), `script.js` (pile polaroid).

### A1 — Hero : animation polaroid

**Constat.** L’arc est mieux, mais ça saccade encore. Le vrai défaut : **coup de passe de plan**. À chaque cycle, les cartes du dessous sont restackées (z-index + transform) en même temps que la carte du dessus vole. Résultat : une image **surgit au premier plan** pendant qu’une autre **tombe derrière**, sans fluidité.

Cause dans `script.js` : au `cycle()`, les sœurs passent tout de suite en `z-index` du slot supérieur et animent `pose(i+1) → pose(i)` pendant 1080 ms. Le z-index ne s’interpole pas : c’est un pop.

**Cible.** Une pile de photos posée sur une table. Seule la carte du dessus bouge. Elle glisse un peu sur le côté, passe derrière **à l’instant du pic**, et **revient à sa place**. Les autres cartes ne bougent pas, ne changent pas de z-index pendant le vol. DOM : `appendChild` à la fin, z-index uniquement (5→1 selon l’ordre), **transforms inchangés** (pose d’identité par carte, `data-home`).

Fichiers : `script.js`, `styles.css` (`.polaroid`), `QA-UI.md`.

Vérif : y monotone pendant le peek, un seul pic x, opacity 1, pas de clip, **aucune sœur dont le getBoundingClientRect ne bouge de plus de 4 px**, z de la carte volante qui drop à mi-course pas à l’arrivée.

### A2 — Hero : colonne gauche + air sous la nav

**Constat.** « Encadreur d’art à Luxembourg » + avis : pas mal, mais le bloc **ne descend pas**. Il est collé en haut (`align-items: start`, `padding-top: 32px` desktop / `28px` mobile). Tout est calé en haut, pas aligné avec le volume de la pile. La hero **colle à la navbar**.

**Cible (tokens).**

| | Desktop 1440 | Mobile 390 |
|---|---|---|
| Air header.bottom → premier contenu hero | **52–64 px** (était 24–36, trop juste) | **36–44 px** |
| Colonne gauche vs pile | `align-items: center` dès 960 px | stack naturel, air au-dessus du H1 |
| Rythme interne gauche | badge → `--s3` → H1 → `--s4` → lead → `--s5` → boutons | idem |

Mettre à jour `DESIGN.md` § Hero et `QA-UI.md` (anciens 24–36 / 20–28). **Ne jamais** `padding-top: 0` sur `#acc .p-hero-home`.

Fichiers : `styles.css` (`#acc .p-hero-home`, `.p-hw`, `.p-gtrust`, `.p-btns`).

### A3 — Quatre métiers (01 Standards … 04 Institutions)

**Constat.** La grille est la bonne idée. **01 et 02 trop collés.** Filet (`border-top` sur `.p-services`) + `margin-top: 64px` : le filet arrive trop tôt sous la hero, le design ne respire pas. Les sections du site sont **globalement trop collées**.

**Cible.**

- Air hero → filet métiers : `--s7` (64px) **en plus** d’un `padding-top: --s6` au-dessus du filet, ou un seul `margin-top: --space-section` (64–80) et filet collé au padding, pas les deux trop faibles.
- Gap interne grille : desktop 4 col **56×64** (était 40×48). Mobile : **48px** entre les tuiles.
- Numéros 01–04 : plus d’air sous l’icône (`margin-bottom: --s4` sur `.p-svc__head`).
- Audit rythme **toute la page** (sous-agent) : entre `#acc` blocs, `#conf`, `#gf`, `#real`, `#faq`, `#avis` — viser `--space-section` clamp 72–96 px (aujourd’hui 64–80, trop serré d’après le ressenti). Passer `--space-section` à `clamp(72px, 8vw, 96px)` et `--space-block` à 72px. Recalibrer si un bloc explose.

Fichiers : `styles.css` (`:root`, `#acc .p-services`, `.section`).

### A4 — Bloc « Votre devis, en quelques clics »

**Constat.** Photo type catalogue (échantillons baroques / studio) à côté d’un Nielsen Click & Collect : ça ne raconte pas l’atelier. CTA contour alors qu’il **mérite l’orange**. « Click & Collect · retrait en 1 h » **pas aligné** avec le bouton (wrap, baseline, ou colonne mobile cassée).

**Cible.**

- Image : photo **réelle atelier**. Remplacer `ac-mesure-2.jpg` par `ac-contact.jpg` (mur de baguettes Hollerich) ou `ac-standard-2` seulement si on croppe du vrai atelier — **préférer `ac-contact.jpg`** ou `histoire-atelier-1.jpg`.
- CTA : `btn_orange("Accéder au configurateur", "configurateur.html")`.
- Note Click & Collect : même ligne que le bouton, `align-items: center`, `min-height: var(--btn-h)`, `display: inline-flex`. Mobile : note sous le bouton, alignée à gauche du bouton, pas étirée en pleine largeur bizarre.
- Mettre à jour `DESIGN.md` : exception orange configurateur **uniquement** sur ce CTA de conversion.

Fichiers : `build.py` (bloc `p-cta--rich`), `styles.css` (`#acc .p-cta__action`, `#acc .p-cta__note`), `DESIGN.md`.

### A5 — Mosaïque « À l’atelier »

**Constat.** Le titre « À l’atelier » ne dit pas la marque. Proposition client : **Art'Cadres Luxembourg**.

Tuile Nielsen : `ac-standard.jpg` = shot studio (route dans le brouillard + passe-partout) → Shutterstock. Remplacer par du stock atelier : `ac-contact.jpg` (si pas déjà pris par le devis) ou `ac-standard-1` est le même shot studio — **éviter**. Mieux : photo mur Nielsen / aluminium réel. Si le seul « standard » propre est `ac-contact.jpg`, l’utiliser ici et mettre `histoire-atelier-1.jpg` sur le devis, ou l’inverse (devis = contact mur, Nielsen = `ac-mesure-1.jpg` machine Nexus / passe-partout, qui est de l’atelier).

Décision verrouillée :

| Emplacement | Image |
|---|---|
| Devis / configurateur | `assets/ac-contact.jpg` |
| Mosaïque Cadres Nielsen | `assets/ac-mesure-1.jpg` (Nexus, vrais passe-partout) |
| Mosaïque Sur mesure | garder `ac-mesure.jpg` **seulement si** ça ne fait pas lifestyle Shutterstock. `ac-mesure.jpg` = cage d’escalier / gallery wall lifestyle → **remplacer** par `histoire-atelier-1.jpg` (œuvre sur chevalet, mur d’échantillons). |

Titre mosaïque : `Art'Cadres Luxembourg`.

Fichiers : `build.py` (`metier_grid(...)`).

### A6 — « Nous encadrons et installons sur site »

**Constat.** Les deux photos n’ont **pas le même cadre** (`.p-fr` : filet + overflow, pas de mat `.p-frame`). Traitement différent du reste du site.

**Cible.** Mêmes `.p-frame` que le story 1972. Ratio 4/3, `object-fit: cover`. Photos : garder `kathia-grand-format.jpg` et `gf-deloitte-2.jpg` (vraies poses) — ce sont les bonnes, seul le **rebord** change.

Fichiers : `build.py` (`#gf .p-imgs`), `styles.css` (`#gf .p-fr` → réutiliser `.p-frame` ou aligner les tokens).

### A7 — « Nous encadrons tout type d’objet »

**Constat.** Les 4 cellules n’ont pas le même encadrement que le reste (images à ras, grille 1px, pas de mat). Médailles / végétal / cuillère / trèfle sont de **vraies** pièces — on les garde. On unifie le cadre.

**Cible.** Chaque objet dans `.p-frame` (padding `--s2`, fond `--mat`). Image `aspect-ratio: 1/1` cover. Gap `--s3` au lieu du filet 1px. Caption sous le cadre, même `.p-cap` que partout.

Fichiers : `build.py` (`gf_objs_html`), `styles.css` (`#gf .p-objs`, `#gf .p-obj`).

### A8 — FAQ

**Constat.** Trop d’air entre les questions (~30 % de trop). Le bloc FAQ est trop grand par rapport à la carte atelier à droite. Titre aside « Atelier Hollerich » : **ça ne va pas** → **Art'Cadres Luxembourg**.

**Cible.**

- Padding item : `--s5` 0 `--s6` (32 / 48) → **`--s4` 0 `--s4`** (24 / 24), soit environ −30 %.
- Gap split : `--s7` → `--s5` / `--s6`.
- Aside : `h3` = `Art'Cadres Luxembourg`. Lead inchangé (rendez-vous mercredi–samedi).

Fichiers : `styles.css` (`.faq-item`, `.faq-split`), `build.py` (aside).

### A9 — « Ils nous ont fait confiance, ils en parlent »

**Constat.** Titre **beaucoup trop collé** à la note / badge 4,9/5 juste en dessous.

**Cible.** `#avis .p-h2` a `margin: 0`. Mettre `margin: 0 0 var(--s5)`. Badge ensuite. Pas de filet collé.

Fichiers : `styles.css` (`#avis .p-h2`, `#avis .p-badges`).

### A10 — Footer

**Constat.** Logo Art'Cadres Luxembourg **pas aligné à gauche** avec « Encadrement sur mesure » (colonne prestations, et/ou le paragraphe sous le logo). Le SVG blanc a un `viewBox` large + image embarquée : **marge optique** à gauche. Header à `1340px`, footer à `--maxw` 1180px : les gauches ne coïncident pas.

**Cible.**

- Footer `.fw` et header `.bar` : même gouttière et même `max-width` de contenu (`--maxw` 1180 **ou** 1340, un seul). Recommandé : footer et header inner à `max-width: min(100%, 1340px)` + `padding: 0 24px`, logo flush left.
- Logo : `margin-left` négatif si le SVG a du padding interne, jusqu’à ce que le **glyphe** (pas le viewBox) aligne avec le H3 « Nos prestations » / premier lien. Mesurer `getBoundingClientRect().left` logo vs lien « Encadrement sur mesure » — écart cible **0–2 px** si on veut le logo dans la même colonne… Non : le logo est **colonne 1**, le lien est **colonne 2**. Le client parle du logo vs le **texte sous le logo** (« Encadrement sur mesure, cadres standards… ») dans **la même colonne**. Aligner glyphe logo + paragraphe, `align-items: flex-start`, crop du SVG si besoin.

Fichiers : `styles.css` (`.site-header .bar`, `.site-footer .fw`, `.footer-logo img`), éventuellement recadrage SVG.

### A11 — Audit rythme site entier (sous-agent)

Après A3–A10, un passage **toutes les pages** déjà en ligne (accueil d’abord, puis les autres au fil des retours) : paddings de section, filets orphelins, titres collés aux sous-titres, boutons vs notes. Livrable : tableau page × section × gap mesuré × verdict. Pas de push d’écran cassé.

---

## Langage visuel de référence (accueil)

Les pages intérieures **se calent sur l’accueil déjà retravaillée**, pas sur le template `content_story` (titre à gauche, pavé à droite). Interdit d’enchaîner trois splits texte/texte. On réutilise : mosaïque `.metier`, tuiles `.p-svc` / `.p-ico` lisibles, `.p-frame` identique, 4 objets comme sur l’accueil, air `--space-section`.

`DESIGN.md` §7 le dit déjà : *Ne pas enchaîner trois splits image/texte.* Les pages Sur mesure et Standard le violent.

---

## Page 2 — Encadrement sur mesure

Retours du 2 sept. 2026. Fichier : `encadrement-sur-mesure.html` ← `mesure_body` dans `build.py`. Source originale à ne pas skipper : https://artcadres.lu/nos-services/encadrement-sur-mesure/

### B1 — Hero photo Shutterstock / IA

**Constat.** `assets/ac-mesure.jpg` = gallery wall lifestyle (escalier, mur sombre, déco). Ça fait catalogue, pas Hollerich.

**Cible.** Photo atelier réelle : `histoire-atelier-1.jpg` (œuvre sur chevalet + mur d’échantillons) ou `ac-contact.jpg` si pas déjà prise par l’accueil. Caption honnête (« Encadrement sur mesure à l’atelier, Hollerich »). Même `.p-frame` que l’accueil.

### B2 — Rangée « Étude personnalisée / Techniques / Du petit au monumental »

**Constat.** Sections trop collées (`.p-icos` margin 40–64, collé au hero et au story suivant). Les pictos dans un rond 48 px sont trop faibles : **on ne les lit pas comme des icônes**, donc « il n’y a pas d’icône ». Ça n’incite pas à lire.

**Cible.** Même présence que les 01–04 de l’accueil : icône 44 px encre/orange, numéro ou label, air `--s6` au-dessus et en dessous, gap interne `--s6`. Pas un filet collé au hero. Les trois messages restent (étude, techniques, formats).

### B3 — Pavés « Mettre l’œuvre en valeur… » / « Du rendez-vous… » / « Objets, volumes… »

**Constat.** Trois `.p-story` d’affilée : gros H2 à gauche, **mur de paragraphes à droite, sans image, sans icône**. Illisible. Fait à l’arrache. Personne n’a envie de lire.

**Cible.** Supprimer ce pattern sur cette page. Remplacer par :

1. Un **seul** bloc court « Mise en valeur, selon votre budget » (2 phrases max, moulures contemporain → classique) + visuel atelier.
2. Le détail rendez-vous / délais : **liste métier** type accueil (titre + une ligne), pas un roman.
3. Objets / quand venir : renvoyé à la grille 4 objets (B7) + une ligne vers le configurateur.

Garder les faits, tuer le pavé.

### B4 — Techniques (Marie-Louise, caisse américaine, rehausse)

**Constat.** **Ça, c’est bien.** Ne pas casser le bloc `tech-cards`. Garder Marie-Louise biseautée, caisse américaine, technique de rehausse. « Moulures et baguettes » peut rester en 4e carte si la photo n’est pas studio baroque (`ac-mesure-2`) — préférer `ac-contact.jpg` ou un crop d’échantillons réel.

Copy alignée sur l’ancien site (ne pas appauvrir) :

- Marie-Louise : haut de gamme du passe-partout, profondeur, montage traditionnel et moderne.
- Caisse américaine : œuvre qui flotte, effet de suspension.
- Rehausse : verre en suspension au-dessus du sujet, fond possible.

### B5 — Bande Pop-art / Triptyque / Galerie privée / Verre museum

**Constat.** Les **formats d’image ne marchent pas** (`.p-strip--lg` force `aspect-ratio: 3/4` + `min-height: 400` sur 4 photos qui n’ont pas le même cadre). Crop moche, rythme nul.

**Cible.** Même traitement que la mosaïque accueil ou la galerie teaser : ratio **4/5 ou 4/3 unique et assumé**, `object-fit: cover` avec `object-position` par image si besoin, pas 3/4 portrait forcé sur un pop-art carré. Captions plus petites que `--t-h3` (aujourd’hui `.p-cap--lg` 16px bold, OK) mais **pas plus grosses que le H2 de section**. Si les 4 photos ne tiennent pas un strip égal, passer en mosaïque 2+2 (comme `.metier`).

Ne pas retirer les 4 réalisations, juste les recadrer / regrider.

### B6 — « Les baguettes Nielsen, 4 univers »

**Constat.** Liste texte seule, section collée, un peu moche. **« Nature » est plus gros que le titre de section** : `.p-listh` clamp 19–23 px vs `.p-list .t` = `--t-h3` 20–26 px. Hierarchie inversée, ça n’a pas de sens.

**Cible.** Quatre tuiles avec **image ou icône** (échantillon bois / couleur / ligne / patine — photos atelier, pas mockup). Titre de section = `--t-h2`. Nom d’univers = `--t-h3` **strictement plus petit**. Air `--space-block` au-dessus. Reprendre les 4 libellés de l’ancien site (Nature, Color, Design, Charme) mot pour mot sur le fond.

### B7 — Médailles / végétaux / objets — 4e oublié

**Constat.** Accueil : **4** objets (médailles, végétal, couverts, porte-bonheur). Sur mesure : strip de **3** (`obj-medailles`, `obj-vegetal`, `obj-cuillere`). Inconsistant. Le quatrième (`obj-trefle.jpg`, porte-bonheur) est sauté.

**Cible.** Les **mêmes 4**, même `.p-frame`, même légendes que l’accueil. Grille 4 col desktop / 2 col mobile. Pas un strip 3 qui casse la grille.

### B8 — Contenu de l’ancien artcadres.lu à **réinjecter** (ne pas skipper)

Présent sur https://artcadres.lu/nos-services/encadrement-sur-mesure/ et **absent ou noyé** aujourd’hui :

| Sujet original | Statut actuel | Action |
|---|---|---|
| Intro artisanat / centaines de possibilités | Hero lead, OK | Garder |
| Marie-Louise, caisse américaine, rehausse | tech-cards, OK | Garder (B4) |
| Styles de moulures (modernes, noir, blanc, chêne, or, wengé, gris, couleurs) | Une ligne noyée dans un pavé | Ressortir en liste courte ou pastilles |
| Objectif mise en valeur + budget | Pavé illisible | B3, version courte |
| **Centre Pompidou** (pros, particuliers, architectes, décorateurs) | **Skip** | Réinjecter une ligne factuelle, sans en faire un pavé |
| **Passe-partouts** : contrecollés PH neutre, sans acide, conservation | **Skip** | Bloc matière 3 points (passe-partout / verre / baguette) |
| **Verre Nielsen** : confort visuel, couleurs, filtrage UV **55 % à 99 %** | **Skip** | Même bloc matières |
| Nielsen 4 univers | Liste trop petite / hiérarchie cassée | B6 |
| CTA projet + patrimoine / restauration | CTA contact existe ; lien restauration faible | Bouton orange conseil + lien vers dorure |

Ne pas réécrire un roman SEO par-dessus. Les faits de l’ancien site passent **avant** les textes générés « Du rendez-vous à Hollerich… ».

---

## Page 3 — Encadrement standard (Nielsen)

Retours du 2 sept. 2026 : **mêmes griefs** que Sur mesure. Fichier : `encadrement-standard.html` ← `standard_body`. Original : https://artcadres.lu/nos-services/encadrement-standard/

### C1 — Hero Shutterstock

**Constat.** `ac-standard.jpg` (et `ac-standard-1.jpg`) = cadre chêne + photo brouillard / route, studio. `ac-standard-2.jpg` = salon NY + lampadaire, mockup. Aucun n’est l’atelier.

**Cible.** Hero = photo réelle (mur de baguettes, cartons Nielsen visibles dans `gal-08` / `ac-contact` / `ac-mesure-1`). Les deux shots studio ne servent plus de hero ni de strip de fin.

### C2 — Icônes Click & Collect / Devis / Qualité + sections collées

Même diagnostic que B2. Même cible (présence type accueil, air `--s6`).

### C3 — Pavés « Aluminium ou bois » / « Ce que vous emportez »

**Constat.** Encore des `.p-story` : titre à gauche, **pavé à droite sans image**. Pire : le second story a **4 paragraphes**. Illisible. Ce n’est pas sur l’ancien site (l’ancien est court).

**Cible.** Couper les romans. Structure accueil-like :

- Liste 4 points de l’ancien site (bois, aluminium, Nielsen Design / FSC, fabriqué en Allemagne) **en tuiles ou liste métier**, hiérarchie titre de section > item.
- Un split unique éventuellement : photo atelier + 2 phrases « configurateur + retrait 1 h ».
- CTA orange exception configurateur (même règle que A4) + note Click & Collect alignée.

### C4 — Strip 2 photos studio en bas

**Constat.** `ac-standard-1` + `ac-standard-2` = encore du stock. À remplacer par du vrai (échantillons, chevalet, cartons Nielsen).

### C5 — Contenu original Standard, ne pas skipper

| Sujet original | Statut | Action |
|---|---|---|
| Qualité qui fait la différence (alu + bois) | Liste, OK | Garder, mieux rythmer |
| Cadres bois : dorés, couleurs vives, bois bruts | OK | Garder |
| Cadres alu : charger / démonter, tournettes rivetées dos MDF, verre minéral 2 mm chants polis, pas de blessure | OK mais noyé | Ressortir |
| Conçus par Nielsen Design, **FSC®**, mention « Cadre certifié FSC® » | FSC dit, mention exacte **skip** | Réinjecter la mention |
| Fabriqué en Allemagne, expertise cadre / verre / contrecollé | OK | Garder |
| Click & Collect 1 h | Icônes, OK | Garder, plus lisible |
| Univers Nature / Color / Design / Charme | Noyé dans un pavé | Soit renvoyer vers Sur mesure B6, soit 4 pastilles ici aussi |

---

## Contenu original sauté (site entier)

Croisement https://artcadres.lu/ (accueil) + pages services. À traiter, pas à inventer plus tard.

| Original artcadres.lu | Nouveau site | Décision |
|---|---|---|
| Accueil : **Tirage photo**, petits et grands formats | **Absent** | Réinjecter (ligne métier, mosaïque ou page courte) — ne pas skipper |
| Accueil : Click and Collect 1 h | Présent | OK |
| Sur mesure : Pompidou, PH neutre, verre UV 55–99 % | Skip | B8 |
| Histoire : Sylvie Schied, musées, MH, miroirs/consoles/statues/ferronnerie | Partiel sur dorure | Vérifier à la passe Dorure |
| Boutique WooCommerce | Remplacée par configurateur Nielsen | OK, volontaire |
| Cours dessin / vente matériel (texte Maison Neumann Metz) | Non repris (c’est Metz, pas LU) | Ne pas coller sur LU |

Principe : **si c’était sur artcadres.lu Luxembourg, ça reste.** On ne « compacte » pas en silence.

---

## Page 4 — Dorure & restauration

Retours du 2 sept. 2026. **Verdict : vraiment pas trop mal.** Fichier : `dorures-restauration.html`. Original : https://artcadres.lu/nos-services/restauration-de-tableaux-dorures/

### D1 — Textes trop longs

Trois `.p-story` (« Préservation de votre patrimoine », « Un diagnostic… », « Quand restaurer… »). On se fait chier. Couper à **un** split court (2 phrases) + liste métier (diagnostic, dorure, ce que nous ne faisons pas). Garder Sylvie Schied + agrément MH (c’était sur l’ancien site).

### D2 — « Le travail, en images » trop bas

Les étapes avant / pendant / après **sont cool**. Les monter **juste sous le hero + icônes**, avant tout roman. « La préservation de votre patrimoine » en tête : un peu ièche. Titre plus concret (« Avant, pendant, après ») ou pas de H2 ronflant du tout.

Ne pas casser `rest_gallery()`.

---

## Page 5 — Institutions & entreprises

**Verdict : bien. Layout à garder.** Textes un peu chiant mais ça va. Ne pas refondre la grille de cas.

### E1 — Raccourcir les deux `.p-story` de fin

« Comment nous travaillons » / « Devis, délais » : 2 phrases chacun, ou une liste 3 puces. Le hero + logos + cartes clients **restent**.

---

## Page 6 — Notre galerie

**Verdict : la grille d’œuvres est bien. Ne pas y toucher** (déjà verrouillé). Le **chapeau est faux**.

### F1 — Lead gigantesque, hors DESIGN.md

`#gal .g-lead` = 3 paragraphes, `font-size: clamp(17px, 2vw, 21px)`, `max-width: 54ch`, marge bas jusqu’à **96 px**. Ça n’existe nulle part ailleurs. Ce n’est ni `--t-body` (16 px) ni `--t-h1`.

Le pavé « Passionnés depuis plus de 30 ans … mercredi au samedi, de 10 h à 18 h » est fait à l’arrache.

**Cible.** Un seul paragraphe, `--t-body` 16 px, `line-height: 1.65`, `max-width: var(--measure)` (46–65 ch), marge `--s6` max. H1 = `--t-h1` comme les autres pages (pas `--t-display`). Horaires : une ligne, ou rien (c’est déjà au contact / FAQ). Grille inchangée.

Fichiers : `build.py` (`galerie_body`), `styles.css` (`#gal .g-lead`).

---

## Page 7 — Notre histoire

**Verdict : pas mal.** Fichier : `notre-histoire.html`.

### G1 — Hero trop petit, mat trop gros

`ac-histoire.jpg` (vitrine atelier, photo réelle) : **agrandir** l’image (colonne photo plus large, ou ratio 4/3 rempli). Le `.p-frame` a un mat **plus épais / plus grand** que le reste du site. Aligner padding sur `--s2` comme partout. Pas un cadre « spécial histoire ».

### G2 — Plus de photos atelier / shop

Utiliser le stock : `ac-contact.jpg`, `histoire-atelier-1.jpg`, `ac-mesure-1.jpg`, etc. Pas de lifestyle Shutterstock.

### G3 — « Nos métiers réunis en un même lieu »

Liste titre + ligne **sans icônes**, deux colonnes qui ne dialoguent pas. Même traitement que l’accueil 01–04 : icône + titre + une ligne, 4 métiers (sur mesure, restauration, dorure, galerie).

### G4 — Kathia toute seule, pas avec M.Chat

`kathia-fondatrice.jpg` = Kathia **+ Thoma Vuille + découpe M.Chat** (source `Fwd_Avec_Mr_chat`). Elle doit être **seule**. Recadrer le tiers gauche, ou partir d’une meilleure photo solo (`kathia-portrait.jpg` bien croppée, ou négatif dans `ArtCadres-refs/`). Légende « Kathia Neumann · fondatrice ». **Pas de M.Chat à côté d’elle.**

### G5 — Caisses emballées (portraits / « Napoléon »)

Photo `histoire-atelier-2.jpg` : rangées de cadres **sous bulles**, portraits officiels prêts à livrer. **L’afficher** (série, sérieux, volume). Exception explicite au vieux hors-scope « pas de Napoléon dans la galerie » : ici c’est **l’emballage pro**, pas une mise en galerie de l’œuvre.

### G6 — Virer la citation

Supprimer `.p-quote` (« Chaque œuvre mérite une présentation… »). Zéro exception.

### G7 — « Particuliers… » vs bouton rendez-vous

`.p-note` puis `.p-cta` : pas ferrés à gauche, pas alignés. Même `padding-left: 0`, même axe, `align-items: flex-start`. Le note n’est pas un pavé centré sous une citation disparue.

---

## Page 8 — Partenaires

**La page existe sur l’ancien site :** https://artcadres.lu/partenaires/ → **on la garde.** (Nielsen Design + « Ils nous recommandent ».)

### H1 — Il manque tous les logos

Les tuiles sont des **wordmarks SVG texte** (fichiers ~280 o) ou **aucune image** (LC Cadres, Maison Neumann Metz, La tête dans le cadre). Ça ne ressemble pas à des logos. Nielsen = faux lockup typo dans `.brandfeat`.

**Cible.** Vrais logos (ou wordmarks soignés à partir des sites partenaires). Les 14 maisons de l’ancien site restent. Nielsen : lockup propre, **pas de lien outbound** (déjà décidé). Page moins « affreuse » : grille type logostrip accueil, air, pas de carte Nielsen + 120 px de vide au-dessus de « Ils nous recommandent ».

Fichiers : `build.py`, `fetch_logos.py`, `styles.css` (`.partnergrid`, `.brandfeat`).

---

## Page 9 — Contact

### I1 — Portrait Kathia pétée

`.c-kathia` : polaroid rotaté, `object-position: center 8%`, crop raté (table, lustre, œuvre coupée). **Pas un groupe.** Recadrage portrait (tête + épaules + un peu d’atelier), même `.p-frame` que le site, **sans** `rotate(-1.8deg)` si ça casse le crop.

Vérif **obligatoire** 1440×900 **et** 390×844 : visage entier, pas de front coupé, pas de bandeau table en bas.

Meilleure source : recadrer `kathia-portrait.jpg` (elle est seule) plutôt que `kathia-fondatrice.jpg` (M.Chat).

### I2 — Carte : garder

La map en bas est bien. La laisser. Zone « Luxembourg-Ville, Hollerich, Howald » : raccourcir le pavé (même problème que F1).

Fond page = `--bg` (beige), comme l’accueil. Pas d’îlot blanc.

---

## Page 10 — Configurateur

### J1 — Fond blanc vs beige du site

`#cfg { background: var(--bg2) }` et `.cfg-stage { background:#fff; border-radius:16px }`. La nav et l’accueil sont `--bg` `#f2ede6`. La page « saute » en blanc / carte arrondie hors système.

**Cible.** Fond de page `--bg`. L’iframe Nielsen peut rester blanche **à l’intérieur** de l’outil (c’est leur UI), mais le chrome autour (titre, intro, footer) = même beige, mêmes `--t-h1` / `--t-body`, pas un îlot SaaS.

Fichiers : `styles.css` (`#cfg`).

---

## Vérif (toutes les phases, non négociable)

Approche complète : **desktop 1440×900 et mobile 390×844**, screenshot de la zone, lecture des PNG, mesure (gaps, crop Kathia, filets). Si un format est faux : corriger, recapturer. Pas de « ça devrait aller ». Détail : `QA-UI.md`.

---

## Pages encore ouvertes

Rien d’autre en attente de retours client. Légal / cookies : hors passe visuelle sauf bug.

---

## Phases d’exécution — Accueil

Ordre volontaire : d’abord ce qui « saute aux yeux », ensuite le rythme, ensuite les photos, ensuite le site-wide.

| Phase | Contenu | Fichiers | Statut |
|---|---|---|---|
| **0** | Ce document | `RETOURS.md` | fait |
| **1** | A1 animation + A2 hero air / alignement | `script.js`, `styles.css`, `QA-UI.md`, `DESIGN.md` | fait |
| **2** | A3 métiers + rythme `--space-section` accueil | `styles.css` | fait |
| **3** | A4 devis orange + alignement + photo atelier | `build.py`, `styles.css`, `DESIGN.md` | fait |
| **4** | A5 mosaïque titre + photos | `build.py` | fait |
| **5** | A6 + A7 mêmes cadres photo | `build.py`, `styles.css` | fait |
| **6** | A8 FAQ −30 % + titre aside | `build.py`, `styles.css` | fait |
| **7** | A9 avis + A10 footer | `styles.css` | fait |
| **8** | A11 sous-agent audit 1440 + 390 toute l’accueil, correctifs de finition | captures `_qa_audit/` (non commitées) | fait |

Chaque phase : build si besoin → screenshots des deux viewports → lecture des PNG → commit + push origin **et** preview.

---

## Phases d’exécution — Sur mesure

Après l’accueil (ou en parallèle une fois A1–A4 stables). Caler le visuel sur l’accueil, pas sur `content_story`.

| Phase | Contenu | Fichiers | Statut |
|---|---|---|---|
| **S1** | B1 hero photo atelier + B2 icônes lisibles + air | `build.py`, `styles.css` | fait |
| **S2** | B3 tuer les 3 pavés, faits en liste / un split | `build.py` | fait |
| **S3** | B4 garder tech-cards, photo moulures réelle | `build.py` | fait |
| **S4** | B5 formats Pop-art… (grille type accueil) | `build.py`, `styles.css` (`.p-strip--lg`) | fait |
| **S5** | B6 Nielsen 4 univers visuels + hiérarchie type | `build.py`, `styles.css` | fait |
| **S6** | B7 4 objets identiques à l’accueil | `build.py` | fait |
| **S7** | B8 réinjecter Pompidou, PH, verre UV, styles moulures | `build.py` | fait |

---

## Phases d’exécution — Standard

Même langage que Sur mesure / accueil.

| Phase | Contenu | Fichiers | Statut |
|---|---|---|---|
| **N1** | C1 hero atelier (plus `ac-standard.jpg`) | `build.py` | fait |
| **N2** | C2 icônes + air | `styles.css` | fait |
| **N3** | C3 couper les romans, liste type ancien site | `build.py` | fait |
| **N4** | C4 strip photos réelles | `build.py` | fait |
| **N5** | C5 FSC® mention exacte, univers, CTA configurateur | `build.py` | fait |

**Tirage photo** (sauté sur l’accueil originale) : phase dédiée dès que l’accueil A3/A5 est ouverte, pas avant d’avoir un visuel atelier. Ne pas inventer une page vide.

---

## Phases d’exécution — Restauration / Institutions / Galerie / Histoire

| Phase | Contenu | Fichiers | Statut |
|---|---|---|---|
| **DOR1** | D1 textes courts + D2 galerie avant/pendant/après plus haut | `build.py` | fait |
| **INST1** | E1 raccourcir stories institutions, **layout inchangé** | `build.py` | fait |
| **GAL1** | F1 lead galerie `--t-body`, 1 paragraphe | `build.py`, `styles.css` | fait |
| **HIS1** | G1–G7 histoire (hero, métiers+icônes, Kathia solo, caisses, **plus de citation**, alignement CTA) | `build.py`, `styles.css` | fait |

Vérif 1440 + 390 à chaque phase.

---

## Phases d’exécution — Partenaires / Contact / Configurateur

| Phase | Contenu | Fichiers | Statut |
|---|---|---|---|
| **P1** | H1 page partenaires **conservée** (existe sur artcadres.lu), vrais logos, grille propre | `build.py`, `fetch_logos.py`, `styles.css` | fait |
| **K1** | I1 crop Kathia solo + I2 map gardée, fond `--bg` | `build.py`, `styles.css` | fait |
| **Q1** | J1 configurateur fond `--bg`, chrome aligné nav | `styles.css` | fait |

Contact et configurateur : **les deux viewports**, crop Kathia relu sur les PNG.

---

## Hors scope (rappel)

- Ne pas restaurer Molitor, cfg-points, gallery featured span.
- **M.Chat** : pas sur le contact, pas collé à Kathia (histoire).
- **Napoléon / portraits officiels** : pas dans la galerie d’œuvres. **OK** sur histoire / institutions en **caisses emballées** (`histoire-atelier-2.jpg`) pour montrer le sérieux.
- Photos d’atelier **dans** la galerie : non (la galerie = œuvres encadrées).
- Iframe Nielsen : on garde.
- Page **partenaires** : on **garde** (présent sur artcadres.lu/partenaires/).
- Blog : pas V1.
- `SITE_URL` github.io tant que le DNS n’a pas basculé.
