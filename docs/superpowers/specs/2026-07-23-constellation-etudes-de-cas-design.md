# Constellation — refonte visuelle de la section « Études de cas »

**Date :** 2026-07-23
**Statut :** validé par Saïbo, en implémentation.

## Objectif

Remplacer les vignettes floutées génériques de la section études de cas par une
**vue graphe interactive façon Obsidian** (« constellation ») qui met en scène la
polyvalence de Saïbo d'un coup d'œil, dans la veine « extreme capabilities »
(MÉRIDIEN, SUNU TECH). Élaguer la carte RK Services.

## Décisions

- **Structure : graphe en hero + cartes en dessous.** Le graphe fait le *wow* ;
  les cartes gardent le détail lisible, le SEO et le repli mobile.
- **Desktop-only** pour le canvas force-directed (illisible sur téléphone) →
  sur `< lg`, on masque le graphe et on affiche directement les cartes.
- **Aucune nouvelle dépendance npm** : la simulation de forces est écrite à la
  main en vanilla JS dans un `<canvas>`.
- `EtudesDeCas.astro` reste la **source de vérité unique** des données projets.

## Le graphe

- **Nœuds projets (9)** après retrait de RK Services : Platinum, Jàng, MÉRIDIEN,
  SUNU TECH, S5L, RTZW, Registon, Nur Alhayaa, National Auto. Couleur = accent du
  projet (terracotta / vert-savane / noir-café).
- **Nœuds « hubs »** (les tags qui relient, façon Obsidian) : `Sénégal`, `Canada`,
  `SaaS`, `Démonstrateur`, `Construction`. Chaque projet se relie à ses hubs ;
  les liens sont dérivés d'un champ `hubs: string[]` ajouté à chaque projet.
- **Physique** : répulsion entre nœuds + ressorts sur les liens + centrage doux +
  léger flottement au repos. Réglée pour se stabiliser puis dériver lentement.
- **Interactions** :
  - survol d'un nœud → ses liens s'illuminent, le reste s'estompe ;
  - clic sur un nœud projet → scroll fluide vers sa carte détaillée (ancre `id`) ;
  - drag d'un nœud possible ;
  - respecte `prefers-reduced-motion` (pas de flottement, layout figé).

## Cartes (sous le graphe)

- Les cartes actuelles restent, RK Services retiré.
- Chaque `<article>` reçoit `id="cas-{slug}"` pour l'ancre au clic depuis le graphe.
- Sous-titre mis à jour : « 6 missions livrées, un SaaS en cours et 2
  démonstrateurs » (au lieu de 7 missions).

## Fichiers

- `src/components/ConstellationCas.astro` — **nouveau** : le canvas + la logique
  force-directed + interactions. Reçoit les nœuds/liens en props (ou lit un JSON
  inline dérivé des données).
- `src/components/EtudesDeCas.astro` — intégration du graphe (desktop-only) au-dessus
  de la grille, ajout du champ `hubs` par projet, retrait de RK Services, ancres `id`,
  sous-titre mis à jour.

## Hors code (action séparée)

- Suppression du déploiement Vercel `rk-services-indol` (confirmer le nom exact du
  projet avant suppression — action irréversible).

## Track 2 (planifié, PAS ce soir)

- Transformer le site **Nur Alhayaa** en démo cinématique scroll-scrubbée style Nick
  Saraev (comme SUNU TECH). Nécessite des crédits Higgsfield (épuisés au 22/07).
