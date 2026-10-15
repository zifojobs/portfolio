# Mesures SEO — saibodanfakha.com

Relevés mensuels Google Search Console (propriété https://saibodanfakha.com/, non-www).
Le plus récent en premier ; la baseline du 2026-06-11 en bas de fichier.

---

# Relevé n°4 — 2026-10-15 · DÉPART du plan de visibilité
**Source** : GSC, captures de Saïbo · **Période** : 3 mois (~13/07 → 13/10/2026)

| Métrique | 15/10 | 27/07 | Δ |
|---|---|---|---|
| Clics | **1** | 2 | −1 |
| Impressions | **285** | 96 | **×3** |
| CTR | 0,4 % | 2,1 % | — (dilution) |
| Position moyenne | 19,8 | 20,7 | ≈ |
| Requêtes | 24 | 16 | +8 |
| Pages indexées | **24** (9 non indexées) | — | — |

**Requêtes (top 10)** : rédacteur web senegal 27 · référencement local senegal 20 · référencement google sénégal 19 ·
optimisation seo site web sénégal 15 · software development services 6 · assistant ia whatsapp 4 · création de site
e-commerce sénégal 3 · référencement site senegal 3 · comment choisir un développeur web freelance 3 · référencement naturel dakar 3.

**Lecture**
1. **Les impressions triplent sans un article publié depuis le 21/07** : le site prend de l'âge, Google le montre plus.
   Mais il reste en **page 2** (position ~20) ⇒ presque aucun clic. Le plan vise à faire passer des requêtes en top 10.
2. **Le référencement pèse 60 impressions sur 285** (4 requêtes) ⇒ la page `/referencement-site-web-senegal/`
   (en ligne depuis le 15/10) et l'article du 20/10 tombent juste.
3. 🆕 **« rédacteur web senegal » = 1ʳᵉ requête (27)**, sans aucune page qui y réponde. ⇒ **décision de Saïbo** :
   vend-il la rédaction web (il rédige déjà les articles de Platinum) ? Si oui : une page service ; sinon : rien.
4. « assistant ia whatsapp » (4) : la page `/assistant/` commence à exister pour Google.
5. **Indexation (rapport du 09/10)** : 4 en 404 · 2 « noindex » · 1 canonique alternative · 1 explorée non indexée ·
   1 détectée non indexée. 404 relevés en direct le 15/10 : `/politique/`, `/arabe/`, `/projets/`,
   `/etudes-de-cas/rk-services/`, `/etudes-de-cas/meridien/`, `/sitemap.xml` ⇒ **redirections 301 ajoutées
   (`vercel.json`)**. Saïbo : cliquer « Valider la correction » sur la ligne 404 dans GSC.
6. **Sitemap lu le 03/10, 26 pages** ⇒ les nouvelles pages (30 URL) seront relues ; Saïbo peut le renvoyer (« Envoyer » sur `sitemap-index.xml`).
7. Core Web Vitals : « aucune donnée » = trafic trop faible pour Google, pas un défaut. HTTPS : 0 problème.

**Prochain relevé : début novembre (rapport mensuel, onglet 6).**

---

# Relevé n°2 — 2026-07-10
**Source** : GSC · **Période** : 3 mois (09/04/2026 → 08/07/2026, données à jour −4h)

## Métriques globales (vs baseline)

| Métrique | 2026-07-10 | Baseline 06/06 | Δ |
|---|---|---|---|
| Clics totaux | **2** | 2 | = |
| Impressions totales | **76** | 69 | +7 |
| CTR moyen | **2,6 %** | 2,9 % | −0,3 pt |
| Position moyenne | **9,3** | 6,2 | −3,1 (voir constat 2) |

## Requêtes (7 visibles — vs 2 en juin)

| Requête | Clics | Impressions | Type |
|---|---|---|---|
| danfakha | 0 | 9 | Marque |
| développement web | 0 | 3 | **Générique** 🆕 |
| prix création site wordpress dakar | 0 | 3 | **Générique** 🆕 |
| mohamed danfakha | 0 | 1 | Marque |
| freelance webflow | 0 | 1 | **Générique** 🆕 |
| software development services | 0 | 1 | **Générique** 🆕 |
| creation site web dakar prix | 0 | 1 | **Générique** 🆕 |

> **9 impressions non-marque (vs 0 en juin).** Premier signal de visibilité générique.
> « prix création site wordpress dakar » + « creation site web dakar prix » = le mot-clé
> primaire mappé sur l'article prix (mapping Dialamba v1) qui commence à répondre.

## Pages (10 visibles — vs 6 en juin)

| URL | Clics | Impressions |
|---|---|---|
| / (homepage) | **2** | 65 |
| /politique/ | 1 | 4 |
| /blog/ | 0 | 6 |
| /blog/combien-coute-un-site-professionnel/ | 0 | **6** 🆕 |
| /etudes-de-cas/s5l/ | 0 | 3 |
| /blog/site-one-page-ou-multi-pages/ | 0 | 2 🆕 |
| /blog/wordpress-astro-webflow/ | 0 | 1 🆕 (publié 30/06 !) |
| /etudes-de-cas/rtzw/ | 0 | 1 |
| /blog/comment-choisir-son-developpeur-web-freelance/ | 0 | 1 |
| /blog/5-erreurs-fatales-site-entreprise/ | 0 | 1 🆕 |

## Indexation (inspections URL du 10/07)

- ✅ `/blog/diaspora-site-bilingue/` : **indexée** (« Cette URL est sur Google ») — action de juin soldée.
- ❌ `/freelance-web-kaolack/` : **non indexée** — « Google ne reconnaît pas cette URL »,
  jamais explorée. Vérification faite le 10/07 : la page **est bien dans le sitemap live**
  (`sitemap-0.xml`, 20 URLs) → pas de bug technique, Google n'a simplement pas encore
  rapproché les deux. Action : « Demander une indexation » dans GSC + attendre.

## Constats clés

1. **La barrière marque est tombée** : 5 requêtes génériques génèrent des impressions
   (développement web, prix création site wordpress dakar…). Volume minuscule (9 imp.)
   mais c'était LE levier identifié en juin. La machine démarre.
2. **Position moyenne 6,2 → 9,3 = bonne nouvelle déguisée** : la moyenne baisse parce que
   des requêtes génériques (qui rankent plus loin) entrent dans le calcul. Une moyenne qui
   se dégrade en gagnant des requêtes vaut mieux qu'une belle moyenne sur la seule marque.
3. **L'article prix confirme le mapping** : `/combien-coute-un-site-professionnel/` passe
   de 0 à 6 impressions, aligné sur ses requêtes cibles « prix/création site Dakar ».
   Angle « Dakar » > « Sénégal » dans les requêtes réelles — à noter pour Dialamba.
4. **Clics toujours à 2** : la visibilité progresse, pas encore le trafic. Normal à ce
   volume d'impressions ; le CTR se jouera quand des requêtes génériques atteindront le top 10.
5. **4 pages entrent dans l'index visible** (10 vs 6), dont `wordpress-astro-webflow`
   8 jours après publication — l'indexation s'accélère.

## Actions découlant du relevé

1. ✅ **Fait le 10/07** : demande d'indexation envoyée pour `/freelance-web-kaolack/`
   et les articles sans impression (`performance-web-conversion`, `pourquoi-un-site-sur-mesure`,
   `seo-local-senegal`). À revérifier au relevé du 11/08.
3. Dialamba : les requêtes réelles disent « Dakar » (prix création site **wordpress dakar**),
   pas « Sénégal » — envisager un renfort sémantique Dakar sur l'article prix.
4. Prochain relevé : **2026-08-11** — surveiller kaolack indexée + premières requêtes en top 10.

---

# Baseline — 2026-06-11
**Source** : Google Search Console (propriété https://saibodanfakha.com/)
**Période analysée** : 3 mois (08/03/2026 → 06/06/2026)

---

## Métriques globales

| Métrique | Valeur |
|---|---|
| Clics totaux | **2** |
| Impressions totales | **69** |
| CTR moyen | **2,9 %** |
| Position moyenne | **6,2** |

---

## Top requêtes (onglet Requêtes)

| Requête | Clics | Impressions |
|---|---|---|
| danfakha | 0 | 11 |
| mohamed danfakha | 0 | 1 |

> Seulement 2 requêtes visibles — toutes deux de marque. Aucune requête générique (ex : "freelance web Sénégal") ne génère encore d'impressions.

---

## Top pages (onglet Pages)

| URL | Clics | Impressions |
|---|---|---|
| https://saibodanfakha.com/ | **2** | 63 |
| https://saibodanfakha.com/politique/ | 1 | 5 |
| https://saibodanfakha.com/blog/ | 0 | 10 |
| https://saibodanfakha.com/etudes-de-cas/s5l/ | 0 | 1 |
| https://saibodanfakha.com/etudes-de-cas/rtzw/ | 0 | 1 |
| https://saibodanfakha.com/blog/comment-choisir-son-developpeur-web-freelance/ | 0 | 1 |

> 6 pages visibles au total. Les articles de blog sont indexés mais ne génèrent pas encore de clics. Les 5 autres articles n'apparaissent pas encore — probablement en attente d'indexation complète.

---

## Constats clés

1. **Trafic quasi nul mais attendu** : 2 clics en 3 mois est faible, mais cohérent avec un site de moins de 3 mois et un blog lancé seulement en mai. Pas d'alarme — c'est la baseline de départ.

2. **Zéro requête non-marque** : 100 % des impressions viennent de "danfakha" (nom propre). Le site n'apparaît encore sur aucune requête générique cible ("freelance web Sénégal", "créer site web Kaolack", etc.). C'est le principal levier à activer.

3. **Homepage seule page performante** : 63 impressions / 2 clics (CTR 3,2 %). Le blog existe dans l'index mais ne reçoit pas encore de trafic. L'article "comment-choisir-son-developpeur-web-freelance" commence à apparaître (1 impression).

4. **Position moyenne 6,2** : bonne pour un site jeune, mais calculée uniquement sur des requêtes de marque — sans valeur pour les requêtes cibles.

---

## Actions prioritaires (découlant de ces chiffres)

1. **Demander l'indexation des articles** dans GSC (Inspection URL → Demander l'indexation) pour les 5 articles qui n'apparaissent pas encore. Action Saïbo.
2. **Attendre 4 semaines** après le déploiement du nouveau `<title>` homepage ("Développeur Web Freelance au Sénégal — Saïbo Danfakha") pour voir si des impressions non-marque apparaissent.
3. **Prochain point de mesure** : 2026-07-11 — comparer impressions/requêtes, vérifier si articles commencent à ranker sur leurs mots-clés primaires (mapping Dialamba v1).

---

## Historique des relevés

| Date | Clics | Impressions | CTR | Position | Notes |
|---|---|---|---|---|---|
| 2026-06-11 | 2 | 69 | 2,9 % | 6,2 | Baseline initiale — 3 mois |
| 2026-07-10 | 2 | 76 | 2,6 % | 9,3 | 1res requêtes non-marque (5, 9 imp.) · 10 pages visibles · diaspora indexée · kaolack non indexée |
| 2026-07-27 | 2 | 96 | 2,1 % | 20,7 | **16 requêtes** · la marque ne pèse plus que 2 imp. · **8/10 des requêtes = SEO/référencement** · aucun mot-clé du mapping v1 ne ressort |
| 2026-08-11 | — | — | — | — | Non relevé |
| 2026-10-15 | 1 | 285 | 0,4 % | 19,8 | **Départ du plan** · 24 requêtes · « rédacteur web senegal » en tête (27) · 24 pages indexées, 4 en 404 → redirigées |

---

## Relevé n°3 — 2026-07-27 (relevé anticipé, fenêtre 3 mois)

**2 clics · 96 impressions · CTR 2,1 % · position moyenne 20,7 · 16 requêtes**

### Lecture des chiffres

- **La position 6,2 → 9,3 → 20,7 n'est PAS une dégradation.** En juin, la moyenne était calculée
  quasi uniquement sur « danfakha » (marque, position 1-3). Le site ressort maintenant sur des
  requêtes génériques concurrentielles où il est en page 2-3 → la moyenne se dilue mécaniquement.
  Même explication pour le CTR (2,9 % → 2,1 %).
- **Le vrai indicateur : +39 % d'impressions depuis juin** (69 → 96), avec une accélération nette
  à partir du 07/07 = effet des demandes d'indexation du 10/07.
- **Sortie de la dépendance à la marque : « danfakha » ne pèse plus que 2 impressions sur 96**
  (contre 100 % en juin). C'est le vrai progrès du trimestre.
- **Bloqué en page 2** : 96 impressions → 2 clics. Il n'y a pas de clic à espérer au-delà du top 10.
  Le levier n'est pas « plus d'articles », c'est **faire passer 2-3 requêtes du top 20 au top 10**.

### 🔴 Découverte majeure : Google classe le site comme prestataire SEO, pas comme créateur de sites

| Requête | Impr. |
|---|---|
| optimisation seo site web sénégal | **15** |
| développement web | 4 |
| referencement local senegal | 4 |
| prix création site wordpress dakar | 3 |
| référencement naturel dakar | 3 |
| danfakha (marque) | 2 |
| software development services | 2 |
| référencement google sénégal | 2 |
| référencement site à dakar | 2 |
| seo et référencement dakar | 2 |

1. **8 des 10 premières requêtes portent sur le référencement**, pas sur la création de sites.
2. **Aucun mot-clé du mapping Dialamba v1 ne ressort** : zéro impression sur « développeur web
   freelance Sénégal », « prix site web Sénégal », « portfolio développeur web Sénégal »,
   « créer boutique en ligne Sénégal ». **Le mapping v1 n'a rien produit à ce jour.**
3. **Une seule requête = 16 % de la visibilité totale** (« optimisation seo site web sénégal »,
   15/96) **sans aucune page dédiée au SEO sur le site**. Meilleur point d'entrée disponible.
4. **Le marché dit Dakar, pas Kaolack** : 5 requêtes sur 10 contiennent « dakar », zéro contient
   « kaolack » — alors que `/freelance-web-kaolack` a été créée le 14/06.
5. « prix création site **wordpress** dakar » : le marché formule son besoin en WordPress + prix.

### Décision à trancher (business, pas technique) — prochaine session SEO

**Saïbo veut-il vendre du référencement ?**
- **Si oui** → écrire une page service « Référencement / SEO au Sénégal ». Google l'y pousse déjà,
  et partir de la page 2 rend le top 10 atteignable rapidement.
- **Si non** → corriger le tir : le site est aujourd'hui visible sur une offre qui n'est pas vendue.

⚠️ **Ne rien lancer avant que Jàng soit relancé** (2 écoles entrantes en attente). Le SEO du
portfolio est un investissement à 12-18 mois ; aucun client de juillet n'en est venu.
