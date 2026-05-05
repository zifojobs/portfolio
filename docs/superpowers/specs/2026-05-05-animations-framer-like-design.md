# Animations Framer-like sur le portfolio

**Date** : 2026-05-05
**Contexte** : portfolio saibodanfakha.com en ligne depuis 2026-05-03. Stack : Astro 6.2 + Tailwind 4 + GSAP/ScrollTrigger + Lenis. Saïbo veut des micro-interactions style Framer pour donner plus de vie au site.

## Objectif

Ajouter une couche de micro-interactions cohérente sur tout le site sans nouvelle dépendance et sans dégrader la performance ou l'accessibilité.

## Scope

Six effets, à livrer ensemble :

### 1. Curseur custom

- Cercle 24px qui suit la souris (lerp / interpolation douce)
- Au hover de `a`, `button`, `[data-cursor]` : grossit à 56px, couleur passe à l'accent chaud
- Curseur natif masqué uniquement quand le custom est actif
- Désactivé sous 1024px et si `prefers-reduced-motion: reduce`
- Fichier : `src/scripts/cursor.ts`, vanilla TS, monté depuis `Layout.astro`

### 2. Hover cartes — lift + glow

- Cibles : cartes Offres, Études de cas, Témoignages
- `translateY(-4px)` + `scale(1.01)` au hover
- Ombre douce qui apparaît, glow plus chaud en dark
- Transition 300ms ease-out
- CSS pur via Tailwind + variables de thème existantes

### 3. Boutons magnétiques

- Cibles : CTA Hero, CTA par offre, Contact, Header
- Zone d'attraction ~80px autour du bouton, déplacement max 8px vers le curseur, easing fluide
- Sortie : retour à l'origine
- Fichier : `src/scripts/magnetic.ts`, attaché via `data-magnetic`
- Désactivé sous 1024px et si reduced-motion

### 4. Reveal de texte au scroll

- Cibles : `h2` de section (Offres, Études de cas, À propos, Témoignages, Contact)
- Split par **mots** (pas par lettres), cascade `translateY 20px → 0`, `opacity 0 → 1`, stagger 50ms
- Trigger : GSAP ScrollTrigger à l'entrée du titre dans le viewport
- One-shot, pas de replay
- Désactivé si reduced-motion
- Fichier : `src/scripts/textReveal.ts`

### 5. Compteurs animés sur les stats

- Si une section contient des stats numériques (À propos), animer de 0 à la valeur cible
- Durée ~1.2s, easing easeOut, déclenché à l'entrée dans le viewport
- À vérifier dans le code : si pas de stats actuellement, l'effet est sauté ou les stats sont ajoutées dans la section À propos
- Fichier : `src/scripts/counters.ts` (conditionnel)

### 6. Transitions sur les liens

- Cibles : liens nav header + footer
- Underline qui se trace de gauche à droite au hover, 300ms
- CSS pur via pseudo-élément `::after`

## Garde-fous transverses

- `prefers-reduced-motion: reduce` désactive tout (CSS media query + early-return JS)
- Mobile (<1024px) : pas de curseur custom, pas de magnétique. Reste (hover, reveal, compteurs) reste actif.
- Aucune nouvelle dépendance npm. Bundle inchangé.

## Architecture fichiers

Nouveaux :
- `src/scripts/cursor.ts`
- `src/scripts/magnetic.ts`
- `src/scripts/textReveal.ts`
- `src/scripts/counters.ts`

Modifiés :
- `src/styles/global.css` — règles hover cartes + underline liens + reduced-motion
- `src/layouts/Layout.astro` — import des nouveaux scripts
- Composants `Hero.astro`, `Offres.astro`, `EtudesDeCas.astro`, `Temoignages.astro`, `APropos.astro`, `Contact.astro`, `Header.astro`, `Footer.astro` — ajout d'attributs `data-magnetic`, `data-cursor`, `data-text-reveal` sur les éléments cibles

## Critères de réussite

- Site fluide en desktop, aucun jank au scroll
- Curseur custom invisible et désactivé en mobile
- Reduced-motion respecté (à tester dans DevTools)
- Build Astro passe sans warning
- Aucune régression visuelle sur le toggle dark/light
