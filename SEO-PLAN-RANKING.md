# Plan de ranking — Art'Cadres vs concurrence Luxembourg

**Date :** 1er septembre 2026  
**Outil :** claude-seo v2.2.5 (AgriciDaniel) — runtime isolé, Chromium OK  
**URL auditée :** https://jfeosjfosi.github.io/artcadres-preview/  
**Type détecté :** service local hybride (atelier Hollerich + pose sur site / Grande Région)  
**Score santé SEO (0–100) :** **70**  
**Objectif 90 jours :** Top 3 pack local + organique sur `encadreur luxembourg` et `encadrement luxembourg`, devant Création Plus et In Octavo, et rattrapage avis vs L'Éclat de Verre.

Sources : audit live (robots, sitemap, titles, schema, `llms.txt`, parse HTML, content quality 87/100 accueil), `SEO-CONCURRENTS.md`, `SEO-STRATEGIE.md`, Whitespark 2026 (GBP 32 % du pack, avis ~20 %).

APIs non branchées (à faire Phase 0) : Google Search Console, PageSpeed/CrUX, GA4, Moz, Bing Webmaster. PSI public = quota épuisé ce jour. Ne pas inventer des CWV de terrain.

---

## 0. Ce qui est déjà fort (ne pas casser)

- Hub + 9 silos indexables, `robots.txt` Allow, sitemap 10 URLs, `index,follow`, HTTPS + HSTS GitHub.
- H1 unique par page, title/description présents, `og:locale` `fr_LU`.
- JSON-LD `ProfessionalService` + `LocalBusiness` (NAP, geo, horaires mer–sam 10–18, `foundingDate` 1972) + `FAQPage` accueil (10 Q, rich results FAQ Google retirés mai 2026 : **Info**, ne pas supprimer).
- `llms.txt` pour ChatGPT / Perplexity / AI Overviews.
- Différenciateurs uniques vs le marché LU : **1972**, **cas nommés** (Deloitte, Accor, SES, BnL, Cour), **configurateur Nielsen**, **restauration agréée MH (Sylvie Schied)**, Click & Collect 1 h.
- Accueil : ~1250 mots, content-quality **87**, 7 H2 alignés intention.

**THINK :** sur un marché de 5 acteurs peu digitalisés, le site n'est plus le goulot. Le pack Maps et les avis le sont.

---

## 1. Score par catégorie (pondération claude-seo)

| Catégorie | Poids | Score | Commentaire |
|-----------|------:|------:|-------------|
| Technical SEO | 22 % | 78 | Crawl OK. Canonical = github.io, pas le domaine marque. Pas d'IndexNow. Headers sécurité GitHub-only. |
| Content Quality | 23 % | 65 | Accueil OK. Silos sous le seuil 800 mots (quality-gates). Flag « repetitive » accueil. |
| On-Page | 20 % | 68 | Titles plusieurs > 60 car. Parseur : 3 images strip boutique `alt=""`. Pas de fil d'Ariane. |
| Schema | 10 % | 72 | LocalBusiness solide. Manquent `BreadcrumbList`, `Service` sur silos, `AggregateRating`, `hasMap`, `sameAs` Google. |
| Performance (CWV / INP) | 10 % | 55 | Non mesuré (PSI 429). Risque LCP polaroids hero + iframe Nielsen. |
| AI Search / GEO | 10 % | 82 | `llms.txt` + FAQ citables. Manque Person schema Kathia / Sylvie. |
| Images | 5 % | 70 | Lazy OK. 3 alt vides accueil. Pas de width/height → CLS. |
| **Santé** | 100 % | **70** | |

### Qualité de contenu vs seuils claude-seo (mots HTML totaux, chrome nav/footer inclus)

Rebuild Phase 1 (1er sept. 2026) :

| Page | Mots | Seuil page type | Verdict |
|------|-----:|----------------:|---------|
| Accueil | 1259 | 500 | OK |
| Sur mesure | 809 | 800 service | OK |
| Standard | 805 | 800 service | OK |
| Dorures | 803 | 800 service | OK |
| Institutions | 801 | 800 / 600 landing | OK |
| Configurateur | 605 | 600 landing | OK |
| Histoire | 462 | 400 about | OK |
| Contact | 413 | 400 | OK |
| Galerie | 400 | 400 | OK |
| Partenaires | 400 | 400 | OK |

**ACCEPT (échec) :** si dans 30 jours GSC n'indexe pas les 10 URLs sitemap, ou si `site:artcadres.lu` (après cutover) ne renvoie pas le H1 accueil.

---

## 2. Comment on éclate le benchmark

Le pack local (Maps) pèse plus que « plus de blog ». Ordre d'attaque :

| Concurrent | Ils gagnent aujourd'hui par | Notre coup pour les dépasser |
|------------|-----------------------------|------------------------------|
| **L'Éclat de Verre** | 165+ avis, 48 h, landing Howald | Volume + vélocité d'avis (88 → 150), GBP photos/Q&A, copy « montage complexe / institutions » sans les nommer |
| **Création Plus** | Autoproclamé « leader », stock, site mince | 1972 + MH + logos C-level + silos plus longs que leur vitrine |
| **In Octavo + Nombre d'Or** | 1982, musées génériques, Route d'Esch | Antériorité 1972, **clients nommés**, configurateur, avis publics, Sylvie Schied MH plus visible |
| **Lucien Schweitzer** | Luxe déco, encadrement noyé | Page dédiée déjà là ; viser `encadrement d'art luxembourg` + galerie |
| **Nielsen online** | Configurateur national | Atelier + pose + restauration = ce que le site .fr ne fait pas |

**CONNECT :** un site parfait sans GBP / avis perd le pack (32 % + 20 %). Un GBP parfait avec un site thin perd l'organique long terme. Les deux, dans cet ordre.

---

## Phase 0 — Jours 1 à 3 : débloquer l'indexation marque

**Pourquoi en premier :** Google et les IA citent `artcadres.lu`, pas `github.io`. Tant que le canonical pointe vers Pages, on donne de l'autorité à une URL jetable.

| # | Action | Qui | Falsifiabilité | Leading indicator |
|---|--------|-----|----------------|-------------------|
| 0.1 | DNS `artcadres.lu` → GitHub Pages (ou Pages custom domain). 301 de **toutes** les URLs WordPress. | Tech | `curl -I https://artcadres.lu` = 200. Anciennes URLs WP = 301. | Couverture GSC « pages connues » |
| 0.2 | `SITE_URL` dans `build.py` = `https://artcadres.lu` (canonical, OG, schema, sitemap, llms.txt). Rebuild + push. | Tech | View-source canonical = artcadres.lu | GSC « canonical déclarée » |
| 0.3 | Search Console : propriété domaine, sitemap, Inspection URL accueil + 9 silos. | SEO | 10 URLs « indexée » sous 14 j | Impressions semaine 2 |
| 0.4 | Bing Webmaster + IndexNow (clé dans le repo, ping à chaque push). | Tech | Rapport Bing « URL soumises » | Découverte Bing < 7 j |
| 0.5 | GA4 + events (clic tel, mailto, configurateur, contact). Consent mode si cookies. | Tech | Realtime voit un clic Contact | Taux conversion organique |
| 0.6 | Config claude-seo : `~/.config/claude-seo/google-api.json` (PSI/CrUX) + GSC OAuth. | SEO | `claude-seo run google_auth.py --check` vert | CWV **INP** (pas FID) |
| 0.7 | Moz gratuit + Bing backlinks. | SEO | `backlinks_auth.py --check` tier > 0 | Referring domains |

**Dépendance :** 0.1 → 0.2 → 0.3. Ne pas enrichir le contenu tant que le domaine n'est pas la canonical.

---

## Phase 1 — Semaine 1 : on-page + schema (code, impact organique immédiat)

**Pourquoi :** les silos existent déjà ; ils sont trop courts et mal marqués. C'est le levier le plus rapide **sur le site**.

### 1.1 Titles ≤ 60 caractères — **fait (code, 2026-09-01)**

| Page | Actuel (~car.) | Cible |
|------|----------------|-------|
| Accueil | 63 | `Encadreur d'art à Luxembourg · Art'Cadres` |
| Institutions | ~62+ | `Encadrement entreprises Luxembourg · Art'Cadres` |
| Galerie | ~58–68 | `Galerie d'art encadrée Luxembourg · Art'Cadres` |
| Configurateur | ~60+ | `Devis cadre en ligne Luxembourg · Art'Cadres` |
| Dorures / Histoire / Partenaires | ~63 | Couper le sous-titre redondant |

### 1.2 Enrichir les silos jusqu'au seuil 800 mots uniques (service) — **fait (code, 2026-09-01)**

Sans blog. Texte « nous », preuves, process, CTA.

- **Sur mesure** : Marie-Louise, caisse américaine, rehausse, objets, budget, lien configurateur + contact.
- **Dorures** : process diagnostic, MH, Sylvie Schied (Person), avant/après légendés, vs simple nettoyage.
- **Standard** : aluminium vs bois, FSC, Allemagne, C&C 1 h, pour qui ce n'est **pas** le sur-mesure.
- **Institutions** : process devis B2B, rayon 25 km, confidentialité, 1 cas par logo (déjà 8 cartes : allonger le corps).
- **Configurateur** : 400+ mots autour de l'iframe (quoi, pour qui, limites, quand venir à l'atelier).

### 1.3 Schema à ajouter (pas HowTo ; FAQ existante = Info) — **fait (code, 2026-09-01)**

`sameAs` GBP : **pas inventé** (Phase 0/2). Facebook conservé.

- `BreadcrumbList` sur chaque silo.
- `Service` lié à `#localbusiness` : sur-mesure, Nielsen, restauration, institutions.
- `AggregateRating` : 4,9 / 88 (même source que le pill Google).
- `hasMap` + embed Google Maps sur `contact.html` (aujourd'hui **pas d'iframe Maps**).
- `sameAs` : fiche GBP, Facebook (déjà), Instagram si réel.
- `Person` : Kathia Neumann (fondatrice), Sylvie Schied (restauratrice MH).
- `addressLocality` : préciser Hollerich (quartier) en plus de Luxembourg.
- `areaServed` : Luxembourg-Ville, Hollerich, Howald, Grande Région (pas 30 landing villes).

### 1.4 Images — **fait (code, 2026-09-01)**

- Alts vides accueil : `ac-contact.jpg`, `ac-histoire.jpg`, `histoire-atelier-1.jpg` (strip boutique).
- `width` / `height` ou aspect-ratio déjà CSS : ajouter attributs pour CLS.
- OG image unique par silo (déjà partiellement).

### 1.5 Maillage — **fait (code, 2026-09-01)**

- Accueil → Sylvie / restauration dans le bloc métiers (ancre).
- Footer / silos : Hollerich, Howald, « 25 km » une fois, pas doorway.
- Configurateur toujours `btn2`, Contact orange.

**ACCEPT :** titles non tronqués dans l'outil SERP ; Rich Results Test = LocalBusiness + Breadcrumb sans erreur ; aucun silo service < 800 mots uniques hors nav/footer.

**GROW :** CTR GSC accueil + silos (cible +20 % en 30 j post-cutover).

---

## Phase 2 — Semaines 1 à 4 : Google Business Profile + avis (le plus vite pour le pack)

**Pourquoi :** Whitespark 2026 : GBP **32 %**, avis **~20 %**. L'Éclat gagne Howald ici, pas avec un meilleur atelier.

Catégorie primaire : **Encadreur** (erreur n°1 du pack = mauvaise catégorie).  
Secondaires : restauration d'œuvres, magasin d'art / galerie si pertinent.

| # | Action | Détail |
|---|--------|--------|
| 2.1 | Audit fiche (nom, cat, NAP = site) | Nom : `Art'Cadres Luxembourg` (pas de keyword stuffing dans le title) |
| 2.2 | Description 750 car. | 1972, Hollerich, MH, institutions, C&C 1 h, mer–sam 10–18 |
| 2.3 | Services GBP | Sur mesure, Nielsen, restauration, dorure, pose grand format, galerie |
| 2.4 | 20+ photos | Extérieur, Kathia, mur baguettes, portraits officiels, Deloitte (autorisation), produits |
| 2.5 | Produits / posts | 1 post / semaine (réalisation, horaire, offre C&C) |
| 2.6 | Q&A GBP | Recopier les 10 FAQ du site |
| 2.7 | Attributs | Femme dirigeante, RDV, accessibilité si vrai |
| 2.8 | UTM | `google/maps` sur le site URL de la fiche |
| 2.9 | Campagne avis | QR atelier, SMS J+3, réponse **100 %** sous 48 h. Objectif **+30 avis / 60 j** (88 → 118), puis 150 pour coller Éclat |
| 2.10 | Review velocity | 2–4 avis / semaine, pas 20 d'un coup |

**ACCEPT :** pack local « encadreur luxembourg » depuis Hollerich **et** Kirchberg (2 points) : position mesurée (captures Maps). Si inchangé à 45 j, revoir catégorie + densité photos + avis, pas le copy du site.

**GROW :** appels + itinéraires GBP (insights hebdo).

---

## Phase 3 — Semaines 2 à 4 : citations NAP (IA + pack)

3 des 5 facteurs d'**AI visibility** locale sont citation-related (BrightLocal / skill local).

Annuaires LU / région, **NAP identique** au schema :

1. LuxYello  
2. Editus / Pages d'Or LU  
3. Petit Futé  
4. Europages (B2B, In Octavo y est)  
5. Apple Maps / Bing Places  
6. Chambre des métiers / traces officielles si déjà inscrits  
7. Nielsen success-story (demander une fiche revendeur)  
8. Partenaires FR déjà listés : lien retour si possible (Misterblad, Claude Samuel, etc.)

Pas de spam 200 directories. 8–15 citations propres > 80 poubelles.

**ACCEPT :** 8 citations NAP byte-identiques. Outil : table dans ce dossier `citations-nap.md` (à créer en exécutant).

---

## Phase 4 — Mois 1 : contenu d'intention (sans blog, sans doorway)

Interdit : 30 pages « encadreur [ville] » (hard stop skill à 50, warning à 30).

Autorisé, **une** page zone unique si vraiment du contenu distinct :

- Section / page **« Luxembourg-Ville, Hollerich, Howald, pose 25 km »** sur contact ou institutions : parking, Route d'Esch, vs Howald (3 ateliers sud) **sans nommer** les concurrents.
- Bloc accueil déjà métier : OK.
- **Avant/après restauration** (3 paires) : E-E-A-T visuel vs In Octavo.
- FAQ déjà 10 objections : garder, ne pas gonfler pour Google.

**ACCEPT :** 0 nouvelle URL ville template. GSC requêtes contenant `hollerich` ou `howald` > 0 impressions à 45 j.

---

## Phase 5 — Mois 2 : autorité (liens)

Le skill note les liens **en baisse** dans le pack, utiles en organique + E-E-A-T.

1. Page Nielsen « revendeur Luxembourg » (lien dofollow).  
2. Mention BnL / communiqué (si projet public).  
3. Chambre, visites atelier, école d'art LU.  
4. 2–3 articles presse LU (Paperjam, Virgule) : institutions + 1972.  
5. Common Crawl / Moz : baseline referring domains, puis +5 domaines / 90 j.

**ACCEPT :** Moz/CC referring domains +5 nets, 0 lien toxique massif.

---

## Phase 6 — GEO / IA (en parallèle dès Phase 1)

Déjà : `llms.txt`, FAQ, cas nommés.

À faire :

- `Person` + citations « Kathia Neumann, Art'Cadres, Hollerich ».  
- Réponses courtes type définition en tête de silo (citable Perplexity).  
- Vérifier `llms.txt` après cutover d'URL.  
- Ne pas vendre FAQPage comme rich result Google.

**GROW :** tests mensuels « encadreur luxembourg » sur ChatGPT / Perplexity / AI Overview. Noter si Art'Cadres est cité (45 % des reco locales passent par l'IA, BrightLocal 2026).

---

## Phase 7 — Blog (gate client, pas V1)

Voir `SEO-STRATEGIE.md` §5. **Ne pas publier** sans validation.

Quand validé, 3–5 URLs / an suffisent (concurrents = 0 éditorial) :

1. Encadrer une œuvre au Luxembourg (verre, conservation)  
2. Grand format entreprise / pose site  
3. Restauration : signes d'usure, MH  
4. Nielsen bois vs alu  

Schema `Article` + `author` Kathia. Lien footer « Guides », pas la nav.

---

## Phase 8 — Mesure 90 jours (KPIs)

| KPI | Baseline auj. | 30 j | 90 j |
|-----|---------------|------|------|
| Pack « encadreur luxembourg » (Hollerich) | à photographier | Top 5 | Top 3 |
| Organique même requête | top 3 déjà (benchmark interne) | #1–2 | #1 |
| Avis Google | 88 / 4,9 | 100+ | 150 / ≥ 4,8 |
| Impressions GSC `institution` / `grand format` | 0 connu | > 0 | croissance |
| Clics Contact vs Configurateur | GA4 à brancher | Contact ≥ config | B2B |
| Santé claude-seo | 70 | 78 | 85 |
| INP / LCP mobile | inconnu | LCP < 2,5 s, INP < 200 ms | tenir |

Re-audit : `/seo audit https://artcadres.lu` + `/seo local` + `/seo drift compare` après cutover.

---

## Backlog code (ordre d'implémentation site)

1. `SITE_URL` + canonical domaine. **Bloqué Phase 0.1** (DNS). Canonical reste github.io tant que artcadres.lu n'est pas live.  
2. Titles courts. **Fait.**  
3. Alts strip boutique. **Fait.**  
4. Maps embed contact. **Fait.**  
5. Schema Breadcrumb + Service + AggregateRating + Person. **Fait.** (`sameAs` GBP non inventé.)  
6. Copy silos 800+ mots. **Fait** (rebuild + compte mots).  
7. IndexNow : fichier clé à la racine. **Fait.** Ping live après cutover (github.io peut 403).  
8. Width/height images LCP. **Fait.**  
9. Configurateur : texte autour iframe. **Fait.**  
10. `sameAs` GBP. **Hors code** (URL fiche à coller après audit Phase 2).

Hors code : GBP, avis, citations (`citations-nap.md` créé), 301, GSC.

---

## Ce que claude-seo n'a pas pu mesurer ici

- Positions SERP live (pas DataForSEO).  
- CWV **field** CrUX (pas de clé).  
- Indexation réelle GSC.  
- Profil de liens (Common Crawl cache vide au premier run).  
- Qualité de la fiche GBP (pas d'API Maps branchée).

Ces trous se ferment en Phase 0.6–0.7 et Phase 2.

---

## Synthèse une ligne

**Semaine 1 = domaine + schema + titles + silos plus longs. Semaines 1–4 = GBP et avis (c'est là qu'on dépasse L'Éclat). Mois 2 = citations et 5 backlinks propres. Blog seulement si le client dit oui.**
