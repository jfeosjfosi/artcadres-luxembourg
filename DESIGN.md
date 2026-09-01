# Design system — Art'Cadres Luxembourg

Source de vérité visuelle. Les tokens vivent dans `:root` de `styles.css`. Ne pas inventer de couleurs, rayons ou paddings hors de cette échelle.

**Lecture :** site artisan + B2B (Hollerich), langue éditoriale atelier, marque crème / enccre / orange. Variance 6, motion 4, densité 4. On préserve la palette. On n'introduit pas Tailwind ni une seconde accent color.

## 1. Atmosphere

Atelier lumineux, papier, bois, feuille d'or. Surfaces calmes, photos réelles, peu de cartes. L'orange n'apparaît que sur Contact et les accents (étoiles, soulignements, icônes). Le configurateur reste un bouton contour.

## 2. Color

| Token | Hex | Role |
|---|---|---|
| `--bg` | `#f2ede6` | Canvas page |
| `--bg2` | `#f6f3ee` | Bande un ton plus claire (trust, grands formats) |
| `--ink` | `#2c1f17` | Texte, logo, header |
| `--muted` | `#6b5d50` | Corps secondaire, notes |
| `--accent` | `#c15715` | Contact, étoiles, icônes, liens actifs |
| `--mat` | `#ffffff` | Carton d'un cadre photo |
| `--line` | `color-mix(in srgb, var(--ink) 12%, transparent)` | Filets 1 px |
| `--shadow` | `0 24px 60px -34px color-mix(in srgb, var(--ink) 40%, transparent)` | Cadres photo |

Jamais `#000`. Jamais un second accent. Jamais orange sur un bouton qui n'est pas Contact / rendez-vous.

## 3. Type

Manrope uniquement (déjà chargé). Pas d'Inter, pas de serif de secours.

| Token | Size | Use |
|---|---|---|
| `--t-display` | `clamp(36px, 5.2vw, 64px)` | H1 accueil |
| `--t-h1` | `clamp(30px, 4.2vw, 48px)` | H1 pages |
| `--t-h2` | `clamp(26px, 3.2vw, 38px)` | Titres de section |
| `--t-h3` | `clamp(20px, 2.2vw, 26px)` | Tuiles, listes |
| `--t-body` | `16px` / `17px` lead | Corps, `line-height: 1.65`, max `46ch`–`65ch` |
| `--t-small` | `13px`–`14px` | Notes, captions |
| `--track-display` | `-0.025em` | Display et H2 |

Poids : 500 nav, 600 boutons et titres de tuiles, 700 H1/H2. `text-wrap: balance` sur les titres.

## 4. Space

Échelle unique. Pas de `padding: 12px 0` improvisé.

| Token | Value |
|---|---|
| `--s1` | `8px` |
| `--s2` | `12px` |
| `--s3` | `16px` |
| `--s4` | `24px` |
| `--s5` | `32px` |
| `--s6` | `48px` |
| `--s7` | `64px` |
| `--space-section` | `clamp(64px, 7vw, 80px)` |
| `--space-block` | `64px` |
| `--space-cta` | `48px` |
| `--btn-h` | `56px` |
| `--maxw` | `1180px` |
| `--gutter` | `24px` (16px sous 480px) |

Rythme interne d'un bloc split (titre + texte + bouton + image) :

1. H2 → `--s3` sous le titre
2. Lead → `--s5` sous le paragraphe
3. Bouton et note sur **la même ligne** (`align-items: center`, gap `--s3`)
4. Image à droite, `align-items: center`, ratio **4/3** (pas 3/4, ça décale tout)

Entre deux sections sœurs : `--s6` ou `--s7`, un seul filet. Pas `--space-block` empilé deux fois.

## 5. Shape and motion

- Cadres photo : rayon `--r-frame` `4px`, padding `--s2`–`--s3`, fond `--mat`
- Boutons : pill `--r-pill` `999px`, hauteur `--btn-h`
- Hover : `transform` uniquement, courbe `--ease` `cubic-bezier(.32, .72, 0, 1)`
- Pas d'animation de `padding` / `left` / `height`
- `prefers-reduced-motion: reduce` coupe les loops (pile polaroid)

## 6. Components

**Bouton primaire `.btn`** — orange, Contact / rendez-vous seulement.

**Bouton secondaire `.btn2`** — contour encre, configurateur et liens secondaires.

**Filet de section** — `border-top: 1px solid` via `--line`, pas une carte blanche.

**Liste métier `.p-list`** — titre + texte, 2 colonnes dès 900px. Pas de puces. Pas de filet haut **et** bas sur chaque ligne : un `border-bottom` suffit. Hover = `translateX(6px)`, pas `padding-left`.

**Mosaïque atelier `.metier`** — 6 cellules, 2 mises en avant (col 1), 4 compactes. Photo réelle + titre + une ligne. Lien vers la page. Mobile : une colonne.

**Split devis `.p-cta--rich`** — copie à gauche, photo 4/3 à droite. Pas de liste d'étapes sous le bouton (ça casse le rythme).

**Hero accueil** — air sous nav 24–36 px desktop, 20–28 px mobile. Voir `QA-UI.md`.

## 7. Layout families (une fois par page)

Ne pas enchaîner trois splits image/texte. Sur l'accueil : hero split → grille 4 services → story split → mosaïque → devis split (la mosaïque casse la répétition).

## 8. Copy

« nous », jamais « on ». Pas de tiret cadratin. Orange = Contact.

## 9. Interdit

3 cartes identiques, puces nues sur 6 métiers, image 3/4 collée à un pavé plus court, `padding-top: 0` sur le hero, deuxième couleur d'accent, Inter, emojis, « Elevate / Seamless ».
