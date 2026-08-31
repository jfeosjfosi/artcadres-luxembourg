# Art'Cadres Luxembourg — site statique

Site vitrine statique (HTML/CSS), sans dépendance Shopify.

- Pages générées par `build.py` (contenu réel du thème d'origine).
- `styles.css` : styles partagés.
- `assets/` : images et logos.

## Régénérer

```bash
python3 fetch_logos.py   # logos partenaires (Wikimedia + wordmarks)
python3 build.py
```

## Aperçu local

```bash
python3 -m http.server 8765
# http://localhost:8765
```
