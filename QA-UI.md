# QA UI — Art'Cadres (ne pas livrer à l’aveugle)

Règle projet : **aucun changement visuel n’est terminé** tant qu’il n’a pas été vu en **desktop et mobile**, avec captures à l’appui.

Les sous-agents UI screenshot **les deux** formats. Ils ne rendent pas tant que ce n’est pas juste. Boucle : corriger → recapturer → relire les PNG.

## Formats obligatoires

| Format | Viewport | À faire |
|---|---|---|
| Desktop | 1440 × 900 | Screenshot de la zone changée + mesure (gaps, hauteurs) |
| Mobile | 390 × 844 | Idem, plus hamburger / stack vertical |

Pas de « ça devrait aller ». Pas de screenshot desktop seul. Pas de `reducedMotion` si on vérifie une animation (`no-preference`).

## Boucle (infinite feedback)

1. Changer le code.
2. `python3 build.py` si le HTML est généré.
3. Capturer desktop **et** mobile (Playwright ou équivalent).
4. **Lire** les PNG. Mesurer : header → hero, boutons, overflow, crops.
5. Si un format est faux : corriger, **revenir à 3**. Ne pas pousser.
6. Seulement alors : commit + push origin **et** preview.

S’ils rendent un audit sans captures des deux formats, relancer.

## Accueil — critères hero

- **Air sous la navbar** : 24–36 px desktop, 20–28 px mobile (ni collé, ni gouffre). Ne jamais mettre `padding-top: 0` sur `#acc .p-hero-home`.
- **Pile polaroid** : la carte du dessus glisse sur le côté **dans** le tas, passe derrière (`is-exit` puis `is-tuck`), opacity toujours `1`. Pas de disparition, pas de carte coupée par `overflow-x: clip` sur html/body.
- Google avis au-dessus du H1.

## Commande type

```text
Playwright 1440×900 + 390×844, fullPage false, zone hero.
Mesurer header.bottom vs .p-gtrust.top et vs .polaroids.top.
Animation : 3 frames (repos, is-exit, après tuck), opacity === 1, clippedRight === false.
```
