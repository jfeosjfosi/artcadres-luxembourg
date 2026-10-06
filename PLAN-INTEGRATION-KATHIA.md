# Plan d'intégration — batch Kathia (oct. 2026)

> Objectif : intégrer les **nouveaux textes** + les **nouvelles photos** que Kathia a envoyés
> (mail « textes retravaillés » + photos avec légendes de placement + 2 messages WhatsApp),
> sur le site `artcadres-site/` (généré par `build.py`), puis build + vérif + push.
>
> **Règles verrouillées** : zéro invention (chaque mot/photo vient de Kathia ou d'une source réelle) ·
> zéro « ! » en copy éditoriale · jamais « Maison Neumann » visible · note Google réelle = **4,7/5 · 12 avis** ·
> jamais `git add -A` (seulement `git add -u` + fichiers neufs explicites) · jamais `--force` ·
> « nous » jamais « on » · CTA orange = Contact uniquement.

---

## 0. Workflow mail — comment tu me forwardes tout (first try)

**Adresse de réception (boîte jetable mail.tm, créée et testée) :**

```
acadres496@maxxspace.com
```

- Forwarde **tous** les mails de Kathia (textes + photos en pièces jointes) à cette adresse.
- Je relève la boîte avec `python3 mailsweep.py` (depuis `Shopify Neumann/`) : ça télécharge le
  **corps** (`_mail.md`) + **toutes les pièces jointes en pleine qualité** dans `ArtCadres-refs/<sujet>__<id>/`,
  puis vide le mail (libère le quota).

**Limites connues & parades :**
- Quota boîte = **40 Mo**. Je relève souvent → la suppression après download libère la place, donc même
  beaucoup de photos passent tant qu'**un seul mail** ne dépasse pas ~35 Mo.
- iPhone envoie des JPEG de 2–4 Mo → ~10 photos / mail OK. Si Kathia a **beaucoup** de photos haute def
  d'un coup : qu'elle **forwarde en plusieurs mails** (5–8 photos chacun), ou qu'elle mette un
  **lien WeTransfer / Drive** dans le mail → je le télécharge direct (comme on avait fait pour les 47 photos).
- Si le domaine mail.tm tombe, je recrée une boîte et je te redonne l'adresse (registre `.mailtm-boxes`).
- Les photos tournées 90° (EXIF) : je les redresse à l'intégration.

---

## 1. Nouveaux TEXTES (du mail « textes retravaillés »)

⚠️ Le mail a été écrit avec une IA → il contient des **bouts de prompt** à NE PAS mettre en ligne :
- la partie méta « Cc ci joint les textes… Question le simulateur… Bises »
- la phrase « Oui, et c'est même intéressant : ça permet de positionner… Je tournerais le texte comme ça : »
  → c'est le commentaire de l'IA, **pas** du contenu site. Le vrai texte est celui qui suit (« CADRES STANDARDS »).

Segmentation → où va quoi dans `build.py` :

| Bloc du mail | Destination `build.py` | Statut |
|---|---|---|
| « Encadreur d'art à Luxembourg » (hero) | `accueil_body` hero `p-lead` | ✅ |
| « Un savoir-faire transmis depuis 1972 » | accueil `p-story` intro (home) | ✅ |
| « ENCADREMENT SUR MESURE » | `mesure_body` hero | ✅ |
| « CADRES STANDARDS / Nielsen » (⚠️ « ! » retiré) | `standard_body` hero | ✅ |
| « DORURE & RESTAURATION » | `dorures_body` hero | ✅ |
| « Encadrement pour entreprises & institutions » | `institutions_body` hero | ✅ |
| « Notre histoire » (page) | `hist_body` hero | ✅ |
| « De Metz à Luxembourg » + « Repères » (1972/1996/2014/2026) | `hist_body` story + `content_list` | ✅ |

Noms d'institutions dans les textes = Deloitte, Accor, SES, Bibliothèque nationale du Luxembourg
(✓ conforme : plus de « Cour grand-ducale »).

## 2. Nav — simulateur dans les premiers onglets
Kathia : « le simulateur il doit pas être dans les premiers onglets ? » → **oui**.
→ Déplacer le lien **Configurateur** juste après le menu « Encadrement » (3ᵉ position), au lieu d'avant Contact. ✅

## 3. « Retrait en 1 h » — à retirer / conditionner
Kathia : « enlever “retirer en 1 h”, mettre “en une heure” ou “en fonction des stocks disponibles” ».
→ Toutes les promesses de délai dur « en 1 h / en une heure / dans l'heure » remplacées par
**« selon les stocks disponibles »** (phrasing honnête, conditionné au stock). ~16 occurrences. ✅

## 4. Photo Bibliothèque — la montrer EN ENTIER
Kathia : « le cadre de la bibliothèque, dommage de l'avoir coupé ».
Diagnostic : l'asset `biblio-kathia.jpg` montre déjà le cadre entier (portrait), mais il est affiché
dans des cadres **paysage** (`#gf` = 4/3 cover) → haut/bas rognés.
→ Re-crop portrait serré (frame + Kathia) + affichage **`object-fit:contain`** sur fond crème
(effet passe-partout) partout où l'image apparaît. ✅

## 5. Nouvelles PHOTOS (à l'arrivée des mails)
À intégrer selon les légendes de placement de Kathia (elle indique où elle veut chaque photo).
WhatsApp (showroom Nielsen : mur d'échantillons, « Le choix du verre », Kathia à la table,
espace galerie murs blancs) → candidates pour **Espace d'exposition**, page **Cadres standards**, hero.
→ Traitées dès réception (redressement EXIF, recadrage, webp, placement), puis re-build + push.

## 6. Build, vérif, push
1. `python3 build.py`
2. Serveur local + **screenshots desktop 1440 + mobile 390** de chaque page touchée → je compare moi-même.
3. Correctifs jusqu'à ce que ce soit net (nav cliquable, 0 erreur JS, 0 overflow).
4. `git add -u` (+ assets neufs explicites) · commit · `git push origin main` + `git push preview main`.
5. Live : https://jfeosjfosi.github.io/artcadres-preview/

---

## Suivi
- [x] Boîte mail créée + adresse donnée
- [x] Textes segmentés + intégrés
- [x] Nav : configurateur en premier
- [x] « 1 h » → « selon les stocks disponibles »
- [x] Photo bibliothèque en entier
- [ ] Nouvelles photos du mail intégrées (en attente des forwards)
- [ ] Build + screenshots + push
