# Stratégie SEO 20/80 — Art'Cadres Luxembourg

**Date :** septembre 2026  
**Sources :** `SEO-CONCURRENTS.md`, inventaire client, skill claude-seo (`.claude/skills/seo/`)

---

## 1. Principe 20/80

Sur un marché local (~5 acteurs), **10 requêtes transactionnelles** concentrent ~80 % du trafic qualifié. Le reste = longue traîne (Hollerich, objets, médailles, etc.).

| Prio | Requête | Page | Statut |
|:----:|---------|------|--------|
| 1 | encadreur luxembourg | index | ✅ H1 + schema |
| 2 | encadrement luxembourg | index + sur-mesure | ✅ maillage |
| 3 | cadre sur mesure luxembourg | encadrement-sur-mesure | ✅ enrichi |
| 4 | encadrement d'art luxembourg | index | ✅ B2B |
| 5 | restauration tableau luxembourg | dorures-restauration | ✅ MH |
| 6 | dorure cadre luxembourg | dorures-restauration | ✅ |
| 7 | cadre nielsen luxembourg | encadrement-standard | ✅ |
| 8 | encadrement grand format | index + institutions | ✅ |
| 9 | devis encadrement en ligne | configurateur | ✅ |
| 10 | encadrement entreprise institution | institutions-entreprises | ✅ **nouvelle page** |

---

## 2. Implémenté dans la refonte (build.py)

- **JSON-LD** : `ProfessionalService` + `LocalBusiness` (index, contact), `FAQPage` (index)
- **sitemap.xml** + **robots.txt** + **llms.txt** (GEO / IA)
- **Meta titles/descriptions** optimisés par page (≤ 60 / 155 car.)
- **Page Institutions & entreprises** — 8 cas clients nommés (trust B2B unique au LU)
- **24 images galerie** synchronisées depuis WeTransfer + refs client
- **4 vignettes** sous bandeau logos (Deloitte, Accor, SES, BNL)
- **Teaser galerie** accueil (6 visuels)
- **Copy B2B** : « nous », grands formats, heritage 1972, agrément MH

---

## 3. Concurrents — angles à tenir

| Concurrent | Leur force | Notre réponse (sans les nommer) |
|------------|-----------|----------------------------------|
| L'Éclat de Verre | 165+ avis, 48h | Atelier artisan + complexe + institutions |
| In Octavo + Nombre d'Or | Patrimoine Route d'Esch | Agrément MH + galerie + 1972 + cas nommés |
| Création Plus | Volume retail | Premium sur mesure, pas du stock |
| Création Plus / In Octavo | Années 1992/1982 | **Maison Neumann depuis 1972** |

---

## 4. Actions post-lancement (hors site)

1. **Google Business Profile** — catégories Encadreur + Restauration d'œuvres ; photos atelier + installations
2. **Campagne avis** — objectif rattraper L'Éclat de Verre (165+) sur la fiche Art'Cadres
3. **Migration DNS** artcadres.lu → GitHub Pages avec 301 WordPress
4. **Search Console** — soumettre sitemap, surveiller requêtes Hollerich / grand format

---

## 5. Blog — architecture recommandée (NE PAS IMPLÉMENTER EN V1)

Le blog n'est **pas** dans le build actuel. Voici le plan pour une V2 quand le client valide.

### Pourquoi un blog (plus tard)

- Tous les concurrents locaux ont **zéro contenu éditorial** → opportunité longue traîne
- Renforce E-E-A-T (Kathia Neumann, Sylvie Schied agréée MH)
- Alimente FAQ schema et maillage vers pages conversion

### Structure technique proposée

```
artcadres-site/
  blog/
    posts/           # fichiers .md (frontmatter YAML)
      2026-encadrer-oeuvre-luxembourg.md
      ...
  build.py           # étendre : génère blog/index.html + blog/<slug>.html
  sitemap.xml        # inclure URLs /blog/*
```

**Frontmatter exemple :**
```yaml
---
title: "Comment encadrer une œuvre d'art au Luxembourg"
description: "..."
date: 2026-10-01
keywords: [encadrement luxembourg, verre musée]
cta: contact.html
---
```

**Génération :** même pipeline que les pages légales (`contenu-a-coller/`) — markdown → HTML statique, pas de CMS.

### Silo éditorial (3–5 articles/an suffisent)

| Thème | Mot-clé cible | Lien interne |
|-------|---------------|--------------|
| Guide encadrement | encadrer tableau luxembourg | sur-mesure |
| Verre & conservation | verre musée vs standard | standard + dorures |
| Entreprises | cadre collection corporate | institutions |
| Grands formats | panneau mural encadrement | index GF |
| Restauration | restauration tableau signes usure | dorures |

### Navigation

- Lien discret footer « Guides & conseils » → `/blog/`
- Pas dans la nav principale (éviter dilution conversion)

### Schema blog

- `Article` + `author` (Kathia Neumann) + `datePublished`
- `BreadcrumbList`

**Décision :** attendre validation client + 2–3 briefs rédigés manuellement avant d'activer le générateur blog dans `build.py`.

---

## 6. Skill SEO installé

- Repo : [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) **v2.2.5**
- Runtime : `~/.claude/skills/seo/bin/claude-seo` (`doctor` : ready, Chromium OK, 2026-09-01)
- Skills projet : `.claude/skills/` + `.cursor/skills/artcadres-seo/SKILL.md`
- **Plan de ranking phase par phase :** [`SEO-PLAN-RANKING.md`](SEO-PLAN-RANKING.md) (audit live + battre le benchmark LU)

**Usage :** `/seo audit https://artcadres.lu` après cutover DNS. Preview : GitHub Pages.

---

## 7. KPIs à 90 jours

- Top 3 sur « encadreur luxembourg » et « encadrement luxembourg »
- Impressions GSC sur requêtes B2B (institution, grand format)
- 30+ nouveaux avis Google
- Taux clic contact / institutions > configurateur (objectif B2B)
