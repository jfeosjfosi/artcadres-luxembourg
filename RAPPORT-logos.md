# RAPPORT — scales optiques logos (manuel)

`optical_logos.py` a échoué : ImageMagick ne peut pas rasteriser les SVG texte (`courducale`, `bnl`, `maisonheler`, etc.) — erreur `unable to read font`. Seuls Deloitte, Accor et SES ont été mesurés (area ~30–38k px² → scale clampé à **0.72**).

Recommandations visuelles (1440px + 390px, screenshots) pour alignement **optique** :

| Logo | État actuel | `transform:scale()` recommandé | Notes |
|------|-------------|-------------------------------|-------|
| Deloitte | **Trop grand** (masse visuelle dominante) | **0.82** (actuel 1.08) | Réduire aussi `max-height` à 22px |
| Accor | Légèrement petit | **1.05** (actuel 1.12) | Bird icon + texte fins |
| SES | **Trop grand** | **0.88** (actuel 1.15) | Wordmark + picto très massifs |
| Cour grand-ducale | **Trop petit** / léger | **1.18** | Deux lignes, faible encre |
| BNL | **Trop petit**, lisible mais pas coupé | **1.14** | `max-height: 50px` ; pas de clip |
| Maison Heler | **Le plus petit** du strip | **1.28** | Serif léger, une seule ligne |
| SODIKART | OK | **1.00** (actuel 1.05) | Référence médiane |
| M.Chat | OK | **1.05** (actuel 1.10) | Légère réduction possible |

CSS cible (à intégrer dans `styles.css` ou `logo-scales.css`) :

```css
.logosvg--deloitte { transform: scale(0.82); max-height: 22px; }
.logosvg--accor    { transform: scale(1.05); }
.logosvg--ses      { transform: scale(0.88); max-height: 28px; }
.logosvg--cour     { transform: scale(1.18); }
.logosvg--bnl      { transform: scale(1.14); max-height: 50px; }
.logosvg--heler    { transform: scale(1.28); }
.logosvg--sodikart { transform: scale(1.00); }
.logosvg--mchat    { transform: scale(1.05); }
```

Fix script : remplacer les SVG `<text>` par chemins vectoriels, ou configurer une police pour ImageMagick (`MAGICK_FONT_PATH`), pour automatiser via `optical_logos.py`.
