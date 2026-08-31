# Art'Cadres Luxembourg — site statique

Site vitrine statique (HTML/CSS), sans dépendance Shopify.

## URL live (à utiliser)

**https://jfeosjfosi.github.io/artcadres-luxembourg/**

> `artcadres.lu` affiche encore l’**ancien WordPress** (hébergement o2switch). Ce n’est pas le nouveau site. Ne pas utiliser ce domaine tant que le DNS n’a pas été basculé.

- Pages générées par `build.py` (contenu réel du thème d'origine).
- `styles.css` : styles partagés.
- `assets/` : images et logos.

## Régénérer

```bash
python3 fetch_logos.py   # logos partenaires (Wikimedia + wordmarks)
python3 build.py
git add -A && git commit -m "..." && git push   # GitHub Pages se met à jour (~1 min)
```

## Aperçu local

```bash
python3 -m http.server 8765
# http://localhost:8765
```

## Plus tard : domaine artcadres.lu

Quand le client voudra remplacer l’ancien site sur `artcadres.lu` :

**Option A — GitHub Pages (gratuit)**  
Remplacer l’IP DNS `109.234.162.35` par les 4 IP GitHub Pages, ajouter `CNAME` `artcadres.lu` au repo, mettre `SITE_URL=https://artcadres.lu` dans `build.py`.

**Option B — o2switch (FTP)**  
`export FTP_USER=... FTP_PASS=... && ./deploy-o2switch.sh`
