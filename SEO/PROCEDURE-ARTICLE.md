# Procédure — un article par semaine (plan de visibilité 2026-2027)

Lue par les routines cloud **et** par toute session qui prépare un article. Source du calendrier :
onglet « 3. Calendrier » de `SEO/PLAN-VISIBILITE-2026-2027.xlsx` (miroir texte : `SEO/CALENDRIER.md`).

## Le cycle

| Quand | Qui | Quoi |
|---|---|---|
| **Jeudi 08:00 (UTC)** | routine « rédaction » | Rédige l'article du **mardi suivant** sur la branche `article/AAAA-MM-JJ`, + `SEO/posts/AAAA-MM-JJ.md` (3 posts). Pousse la branche. **Ne touche jamais à `main`.** |
| Jeudi → lundi | Saïbo | Relit l'aperçu Vercel de la branche. S'il refuse : il crée le fichier `NE-PAS-PUBLIER` à la racine de la branche (ou le dit en session). |
| **Mardi 09:00 (UTC = heure de Dakar)** | routine « publication » | Si la branche du jour existe et ne contient pas `NE-PAS-PUBLIER` : fusion dans `main` (fast-forward ou merge sans conflit), push, vérification en live. Sinon : ne fait rien. |
| Mardi, jeudi matin, samedi | Saïbo | Publie les 3 posts de `SEO/posts/AAAA-MM-JJ.md` sur ses comptes, coche l'onglet 4. |

**Nom de branche** : `article/AAAA-MM-JJ` (date du mardi). Si l'environnement cloud refuse de pousser ce nom,
utiliser `claude/article-AAAA-MM-JJ`. La routine de publication cherche les deux.

⛔ Rien ne se publie entre **jeudi au maghrib et vendredi au maghrib** (fenêtre Yahdi Qalbah). Les routines tournent hors de cette fenêtre.

## Rédiger l'article

1. **Lire le calendrier** (`SEO/CALENDRIER.md`) : titre et mot-clé de la semaine. Vérifier qu'aucune page ne vise déjà ce mot-clé (`SEO/CALENDRIER.md` § mots-clés) — sinon, l'article renvoie vers la page au lieu de la concurrencer.
2. **Copier la structure** de `src/pages/blog/creer-boutique-en-ligne-senegal.astro` : objet `article` (slug, titre, extrait, date du mardi, tags, tempsLecture), `Layout` avec `article={{ headline, datePublished }}`, image Unsplash **sans personne, sans visage, sans main**, `prose`, encadré CTA final.
3. **Ajouter l'entrée** dans le tableau `allArticles` de `src/pages/blog/index.astro` (même champs + `image` 600×450, `alt`, `draft: false`). Il n'y a **pas** de content collection : un `.md` dans `src/content/` n'est pas publié.
4. **Contenu** :
   - Français, ton pro, phrases courtes, exemples sénégalais concrets (Dakar, Thiès, diaspora). 1 200 à 1 800 mots.
   - Le mot-clé dans le `titre` (≤ 54 caractères avant « — Saïbo Danfakha », pour une balise title ≤ 70), dans le premier paragraphe et dans un `h2`.
   - `extrait` = meta description : **120 à 160 caractères**.
   - **2 à 4 liens internes** : au moins une page service (`/referencement-site-web-senegal/`, `/application-web-sur-mesure/`, `/site-web-diaspora/`, `/site-web-association-diaspora/`, `/freelance-web-kaolack/`) et un article existant.
   - **Aucun prix de Saïbo.** Les fourchettes du marché sont permises. « Chiffré sur devis ».
   - **Aucun client nommé** en dehors des études de cas déjà publiques (`src/pages/etudes-de-cas/`), et seulement avec ce que l'étude de cas dit déjà.
   - **Aucun chiffre inventé** (statistiques, études) : pas de source vérifiable ⇒ pas de chiffre.
   - Rien de religieux, rien sur la musique.
5. **Les 3 posts** (`SEO/posts/AAAA-MM-JJ.md`) :
   - **Post 1 — mardi, LinkedIn + X** : l'idée de l'article en 5 lignes, une question finale, le lien. Version X ≤ 280 caractères.
   - **Post 2 — jeudi matin, carrousel Instagram + Statut WhatsApp** : 7 diapositives (titre + 5 points + appel « lien en bio / écris-moi »), légende Instagram, texte du Statut.
   - **Post 3 — samedi, vidéo 9:16 TikTok + Reels** : script de 30-45 s (accroche en 2 s, 3 idées, appel), texte à l'écran, légende. **Aucune musique** : design sonore seul ou voix.
6. **Contrôle avant push** : `npm run build` vert (en cloud ; sur le PC de Saïbo le build est bloqué par Windows, c'est l'aperçu Vercel qui fait foi), la page existe dans `dist/blog/<slug>/index.html`, le slug est dans `dist/sitemap-0.xml`.
7. **Commit** : ajouter les fichiers **un par un** (jamais `git add -A`), message `Article du AAAA-MM-JJ : <titre>`, fin de message `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Publier (mardi)

1. `git fetch --all`, chercher `origin/article/AAAA-MM-JJ` puis `origin/claude/article-AAAA-MM-JJ` ; vérifier que la branche trouvée ne contient pas `NE-PAS-PUBLIER`.
2. `git checkout main && git pull && git merge --no-edit <branche>` ; en cas de conflit : **abandonner** (`git merge --abort`) et ne rien publier.
3. Push sur `main` (Vercel déploie seul). Attendre ~2 min puis vérifier : `https://saibodanfakha.com/blog/<slug>/` répond 200 et contient le titre ; `https://saibodanfakha.com/sitemap-0.xml` contient le slug.
4. Ajouter une ligne au journal de ce fichier : date, slug, commit, résultat de la vérification.

## Journal

- **2026-10-15** — Procédure créée (plan de visibilité validé par Saïbo le 15/10).
- **2026-10-20** — publié referencement-google-dakar-par-ou-commencer (8694eda) : build OK, push OK ; vérification prod NON effectuée (proxy du routeur : 403 sur saibodanfakha.com) — à contrôler à la main
- **2026-10-27** — publié combien-coute-referencement-site-senegal (314cd99) : build OK, push OK ; vérification prod NON effectuée (proxy : 403 sur saibodanfakha.com) — à contrôler à la main
