# SEO — Backlog & Stratégie · saibodanfakha.com

**Agence SEO (familiale) :** Raby (directrice) · Youssouf (technique) · Dialamba (contenu) · Mouhamed (local) · Lamine (autorité) · Fodé (analytics) · Bangaly (veille)
**Audit initial :** 2026-06-09 · **Objectif :** plus de visiteurs organiques qualifiés → plus de demandes de devis.

---

## 🩺 AUDIT INITIAL — état réel du site

### ✅ Déjà en place (bonnes bases)
- Balises `<title>`, `description`, `canonical` par page (centralisées dans `src/layouts/Layout.astro`).
- Open Graph + Twitter Card + `og-image.jpg` (1200×630).
- Schema.org `ProfessionalService` (geo, areaServed, founder, langues).
- `google-site-verification` présent → **Search Console connectée**.
- `robots.txt` + `sitemap.xml` + `manifest.json` + favicon.
- Blog actif, 1 article/mardi (6 articles publiés).

### 🔴 Problèmes trouvés (par priorité)

| # | Priorité | Problème | Pourquoi ça fait mal | Propriétaire |
|---|----------|----------|----------------------|--------------|
| 1 | **P0** | **Le blog est ABSENT du sitemap.** `public/sitemap.xml` est statique : il ne liste que la home + 6 études de cas. Aucune page `/blog` ni aucun article. `lastmod` figé au 2026-05-08. | C'est probablement **la cause n°1 du manque de visites** : le moteur de contenu (le blog) est quasi invisible pour Google. Les 6 articles ne sont pas signalés. | Youssouf |
| 2 | **P0** | **NAP incohérent.** Le schema.org indique localité **« Dakar »** (Saïbo est à **Kaolack**) et email **zifo1819@gmail.com** (le pro est **youmou@saibodanfakha.com**). | Le SEO local repose sur un NAP identique partout. Une incohérence = Google hésite et rétrograde. | Mouhamed (donnée) → Youssouf (édite) |
| 3 | **P0** | **Google Business Profile** à créer/optimiser. | Levier n°1 du SEO local (pack Maps). Gratuit, fort impact. | Mouhamed |
| 4 | **P1** | **hreflang trompeur** : déclare `fr`, `en` et `x-default` pointant tous vers la **même URL française**. Aucune version EN n'existe. | Google peut se méfier d'un hreflang qui ment. | Youssouf |
| 5 | **P1** | **Pas de schema Article/BlogPosting** sur les articles (seulement le `ProfessionalService` global). | On rate les rich results et la compréhension des articles par Google. | Youssouf |
| 6 | **P1** | **Stratégie mots-clés non formalisée.** Quelles pages visent quelles requêtes ? | Sans cible claire, on n'optimise rien précisément. | Dialamba + Bangaly |
| 7 | **P1** | **Baseline de mesure manquante.** | Impossible de prouver l'impact des actions sans état de départ. | Fodé |
| 8 | **P2** | Polices Google chargées en bloquant le rendu. | Léger impact vitesse/LCP. | Youssouf |
| 9 | **P2** | OG image unique pour toutes les pages (les articles ont pourtant des miniatures distinctes). | Partages sociaux moins percutants. | Youssouf |
| 10 | **P2** | Peu de citations/backlinks locaux. | Autorité de domaine faible. | Lamine |
| 11 | **P2** | Maillage interne entre articles à renforcer. | Diffuse mal le « jus » SEO et l'engagement. | Dialamba |

---

## 🗺️ STRATÉGIE 90 JOURS

### Phase 1 — Débloquer l'indexation (Semaines 1-2) · *fondations*
> Si Google ne voit pas le blog, rien d'autre ne compte. On répare la plomberie d'abord.
- [x] **[P0]** Sitemap auto incluant blog + articles — *Youssouf* → ✅ **Déjà résolu** : `@astrojs/sitemap` était actif, le sitemap live (`sitemap-0.xml`) liste déjà `/blog` + les 6 articles. L'audit décrivait un `public/sitemap.xml` statique qui n'existe pas/plus. ⚠️ Vraie piste restante = soumettre/vérifier l'indexation dans Search Console (→ Fodé).
- [x] **[P0]** Corriger le NAP dans le schema.org (Kaolack + email pro) — *Mouhamed → Youssouf* → ✅ localité déjà Kaolack ; email corrigé `zifo1819@gmail.com` → `youmou@saibodanfakha.com` (commit e3b6c52).
- [x] **[P0]** Créer/optimiser Google Business Profile (catégorie, zone, photos, lien) — *Mouhamed* → ✅ **fiche publiée par Saïbo le 2026-06-14** (catégorie « Concepteur de sites Web », zone de service Kaolack/Dakar/Thiès/Mbour, offres FCFA). Brief : `SEO/GBP-fiche-saibo.md`. Reste : vérification Google + 2-3 avis clients.
- [x] **[P1]** Corriger ou retirer le hreflang EN/x-default — *Youssouf* → ✅ hreflang trompeur retiré, build vert (commit e3b6c52).
- [ ] **[P1]** Relever la baseline Search Console (impressions, clics, position, pages indexées) — *Fodé* → ✅ chiffres consignés dans `SEO/MESURES.md`.

### Phase 2 — Contenu & autorité (Semaines 3-8) · *attaque*
- [x] **[P1]** Recherche de mots-clés cibles (Sénégal/diaspora) + mapping page↔mot-clé — *Dialamba* → ✅ Mapping v1 livré 11/06 (7 pages mappées, zéro cannibalisation). Voir section ci-dessous.
- [x] **[P1]** Analyse concurrentielle SERP : 5 opportunités à faible concurrence — *Bangaly* → ✅ Livré 11/06. Voir section ci-dessous.
- [x] **[P1]** Optimiser on-page des pages clés (home) : title/meta — *Youssouf* → ✅ commit `1a386b6` (11/06). Title homepage, meta description, kicker "Tarifs & offres".
- [~] **[P1]** Ajouter schema `BlogPosting` + `BreadcrumbList` aux articles — *Youssouf* → ✅ `BlogPosting` fait (commit e3b6c52). Reste `BreadcrumbList`.
- [x] **[P2]** Renforcer le maillage interne entre articles liés — *Dialamba/Youssouf* → ✅ commit `1a386b6` : lien "Voir les tarifs → /#offres" ajouté sur 6 articles. CTA box ajoutée sur site-one-page (manquait).
- [ ] **[P1]** Créer page `/freelance-web-kaolack` — *Youssouf + Dialamba* · opportunité géo-locale vierge (Bangaly).
- [ ] **[P1]** Créer page `/site-web-diaspora` — *Youssouf + Dialamba* · segment vierge, zéro concurrent direct (Bangaly).
- [ ] **[P1]** Enrichir article `comment-choisir-son-developpeur-web-freelance` avec contexte local sénégalais — *Dialamba*.
- [ ] **[P1]** Optimiser article `combien-coute-un-site-professionnel` : prix en FCFA, tableau comparatif, titre 2026 — *Dialamba*.
- [ ] **[P2]** Créer page `/site-web-association-diaspora` (après article 16/06) — *Youssouf + Dialamba*.
- [ ] **[P2]** Citations annuaires sénégalais + 3-5 backlinks de qualité (NAP cohérent) — *Lamine*.

---

## 🗺️ MAPPING MOTS-CLÉS v1 (Dialamba — 2026-06-11)

| Page | Mot-clé primaire | Intention |
|---|---|---|
| `/` | développeur web freelance Sénégal | Commerciale |
| `/#offres` | prix site web Sénégal | Transactionnelle |
| `/projets` | portfolio développeur web Sénégal | Commerciale |
| Blog — PME | créer un site web PME Sénégal | Informationnelle |
| Blog — Construction Canada | site web entreprise construction Canada | Commerciale |
| Blog — E-commerce | créer boutique en ligne Sénégal | Trans. + Info. |
| Blog — Refonte | refaire son site web Sénégal | Info. + Commerciale |
| Blog — Diaspora (16/06) | site web bilingue diaspora sénégalaise | Info. + Commerciale |

## 🔍 OPPORTUNITÉS SERP (Bangaly — 2026-06-11)

**Concurrents freelances identifiés :** doroniasse.com · elhadji-dieng.com · djibril.dev
**Angle gagnant :** "le freelance web qui comprend Kaolack et la diaspora" — territoire vierge, authentique, atteignable en 3-6 mois.

| # | Mot-clé | Concurrence | Action | Priorité |
|---|---|---|---|---|
| 1 | `freelance web Kaolack` | Faible | Créer `/freelance-web-kaolack` | 🔴 HAUTE |
| 2 | `site web diaspora sénégalaise` | Quasi nulle | Article 16/06 + `/site-web-diaspora` | 🔴 HAUTE |
| 3 | `comment choisir freelance web Sénégal` | Faible-moyen | Enrichir article existant | Moyenne |
| 4 | `prix site web Sénégal 2026 FCFA` | Moyen-fort | Optimiser article existant | Moyenne |
| 5 | `site web association diaspora` | Faible | `/site-web-association-diaspora` (après 16/06) | Moyenne |

### Phase 3 — Mesure & itération (Semaines 9-12) · *amplification*
- [ ] **[P1]** Comparer aux chiffres de départ (trafic, positions, conversions) — *Fodé*.
- [ ] **[P1]** Doubler sur ce qui marche, corriger ce qui stagne — *Raby* (arbitrage).
- [ ] **[P2]** Optimisations perf (polices non bloquantes, images) — *Youssouf*.
- [ ] **[P2]** OG images par article — *Youssouf*.

---

## 📌 Règles de l'agence (anti-conflit)
- **Une tâche = un seul propriétaire** (colonne ci-dessus). En cas de doute, Raby tranche.
- **NAP = source unique = Mouhamed.** Personne d'autre n'invente nom/adresse/téléphone/email.
- **Chaque tâche a un critère de réussite vérifiable** (le « ✅ quand… »).
- Statuts : `[ ]` à faire · `[~]` en cours · `[x]` fait.

---

## 📝 Journal
- **2026-06-09** — Audit initial réalisé. Agence familiale (7 agents) créée dans `~/.claude/agents/`. Constat majeur : blog absent du sitemap (P0 #1).
- **2026-06-09 (après-midi)** — Corrections code P0/P1 (commit `e3b6c52`, push main → Vercel). **P0 #1 sitemap : faux problème — déjà OK en prod** (le vrai levier devient l'indexation Search Console → Fodé). NAP email pro corrigé. hreflang trompeur retiré. Schema `BlogPosting` ajouté aux 6 articles. Restent ouverts : Google Business Profile (Saïbo), baseline Search Console (Fodé), BreadcrumbList, Phase 2 contenu/mots-clés.
- **2026-06-11** — Phase 2 lancée. Dialamba : mapping mots-clés v1 (7 pages). Bangaly : 5 opportunités SERP identifiées (Kaolack géo-local + diaspora = priorité HAUTE). Youssouf : title homepage, meta description, kicker "Tarifs & offres", lien "Voir les tarifs →" sur 6 articles, CTA box site-one-page (commit `1a386b6`). Fodé : baseline GSC créée dans `SEO/MESURES.md` (2 clics, 69 impressions, 3 mois — zéro requête non-marque). **Actions Saïbo restantes** : demander indexation articles dans GSC + créer Google Business Profile.
