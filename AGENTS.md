# Art'Cadres Luxembourg — instructions agents

Site statique dans `artcadres-site/` (généré par `python3 build.py`).

## SEO (claude-seo v2)

Skills installés dans `.claude/skills/` (AgriciDaniel/claude-seo). Pour Cursor, invoquer le skill `seo` avant tout audit ou enrichissement SEO.

**Contexte projet :**
- Cible : encadreur d'art premium + B2B institutions (Luxembourg, Hollerich)
- Différenciateurs : Maison Neumann depuis 1972, références Deloitte/Accor/SES/BNL/Cour grand-ducale, configurateur Nielsen, restauration agréée MH
- Rapports : `artcadres-site/SEO-CONCURRENTS.md`, `artcadres-site/SEO-STRATEGIE.md`
- Preview : https://jfeosjfosi.github.io/artcadres-preview/

**Commandes utiles :**
- `/seo audit` — audit technique + contenu sur le site preview
- `/seo schema` — valider JSON-LD LocalBusiness
- `/seo local` — GBP, citations, avis
- `/seo content-brief` — briefs blog (ne pas publier sans validation client)

**Copy :** toujours « nous », jamais « on ». Orange CTA = Contact uniquement.

**Build :** `cd artcadres-site && python3 fetch_logos.py && python3 sync_assets.py && python3 build.py`
