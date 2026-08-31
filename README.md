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

## Domaine artcadres.lu (GitHub Pages)

Le repo contient un fichier `CNAME` (`artcadres.lu`). Côté registrar DNS, pointer le domaine vers GitHub :

**Enregistrements A (apex `artcadres.lu`)** — remplacer l'IP actuelle (`109.234.162.35`) par :

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**Optionnel `www`** : CNAME `www` → `jfeosjfosi.github.io`

Après propagation DNS (jusqu'à 48 h), activer **Enforce HTTPS** dans GitHub → Settings → Pages. Le site répondra sur https://artcadres.lu/
