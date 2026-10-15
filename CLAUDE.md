# saibodanfakha.com — Portfolio & blog (spoke technique)

**Dernière mise à jour : 2026-10-15 (plan de visibilité 6 mois + routines cloud)**

> 🧭 **Contexte global, stratégie, prochaine session → voir le HUB privé** (hors repo).
> Ce fichier ne contient QUE la **référence technique** du site. Le **suivi vivant**
> (état du blog, SEO/GSC, tarifs, prospection, prochaine session) est tenu dans le hub —
> ne pas le recopier ici pour éviter la désynchro.

**État en 1 ligne :** ✅ en ligne depuis 2026-05-03 · 13 articles (14ᵉ le 20/10) · **aucun prix de
Saïbo affiché** (décision du 12/10, chiffrage sur devis) · 3 piliers : sites · référencement · applications
sur mesure. Détail courant = hub.

## 🗓️ Plan de visibilité 16/10/2026 → 15/04/2027 (validé par Saïbo le 15/10)

- **Tout est dans `SEO/`** : `PLAN-VISIBILITE-2026-2027.xlsx` (6 onglets, méthode de l'équipe SEO de Platinum,
  généré par `SEO/plan_visibilite.py` — relancer après chaque changement de page pour la feuille meta),
  `CALENDRIER.md` (miroir texte), `PROCEDURE-ARTICLE.md` (**fait foi**), `posts/AAAA-MM-JJ.md`, `PROFILS-RESEAUX.md`.
- **Automatique** : routine cloud **jeudi 08:00 UTC** (`trig_01T18ULqFvXXuJ1rkEN9Yf8A`, Opus 5.5) rédige l'article du
  mardi suivant sur `article/AAAA-MM-JJ` · routine **mardi 09:00 UTC** (`trig_01FMRDT6Vr6JSLDEozgdjGWk`, Sonnet 5.5)
  le fusionne dans `main` sauf si `NE-PAS-PUBLIER` existe sur la branche. Gérer : claude.ai/code/routines.
- **Saïbo** : relire jeudi → lundi, publier les 3 posts (mardi · jeudi matin · samedi), cocher l'onglet 4.
- ⚠️ **Sur le PC, `npm run build` échoue** (module natif Tailwind bloqué par Windows, erreur 4551) :
  la vérification passe par le statut Vercel du commit (API GitHub) puis la prod. L'aperçu Vercel est protégé.

---

## Stack & déploiement

- **Framework** : Astro 6.2 + Tailwind + GSAP + Lenis (smooth scroll).
- **Repo** : github.com/zifojobs/portfolio
- **Hébergement** : Vercel (auto-deploy sur push `main`), **DNS chez Hostinger**.
- **Site** : propriété GSC **NON-www**, sitemap `sitemap-index.xml` (piège www/non-www
  résolu — garder le non-www).

## Architecture du blog ⚠️

- Les articles sont des **pages `.astro` dans `src/pages/blog/`** + listés à la main dans
  `src/pages/blog/index.astro`. **PAS de content collection.**
- `src/content/blog/` n'est **PAS** lu → ne jamais y déposer de `.md` en pensant publier.
- Rythme de publication : **mardi 9h**.

## Visuels sociaux (pipeline)

- `social-photos/generate_articleN.py` (hors de `public/` → non publié) (Python + Playwright) → 7 slides Instagram
  1080×1080 + 7 WhatsApp 1080×1920 par article.
- **Style de référence validé** : « dark warm + halos colorés » **dans le design system**
  du site. `generate_article7.py` = gabarit à réutiliser/dupliquer pour les prochains.
- **Images de blog** : pas de personnes / visages / mains (objets, espaces, graphiques).

## Page /arabe

- Redesign premium (GSAP hero word-by-word, grille 2×2 des 4 niveaux REVE, couleurs
  Yahdi Qalbah or/noir #b8860b / #000 / #fff, cartes hover, boutons magnétiques).
- Renvoie vers l'activité **Cours d'arabe** (pilotée côté Yahdi Qalbah — voir son spoke).

## SEO (dossier `SEO/`)

- Backlog + mesures + fiches : `SEO/BACKLOG.md`, `SEO/MESURES.md`, `SEO/GBP-fiche-saibo.md`.
- Agence SEO familiale (7 agents) = définie globalement, appelée par prénom
  (Raby, Youssouf, Dialamba, Mouhamed, Lamine, Fodé, Bangaly). État/relevés GSC = **hub**.
- Page d'atterrissage géo : `/freelance-web-kaolack` — **hero 3D particules** « Le sel de Kaolack »
  (`src/scripts/heroKaolack3d.ts`, chunk lazy desktop only ; mobile = hero statique, SEO intact).

## Cohérence diaspora ⚠️

Le site est **FR uniquement**. Tout contenu diaspora = posture « service expert pour
clients », **jamais** « regardez mon site bilingue ». Pas de fausse promesse de bilinguisme.

## Conventions

- **Langue** : français · demander avant les décisions visuelles.
- Ton portfolio = **pro / business** (jamais le ton « Anomalie Audacieuse » de Yahdi Qalbah).

---

> 🗄️ Historique détaillé pré-centralisation (journal mai, distribution Buffer, etc.) :
> sauvegarde locale `_backup_claudemd_2026-06-17/` (hors repo, côté hub privé).
