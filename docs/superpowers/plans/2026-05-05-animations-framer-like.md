# Animations Framer-like — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ajouter une couche cohérente de micro-interactions Framer-like (curseur custom, hover cartes, boutons magnétiques, reveal de titres, compteurs, underline liens) sans nouvelle dépendance.

**Architecture:** Vanilla TypeScript pour les comportements interactifs (cursor, magnetic, text reveal, counters), CSS pur pour les hovers et underlines. GSAP/ScrollTrigger déjà installé est réutilisé pour le text reveal. Tous les effets respectent `prefers-reduced-motion` et sont désactivés sous 1024px quand pertinent.

**Tech Stack:** Astro 6.2, Tailwind 4, TypeScript, GSAP 3 + ScrollTrigger, Lenis (déjà en place).

**Spec:** `docs/superpowers/specs/2026-05-05-animations-framer-like-design.md`

**Verification approach:** Pas de tests automatisés sur ce projet. Chaque tâche se vérifie manuellement dans le navigateur via `npm run dev` (Astro dev server). Le critère de succès est explicité à chaque tâche.

---

## Task 1: Fondations CSS (hover cartes + underline liens + reduced-motion)

**Files:**
- Modify: `src/styles/global.css` (ajout en fin de fichier)

- [ ] **Step 1: Lire le fichier actuel**

Run: `Read src/styles/global.css`
Note la dernière ligne (le bloc `@media (prefers-reduced-motion: reduce)` existant à la ligne ~99).

- [ ] **Step 2: Ajouter les styles hover cartes + underline liens en fin de `global.css`**

Insérer ce bloc à la fin du fichier (après le `@media reduced-motion` existant) :

```css
/* ==========================================
   MICRO-INTERACTIONS — hover cartes, underline liens
   ========================================== */

/* Hover cartes : lift + glow doux */
.card-hover {
  transition:
    transform 0.3s cubic-bezier(0.16, 1, 0.3, 1),
    box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.3s ease;
  will-change: transform;
}
.card-hover:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.12);
}
html:not(.theme-light) .card-hover:hover {
  /* Glow chaud en dark : ombre teintée terracotta */
  box-shadow: 0 12px 40px -8px rgba(194, 65, 12, 0.25);
}

/* Underline animé sur les liens nav */
.nav-link {
  position: relative;
  display: inline-block;
}
.nav-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 100%;
  height: 1.5px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.nav-link:hover::after {
  transform: scaleX(1);
}

/* Curseur custom : caché par défaut, activé par script */
.custom-cursor {
  position: fixed;
  top: 0;
  left: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-terracotta);
  pointer-events: none;
  z-index: 9999;
  transform: translate(-50%, -50%);
  transition: width 0.25s ease, height 0.25s ease, background 0.25s ease, opacity 0.2s ease;
  mix-blend-mode: difference;
  opacity: 0;
}
.custom-cursor.is-active {
  opacity: 0.85;
}
.custom-cursor.is-hover {
  width: 56px;
  height: 56px;
  background: var(--color-terracotta);
  opacity: 0.6;
}
/* Quand le custom cursor est actif, masquer le natif sur desktop */
html.has-custom-cursor,
html.has-custom-cursor * {
  cursor: none !important;
}

/* Text reveal par mots (préparation : caché avant reveal) */
.reveal-word {
  display: inline-block;
  opacity: 0;
  transform: translateY(20px);
  will-change: opacity, transform;
}

/* Reduced motion : neutralise tous les effets ci-dessus */
@media (prefers-reduced-motion: reduce) {
  .card-hover,
  .card-hover:hover,
  .nav-link::after {
    transition: none;
    transform: none;
  }
  .custom-cursor {
    display: none !important;
  }
  html.has-custom-cursor,
  html.has-custom-cursor * {
    cursor: auto !important;
  }
  .reveal-word {
    opacity: 1;
    transform: none;
  }
}
```

- [ ] **Step 3: Lancer le dev server et vérifier que le site charge**

Run dans `e:/DOSSIER FREELANCE/Projets Web/saibodanfakha` :
```bash
npm run dev
```
Expected: serveur sur `http://localhost:4321`, site rendu sans erreur console.

- [ ] **Step 4: Commit**

```bash
git add src/styles/global.css
git commit -m "feat(animations): add CSS foundations for micro-interactions"
```

---

## Task 2: Appliquer les classes hover-cartes + nav-link sur les composants

**Files:**
- Modify: `src/components/Offres.astro` (cartes offres)
- Modify: `src/components/EtudesDeCas.astro` (cartes études de cas)
- Modify: `src/components/Temoignages.astro` (cartes témoignages)
- Modify: `src/components/APropos.astro` (cartes principes ligne 67)
- Modify: `src/components/Header.astro` (liens nav)
- Modify: `src/components/Footer.astro` (liens nav)

- [ ] **Step 1: Trouver les cartes dans chaque composant**

Run: `Grep "rounded-" src/components/Offres.astro src/components/EtudesDeCas.astro src/components/Temoignages.astro -n`
Identifier la balise `<article>` ou `<div>` qui sert de carte dans chaque composant.

- [ ] **Step 2: Ajouter la classe `card-hover` sur chaque carte**

Pour `APropos.astro` ligne 67, modifier :
```astro
<article data-animate class="bg-creme border border-sable-300 rounded-xl p-8 transition-all duration-300 hover:border-noir-cafe">
```
en :
```astro
<article data-animate class="card-hover bg-creme border border-sable-300 rounded-xl p-8 hover:border-noir-cafe">
```
(retirer `transition-all duration-300` puisque `card-hover` gère ses propres transitions).

Faire la même opération pour les cartes principales de `Offres.astro`, `EtudesDeCas.astro`, `Temoignages.astro` : repérer le `<article>` ou `<div>` qui est la carte (généralement avec `rounded-xl` ou `rounded-2xl`), ajouter `card-hover`, retirer un éventuel `transition-all duration-300` redondant.

- [ ] **Step 3: Ajouter la classe `nav-link` sur les liens du Header et Footer**

Dans `Header.astro` : pour chaque `<a href="#xxx">` du menu desktop ET du menu mobile drawer, ajouter la classe `nav-link`.

Dans `Footer.astro` : ajouter `nav-link` sur les liens internes (ancres) et les liens réseaux sociaux.

- [ ] **Step 4: Vérifier dans le navigateur**

Recharger `http://localhost:4321`. Survoler chaque carte : doit lift + ombre douce. Survoler les liens nav : underline qui se trace de gauche à droite. Tester en dark ET en light (toggle du site).

Critère de succès : effet visible sur toutes les cartes ciblées, aucune carte ne saute brutalement, aucun jank.

- [ ] **Step 5: Commit**

```bash
git add src/components/
git commit -m "feat(animations): apply card-hover and nav-link classes"
```

---

## Task 3: Curseur custom

**Files:**
- Create: `src/scripts/cursor.ts`
- Modify: `src/layouts/Layout.astro` (import du script)

- [ ] **Step 1: Créer `src/scripts/cursor.ts`**

```ts
// Curseur custom : cercle qui suit la souris, grossit au hover des éléments interactifs.
// Désactivé sous 1024px et si prefers-reduced-motion: reduce.

const BREAKPOINT = 1024;
const LERP = 0.18;
const HOVER_SELECTOR = 'a, button, [data-cursor], input[type="submit"]';

export function initCustomCursor(): void {
  if (typeof window === "undefined") return;
  if (window.innerWidth < BREAKPOINT) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!window.matchMedia("(pointer: fine)").matches) return;

  const cursor = document.createElement("div");
  cursor.className = "custom-cursor";
  document.body.appendChild(cursor);
  document.documentElement.classList.add("has-custom-cursor");

  let targetX = window.innerWidth / 2;
  let targetY = window.innerHeight / 2;
  let currentX = targetX;
  let currentY = targetY;
  let raf = 0;

  const onMove = (e: MouseEvent) => {
    targetX = e.clientX;
    targetY = e.clientY;
    if (!cursor.classList.contains("is-active")) cursor.classList.add("is-active");
  };

  const tick = () => {
    currentX += (targetX - currentX) * LERP;
    currentY += (targetY - currentY) * LERP;
    cursor.style.transform = `translate(${currentX}px, ${currentY}px) translate(-50%, -50%)`;
    raf = requestAnimationFrame(tick);
  };

  const onEnter = () => cursor.classList.add("is-hover");
  const onLeave = () => cursor.classList.remove("is-hover");

  window.addEventListener("mousemove", onMove);
  document.querySelectorAll(HOVER_SELECTOR).forEach((el) => {
    el.addEventListener("mouseenter", onEnter);
    el.addEventListener("mouseleave", onLeave);
  });

  // MutationObserver pour les éléments ajoutés dynamiquement (ex: drawer mobile, mais
  // bon — sous 1024px le cursor est désactivé, donc utile surtout pour les portails).
  const mo = new MutationObserver(() => {
    document.querySelectorAll(HOVER_SELECTOR).forEach((el) => {
      el.removeEventListener("mouseenter", onEnter);
      el.removeEventListener("mouseleave", onLeave);
      el.addEventListener("mouseenter", onEnter);
      el.addEventListener("mouseleave", onLeave);
    });
  });
  mo.observe(document.body, { childList: true, subtree: true });

  raf = requestAnimationFrame(tick);

  // Désactiver si l'utilisateur quitte la fenêtre
  window.addEventListener("blur", () => cursor.classList.remove("is-active"));
}
```

- [ ] **Step 2: Importer et appeler dans `Layout.astro`**

Dans `src/layouts/Layout.astro`, dans le bloc `<script>` à la ligne 103-123, ajouter en haut :
```ts
import { initCustomCursor } from "../scripts/cursor";
```
Et après `initSmoothScroll();` ajouter :
```ts
initCustomCursor();
```

- [ ] **Step 3: Vérifier dans le navigateur**

Recharger en desktop (>1024px). Le cercle terracotta doit suivre la souris, grossir au hover des liens/boutons. Le curseur natif doit être masqué.

Tester en réduisant la fenêtre sous 1024px (recharger) : le cursor custom disparaît, le natif revient.

Tester avec `prefers-reduced-motion: reduce` activé dans DevTools (Rendering tab → Emulate CSS media feature) : pas de cursor custom.

- [ ] **Step 4: Commit**

```bash
git add src/scripts/cursor.ts src/layouts/Layout.astro
git commit -m "feat(animations): custom cursor with hover state"
```

---

## Task 4: Boutons magnétiques

**Files:**
- Create: `src/scripts/magnetic.ts`
- Modify: `src/layouts/Layout.astro` (import)
- Modify: composants des CTA principaux pour ajouter `data-magnetic`

- [ ] **Step 1: Créer `src/scripts/magnetic.ts`**

```ts
// Effet magnétique : les éléments avec [data-magnetic] sont attirés vers le curseur
// dans une zone de 80px. Désactivé sous 1024px et si reduced-motion.

const BREAKPOINT = 1024;
const ZONE = 80;
const STRENGTH = 0.25; // déplacement max ~ 8px sur 32px de delta
const MAX_OFFSET = 8;

export function initMagnetic(): void {
  if (typeof window === "undefined") return;
  if (window.innerWidth < BREAKPOINT) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const elements = document.querySelectorAll<HTMLElement>("[data-magnetic]");

  elements.forEach((el) => {
    let raf = 0;
    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;

    const tick = () => {
      currentX += (targetX - currentX) * 0.2;
      currentY += (targetY - currentY) * 0.2;
      el.style.transform = `translate(${currentX}px, ${currentY}px)`;
      if (Math.abs(targetX - currentX) < 0.1 && Math.abs(targetY - currentY) < 0.1) {
        raf = 0;
        return;
      }
      raf = requestAnimationFrame(tick);
    };

    const onMove = (e: MouseEvent) => {
      const rect = el.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = e.clientX - cx;
      const dy = e.clientY - cy;
      const dist = Math.hypot(dx, dy);

      if (dist < rect.width / 2 + ZONE) {
        targetX = Math.max(-MAX_OFFSET, Math.min(MAX_OFFSET, dx * STRENGTH));
        targetY = Math.max(-MAX_OFFSET, Math.min(MAX_OFFSET, dy * STRENGTH));
      } else {
        targetX = 0;
        targetY = 0;
      }
      if (!raf) raf = requestAnimationFrame(tick);
    };

    const onLeave = () => {
      targetX = 0;
      targetY = 0;
      if (!raf) raf = requestAnimationFrame(tick);
    };

    window.addEventListener("mousemove", onMove);
    el.addEventListener("mouseleave", onLeave);
  });
}
```

- [ ] **Step 2: Importer et appeler dans `Layout.astro`**

Ajouter après `initCustomCursor();` :
```ts
import { initMagnetic } from "../scripts/magnetic";
initMagnetic();
```
(Note : si l'import existe déjà en haut du bloc script, juste ajouter l'appel.)

- [ ] **Step 3: Ajouter `data-magnetic` sur les CTA principaux**

Repérer et taguer ces boutons :

- `Hero.astro` : le bouton CTA principal (ex: "Discutons de votre projet")
- `Offres.astro` : le bouton de chaque carte d'offre (ex: "Discutons de votre projet")
- `Contact.astro` : le bouton submit du formulaire
- `Header.astro` : le CTA du header (s'il y en a un, ex: "Discuter")

Pour chaque, ajouter `data-magnetic` sur la balise `<a>` ou `<button>` du CTA.

Run: `Grep -n "Discutons|<button|type=\"submit\"" src/components/Hero.astro src/components/Offres.astro src/components/Contact.astro src/components/Header.astro`
pour localiser précisément les CTA.

- [ ] **Step 4: Vérifier dans le navigateur**

Approcher le curseur des boutons taggés. Ils doivent légèrement glisser vers le curseur (max 8px). En s'éloignant, retour fluide à la position d'origine. Effet désactivé en mobile et reduced-motion.

- [ ] **Step 5: Commit**

```bash
git add src/scripts/magnetic.ts src/layouts/Layout.astro src/components/
git commit -m "feat(animations): magnetic buttons on main CTAs"
```

---

## Task 5: Reveal de texte au scroll sur les h2 de section

**Files:**
- Create: `src/scripts/textReveal.ts`
- Modify: `src/layouts/Layout.astro` (import)
- Modify: composants concernés pour ajouter `data-text-reveal` sur les h2 de section

- [ ] **Step 1: Créer `src/scripts/textReveal.ts`**

```ts
// Text reveal par mots sur les éléments [data-text-reveal].
// Utilise GSAP ScrollTrigger (déjà installé). One-shot.

import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function initTextReveal(): void {
  if (typeof window === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const elements = document.querySelectorAll<HTMLElement>("[data-text-reveal]");

  elements.forEach((el) => {
    const text = el.textContent ?? "";
    const words = text.split(/(\s+)/); // garde les espaces

    el.innerHTML = words
      .map((w) => (w.trim() === "" ? w : `<span class="reveal-word">${w}</span>`))
      .join("");

    const wordEls = el.querySelectorAll<HTMLElement>(".reveal-word");

    gsap.to(wordEls, {
      opacity: 1,
      y: 0,
      duration: 0.7,
      stagger: 0.05,
      ease: "power3.out",
      scrollTrigger: {
        trigger: el,
        start: "top 85%",
        once: true,
      },
    });
  });
}
```

- [ ] **Step 2: Importer et appeler dans `Layout.astro`**

Ajouter dans le bloc script :
```ts
import { initTextReveal } from "../scripts/textReveal";
initTextReveal();
```

- [ ] **Step 3: Ajouter `data-text-reveal` sur les h2 de section**

Cibler le `<h2>` principal de chaque section :
- `Offres.astro`
- `EtudesDeCas.astro`
- `APropos.astro` (ligne 43 : `<h2 class="text-4xl md:text-5xl font-semibold leading-tight tracking-tight text-noir-cafe">`)
- `Temoignages.astro`
- `Contact.astro`

Pour chaque, ajouter l'attribut `data-text-reveal` sur le `<h2>`.

**Important** : ne PAS ajouter sur les h2 qui contiennent déjà des `<strong>` ou autres balises imbriquées (le script utilise `textContent` ce qui détruirait le markup). Si un h2 a des balises internes, soit on simplifie le contenu, soit on saute ce titre. Vérifier visuellement chaque h2 ciblé avant d'ajouter l'attribut.

- [ ] **Step 4: Vérifier dans le navigateur**

Recharger, scroller lentement. Chaque h2 de section doit révéler ses mots en cascade (50ms entre chaque mot) au moment où il entre dans le viewport. Pas de replay si on rescroll vers le haut puis le bas. Désactivé en reduced-motion.

- [ ] **Step 5: Commit**

```bash
git add src/scripts/textReveal.ts src/layouts/Layout.astro src/components/
git commit -m "feat(animations): word-by-word reveal on section h2"
```

---

## Task 6: Compteur animé sur la stat "6+"

**Files:**
- Create: `src/scripts/counters.ts`
- Modify: `src/layouts/Layout.astro` (import)
- Modify: `src/components/APropos.astro` (taguer la stat "6+")

- [ ] **Step 1: Créer `src/scripts/counters.ts`**

```ts
// Compteur animé pour les éléments [data-counter] avec attribut data-counter-target="6".
// Animation easeOut de 0 à la valeur cible quand l'élément entre dans le viewport.

const DURATION = 1200; // ms

const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);

export function initCounters(): void {
  if (typeof window === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const elements = document.querySelectorAll<HTMLElement>("[data-counter]");
  if (elements.length === 0) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target as HTMLElement;
        const target = Number(el.dataset.counterTarget ?? "0");
        const suffix = el.dataset.counterSuffix ?? "";
        const start = performance.now();

        const tick = (now: number) => {
          const t = Math.min(1, (now - start) / DURATION);
          const value = Math.round(target * easeOut(t));
          el.textContent = `${value}${suffix}`;
          if (t < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        observer.unobserve(el);
      });
    },
    { threshold: 0.5 }
  );

  elements.forEach((el) => observer.observe(el));
}
```

- [ ] **Step 2: Importer et appeler dans `Layout.astro`**

```ts
import { initCounters } from "../scripts/counters";
initCounters();
```

- [ ] **Step 3: Modifier `APropos.astro` pour taguer la stat "6+"**

Dans le tableau `stats` (lignes 26-31), seul "6+" est animable numériquement. Modifier le rendu (ligne 80-87) pour utiliser `data-counter` quand la valeur est "6+" :

Remplacer :
```astro
{stats.map((s) => (
    <div class="text-center md:text-left">
        <p class="font-serif text-4xl md:text-5xl font-semibold text-noir-cafe leading-none mb-2">
            {s.chiffre}
        </p>
        <p class="text-sm text-sable-600">{s.label}</p>
    </div>
))}
```
par :
```astro
{stats.map((s) => (
    <div class="text-center md:text-left">
        {s.chiffre === "6+" ? (
            <p
                class="font-serif text-4xl md:text-5xl font-semibold text-noir-cafe leading-none mb-2"
                data-counter
                data-counter-target="6"
                data-counter-suffix="+"
            >0+</p>
        ) : (
            <p class="font-serif text-4xl md:text-5xl font-semibold text-noir-cafe leading-none mb-2">
                {s.chiffre}
            </p>
        )}
        <p class="text-sm text-sable-600">{s.label}</p>
    </div>
))}
```

- [ ] **Step 4: Vérifier dans le navigateur**

Scroller jusqu'à la section À propos > stats. La stat "6+" doit s'animer de 0 à 6 sur ~1.2s, easing easeOut. Les autres stats (100%, <2s, FR · EN) restent statiques. Désactivé en reduced-motion.

- [ ] **Step 5: Commit**

```bash
git add src/scripts/counters.ts src/layouts/Layout.astro src/components/APropos.astro
git commit -m "feat(animations): animated counter on stat 6+"
```

---

## Task 7: Vérification globale + build de production

**Files:** aucun

- [ ] **Step 1: Run le build de production**

```bash
npm run build
```
Expected : build OK, aucun warning TypeScript ni Astro.

- [ ] **Step 2: Run le preview**

```bash
npm run preview
```
Tester l'ensemble du site sur `http://localhost:4321` :
- Curseur custom OK en desktop, désactivé sous 1024px
- Hover cartes : lift + glow OK partout (Offres, Études de cas, Témoignages, principes À propos)
- Boutons magnétiques : Hero, Offres, Contact, Header
- Underline liens : Header + Footer
- Text reveal : h2 de chaque section au scroll
- Compteur "6+" anime à l'entrée
- Toggle dark/light : tout reste cohérent dans les deux thèmes
- Toggle région € / FCFA : pas de régression
- Menu hamburger mobile : drawer s'ouvre, liens fonctionnent

- [ ] **Step 3: Test reduced-motion**

DevTools → Rendering → Emulate CSS media feature `prefers-reduced-motion: reduce`. Recharger.
Tous les effets désactivés : pas de curseur custom, pas de magnétique, pas de reveal animé, pas de compteur.

- [ ] **Step 4: Push (optionnel — demander à Saïbo)**

Vercel rebuild automatiquement sur push main. Demander confirmation avant de push :
```bash
git push origin main
```

---

## Critères de réussite globaux

- Aucune nouvelle dépendance npm
- Build production passe sans warning
- Aucune régression sur dark/light, région, menu mobile, formulaire
- Animations fluides (60fps) sur desktop récent
- Tout désactivé en reduced-motion
- Curseur custom et magnétique désactivés sous 1024px
