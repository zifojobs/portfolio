# saibodanfakha.com — Portfolio & blog (spoke technique)

**Dernière mise à jour : 2026-06-17 (réécrit en spoke léger lors de la centralisation)**

> 🧭 **Contexte global, stratégie, prochaine session → voir le HUB :**
> `E:\DOSSIER FREELANCE\Projets Web\Projet Claude\CLAUDE.md`.
> Ce fichier ne contient QUE la **référence technique** du site. Le **suivi vivant**
> (état du blog, SEO/GSC, tarifs, prospection, prochaine session) est tenu dans le hub —
> ne pas le recopier ici pour éviter la désynchro.

**État en 1 ligne :** ✅ en ligne depuis 2026-05-03 · 7 articles blog · SEO en cours
(baseline GSC 11/06). Détail courant = hub.

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

- `public/social-photos/generate_articleN.py` (Python + Playwright) → 7 slides Instagram
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
- Page d'atterrissage géo : `/freelance-web-kaolack`.

## Cohérence diaspora ⚠️

Le site est **FR uniquement**. Tout contenu diaspora = posture « service expert pour
clients », **jamais** « regardez mon site bilingue ». Pas de fausse promesse de bilinguisme.

## Conventions

- **Langue** : français · demander avant les décisions visuelles.
- Ton portfolio = **pro / business** (jamais le ton « Anomalie Audacieuse » de Yahdi Qalbah).

---

> 🗄️ Historique détaillé pré-centralisation (journal mai, distribution Buffer, etc.) :
> `…\Projet Claude\_backup_claudemd_2026-06-17\saibodanfakha_CLAUDE.md.bak`.
