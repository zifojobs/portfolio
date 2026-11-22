# Questionnaire de démarrage (« Démarrer avec Saïbo ») — plan de construction

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** une page `saibodanfakha.com/demarrer/` où un client répond seul, sur son téléphone, aux questions de cadrage ; une carte de projet se remplit à chaque réponse puis devient son dossier de démarrage (PNG) ; le dossier arrive chez Saïbo via l'agent WhatsApp (copie disque + WhatsApp + mail).

**Architecture:** côté portfolio (Astro statique), un moteur en fonctions pures (`src/lib/demarrer/`) piloté par un jeu de questions en JSON ; la page n'a pas de serveur. Côté agent (`Agent WhatsApp Perso`, Node `http` nu, VPS `agent.saibodanfakha.com`), deux routes ajoutées à `src/cloud.js` : `POST /dossier` (reçoit, valide, écrit sur disque, puis prévient) et `GET /config/<jeton>` (le lien personnalisé). Les configurations des clients et les dossiers vivent **sur le VPS seulement**.

**Tech Stack:** Astro 6 + Tailwind 4 (déjà là) · `@fontsource-variable/schibsted-grotesk` 5.x · TypeScript testé par `node --test` (comme `src/lib/estimateur.test.ts`) · agent : Node 24, `nodemailer` 10.x, tests en scripts `node test-*.js` (comme `test-partage.js`).

**Spec:** `docs/superpowers/specs/2026-11-21-questionnaire-demarrage-design.md` (approuvée le 21/11). Maquette : `<dossier du client>\.superpowers\brainstorm\1303-1795301348\content\parcours.html`.

## Global Constraints

- ⚠️ Dépôt portfolio **public** : aucune donnée de client (prénom, société, numéro, NINEA, budget, logo) dans un fichier commité, un test, un message de commit ou un journal Vercel.
- Pas de prix dans le parcours ; pas de compte client ; pas de maquette de site ; aucune promesse de délai de réalisation (la durée figure dans la proposition, pas dans le dossier).
- 10 questions (13 au départ ; NINEA/RCCM, autorisation et parcours à l’étranger retirés par Saïbo le 22/11), une par écran ; la question budget est **toujours la dernière** ; chaque question porte un « Pourquoi je vous le demande » ; vouvoiement ; 8 minutes maximum.
- Page `/demarrer/` : `noindex, nofollow`, exclue du sitemap ; aucun son, aucune musique ; téléphone d'abord (390 px), puis ordinateur.
- Police **Schibsted Grotesk** seule (titres 800, `letter-spacing:-0.025em` ; texte 400). Page en neutres : fond `#f6f3ee`, encre `#1b1b1b`, texte secondaire `#4c524d`, bordures `#cfc6b8`. Les couleurs du client ne vivent que dans la carte et le dossier. Retirés de la charte (jamais) : étiquette en capitales au-dessus d'un titre, numéros 01-03, compteurs, boules floues, guillemet décoratif, « ce n'est pas X, c'est Y ».
- Le jeton du lien personnalisé passe dans le **fragment** (`/demarrer/#t=<jeton>`), jamais dans le chemin ni la requête (il n'atteint ni Vercel ni ses journaux).
- Endpoint : origine acceptée `https://saibodanfakha.com` seule (+ `ORIGINE_DEV` en local uniquement) ; corps ≤ 256 Ko ; 5 requêtes par heure et par IP, 200 dossiers valides par heure au total, 10 notifications par 24 h (au-delà : disque seul + un avis) ; n'exécute rien de ce qu'il reçoit.
- « Envoyé » ne s'affiche qu'après un 200 de l'agent ; 200 = **copie disque écrite**. Les notifications partent après, et leur échec ne change pas le 200.
- Déploiement portfolio **par git uniquement** (jamais la CLI Vercel, jamais `git add -A`) ; agent : `scp` + `pm2 restart agent-whatsapp`, sauvegardes `*.bak-AAAA-MM-JJ` avant écrasement.
- Relecture de sécurité par un agent séparé, en lecture seule, **avant** la mise en prod (règle du hub du 20/10).
- Numéro WhatsApp de Saïbo pour le bouton bonus : `221775277164` (celui de l'estimateur).

## Review Focus

1. **Réseau coupé ou agent arrêté au moment d'« Envoyer »** : message clair, bouton « Réessayer », saisie intacte → test `envoi.test.ts › échec réseau garde la saisie` (Task 3).
2. **Page rechargée ou fermée au milieu** : le client reprend à la même question avec ses réponses → test `brouillon.test.ts › reprise` (Task 3).
3. **`localStorage` refusé (navigation privée, iOS)** : le parcours marche, sans brouillon, sans erreur → test `brouillon.test.ts › stockage qui lève` (Task 3).
4. **Double appui sur « Envoyer » / réessai après un 200 perdu** : un seul dossier, une seule notification → test `test-serveur-dossier.js › même idDossier deux fois` (Task 7).
5. **Texte avec émojis, retours à la ligne, 1 000 caractères** : le résumé WhatsApp reste une ligne, ≤ 600 caractères, sans tabulation ni 4 espaces de suite (règle Meta des paramètres de modèle) → test `test-dossier.js › résumé d'un texte hostile` (Task 6).

---

### Task 1: Le jeu de questions « visibilité, sécurité privée » et ses types

**Files:**
- Create: `src/lib/demarrer/types.ts`
- Create: `src/data/demarrer/visibilite-securite.json`
- Create: `src/lib/demarrer/jeu.ts`
- Test: `src/lib/demarrer/jeu.test.ts`

**Interfaces:**
- Produces (`types.ts`) :
  - `type TypeChamp = "texte" | "choix" | "puces" | "couleur" | "logo"`
  - `interface Option { v: string; l: string; accent?: string }`
  - `interface Champ { id: string; type: TypeChamp; libelle?: string; options?: Option[]; autre?: boolean; max?: number; facultatif?: boolean; carte?: "nom" | "tags"; sansLien?: boolean; prerempli?: "prenom" | "societe"; dossier?: string }` — `dossier` = libellé de la ligne dans « Ce que vous m'avez dit ».
  - `interface Question { id: string; titre: string; pourquoi: string; champs: Champ[]; auMoinsUn?: boolean }`
  - `interface Jeu { id: string; version: number; titreDossier: string; chemin: string[]; questions: Question[] }`
  - `type Valeur = string | string[]` ; `type Reponses = Record<string, Valeur>` (clé = `champ.id` ; texte libre d'une option « autre » sous la clé `${champ.id}.autre`)
  - `interface ConfigClient { prenom: string; societe: string; couleur: string; accent: string; logo?: string; jeu: string }`
- Produces (`jeu.ts`) : `verifierJeu(jeu: Jeu): string[]` (liste d'erreurs, vide si correct) · `chargerJeu(id: string): Jeu` (import statique du JSON, lève si id inconnu) · `JEUX: Record<string, Jeu>`.

- [ ] **Step 1: Écrire le test qui échoue** — `jeu.test.ts` lit le JSON par `readFileSync` + `JSON.parse` et vérifie :

```ts
it('13 questions, ids uniques, budget en dernier', () => {
  assert.equal(jeu.questions.length, 13)
  assert.equal(jeu.questions.at(-1)!.id, 'budget')
  assert.deepEqual(verifierJeu(jeu), [])
})
it('chaque question a un pourquoi non vide', () => { for (const q of jeu.questions) assert.ok(q.pourquoi.trim()) })
it('verifierJeu signale un id de champ dupliqué', () => { /* copie du jeu avec deux champs "societe" */ assert.match(verifierJeu(copie).join(), /dupliqué/) })
it('verifierJeu signale un budget qui n’est pas en dernier', () => { assert.match(verifierJeu(inverse).join(), /budget/) })
it('aucun prix dans les titres ni les pourquoi', () => { assert.ok(!/\d[\d  ]*\s?F\b/.test(texteDesQuestionsHorsBudget)) })
```

- [ ] **Step 2:** `node --test src/lib/demarrer/jeu.test.ts` → FAIL (module introuvable).

- [ ] **Step 3: Écrire `types.ts`, `jeu.ts` et le JSON.** `verifierJeu` contrôle : ids de questions uniques entre questions, ids de champs uniques entre tous les champs du jeu (une question et un champ peuvent porter le même id, ex. `societe`) ; dernière question `budget` ; tout `choix`/`puces`/`couleur` a au moins 2 options ; `pourquoi` non vide. Le JSON (copie exacte, reprise de la spec §7 ; `version: 1`) :

| id | titre | pourquoi | champs |
|---|---|---|---|
| `identite` | Votre prénom et votre nom ? | Pour vous écrire à votre nom, tout simplement. | `prenom` texte max 60 prerempli=prenom ; `nom` texte max 60 facultatif |
| `societe` | Comment s'appelle officiellement votre société ? | Votre nom de domaine sera enregistré au nom de votre société, jamais au mien. Il vous appartient. | `societe` texte max 100 carte=nom prerempli=societe ; `couleur` couleur sansLien, libelle « La couleur de votre marque », options `#045b5b`/accent `#f39221` « Vert pétrole », `#1d3557`/`#e9c46a` « Bleu nuit », `#7a1f2b`/`#f4a261` « Bordeaux », `#8a4b2a`/`#f2cc8f` « Terre », `#1f5130`/`#e9c46a` « Vert forêt », `#1b1b1b`/`#f39221` « Noir » ; `logo` logo sansLien facultatif, libelle « Votre logo (facultatif) » |
| `legal` | Votre NINEA et votre RCCM ? | Ils sont indispensables pour enregistrer votre domaine et écrire les mentions légales du site. | auMoinsUn ; `ninea_rccm` texte max 120 facultatif ; `legal_plus_tard` choix facultatif, options `plus-tard` « Je les envoie plus tard » |
| `autorisation` | Où en est votre autorisation d'exercer ? | Rien de public ne sortira avant qu'elle soit obtenue : c'est votre crédibilité. | `autorisation` choix (`obtenue` Obtenue · `en-cours` En cours · `pas-encore` Pas encore) dossier « Autorisation » ; `autorisation_ref` texte max 80 facultatif libelle « Sa référence, si vous l'avez » |
| `numero` | Quel numéro verront vos clients, sur WhatsApp et sur le site ? | Il sera partout : il doit être celui de la société, pas un numéro personnel. | `numero` choix (`ligne-dediee` Une ligne dédiée, à créer · `existant` Un numéro existant) ; `numero_valeur` texte max 20 facultatif libelle « Le numéro, s'il existe déjà » |
| `services` | Que proposez-vous à vos clients ? | Cochez tout ce qui s'applique : chaque service aura sa place sur votre page. | `services` puces autre carte=tags dossier « Services » (`securite-privee` Sécurité privée · `telesurveillance` Télésurveillance · `incendie` Sécurité incendie · `gardiennage` Rondes et gardiennage) |
| `formations` | Quelles formations proposez-vous ? | Je n'écris rien que vous n'avez pas confirmé, surtout pas le sens d'un sigle. | `formations` puces autre carte=tags dossier « Formations » (`sst` SST · `incendie-formation` Sécurité incendie · `agent` Agent de sécurité · `aucune` Aucune pour l'instant) ; `sst_sens` texte max 120 facultatif libelle « Que veut dire « SST » sur vos supports ? » ; `formations_details` choix facultatif libelle « Durée, public, places, lieu » (`je-precise` Je les précise plus tard · `sur-demande` Sur demande) |
| `zones` | Quelles zones couvrez-vous ? | Pour que Google vous montre aux bonnes personnes, au bon endroit. | `zones` puces autre carte=tags dossier « Zones » (`dakar` Dakar · `thies` Thiès · `mbour` Mbour · `kaolack` Kaolack · `saint-louis` Saint-Louis · `touba` Touba · `ziguinchor` Ziguinchor · `senegal` Tout le Sénégal) |
| `cibles` | Qui sont vos clients prioritaires ? | On parle d'abord à ceux qui vous font vivre. | `cibles` puces dossier « Clients visés » (`entreprises` Entreprises · `commerces` Commerces · `evenements` Événements · `banques-hotels` Banques et hôtels · `ong` ONG · `particuliers` Particuliers) |
| `etranger` | Votre parcours à l'étranger : avez-vous des justificatifs à montrer ? | C'est votre meilleure preuve. On ne la publie qu'avec eux. | `etranger` choix (`oui` Oui · `certains` Certains · `pas-encore` Pas encore) |
| `reponse` | Qui répondra aux messages de vos clients, et en combien de temps ? | Un client qui attend part chez le concurrent. | `repondant` choix (`moi` Moi-même · `equipe` Une personne de l'équipe · `a-voir` À décider) ; `delai_reponse` choix libelle « Sous quel délai » (`heure` Dans l'heure · `jour` Dans la journée · `48h` Sous 48 h) |
| `photos` | La séance photo : quel jour vous arrange, et qui est d'accord pour apparaître ? | De vraies photos de votre équipe, avec l'accord écrit de chacun. | `photos_jour` puces (`semaine` En semaine · `samedi` Le samedi · `dimanche` Le dimanche · `a-voir` Je ne sais pas encore) ; `photos_qui` texte max 200 facultatif libelle « Qui est d'accord ? » |
| `budget` | Votre budget de départ, et votre budget par mois ? | Pour vous proposer ce qui vous sert, sans rien de superflu. | `budget_depart` choix dossier « Budget de départ » (`moins-175` Moins de 175 000 F · `175-350` 175 000 – 350 000 F · `350-800` 350 000 – 800 000 F · `plus-800` Plus de 800 000 F · `en-parler` Je préfère en parler) ; `budget_mois` choix libelle « Par mois » (`aucun` Pas de suivi pour l'instant · `moins-25` Moins de 25 000 F · `25-50` 25 000 – 50 000 F · `plus-50` Plus de 50 000 F · `en-parler` Je préfère en parler) |

`titreDossier`: `"{societe}, prête à être trouvée."` · `chemin`: `["Les fondations", "Être trouvé", "Le site", "Le lancement", "Le suivi"]` (étapes de `<plan de visibilité du client>` §3, **sans durée**).
⚠️ Les tranches de budget sont des **propositions** calées sur `FOURCHETTES` de `src/lib/estimateur.ts` : Saïbo les valide avant la mise en ligne (Task 9, étape 1). Elles ne contredisent pas la grille publique.

- [ ] **Step 4:** `node --test src/lib/demarrer/jeu.test.ts` → PASS (5 tests).
- [ ] **Step 5: Commit** (branche `feat/demarrer`, créée depuis `main` après `git pull`)

```bash
git add src/lib/demarrer/types.ts src/lib/demarrer/jeu.ts src/lib/demarrer/jeu.test.ts src/data/demarrer/visibilite-securite.json
git commit -m "Démarrer : jeu de questions « visibilité, sécurité privée » et ses types"
```

---

### Task 2: Le moteur (réponses, carte, dossier, résumé, couleurs)

**Files:**
- Create: `src/lib/demarrer/moteur.ts`
- Test: `src/lib/demarrer/moteur.test.ts`

**Interfaces:**
- Consumes: `Jeu`, `Question`, `Champ`, `Reponses`, `ConfigClient` (Task 1).
- Produces:
  - `questionsVisibles(jeu: Jeu, avecLien: boolean): Question[]` — retire les champs `sansLien` quand `avecLien` ; garde toutes les questions (13).
  - `estRepondue(q: Question, r: Reponses): boolean` — chaque champ non `facultatif` a une valeur non vide (texte trimé, tableau non vide, option `autre` ⇒ `${id}.autre` non vide) ; avec `auMoinsUn`, un champ quelconque suffit.
  - `carte(jeu: Jeu, r: Reponses): { nom: string; tags: string[]; dernier: string | null }` — `nom` = valeur du champ `carte:"nom"` en capitales ; `tags` = libellés des options choisies des champs `carte:"tags"`, dans l'ordre des champs puis des options du jeu (pas l'ordre des clics), + texte « autre » ; `dernier` = dernier tag ajouté par rapport à l'appel précédent (passé en 3ᵉ paramètre optionnel `avant?: string[]`).
  - `lignesDossier(jeu: Jeu, r: Reponses): { libelle: string; valeur: string }[]` — un élément par champ ayant `dossier`, valeurs jointes par « , », champs vides omis.
  - `titreDossier(jeu: Jeu, r: Reponses): string` — remplace `{societe}`.
  - `resumeTexte(jeu: Jeu, r: Reponses): string` — multi-lignes « Titre de question : réponse » pour le message `wa.me` (≤ 1 500 caractères, coupé proprement avec « … »).
  - `texteSur(hex: string): "#ffffff" | "#1b1b1b"` — contraste WCAG le plus fort.
  - `progression(index: number, total: number): number` — pourcentage entier 0-100.

- [ ] **Step 1: Écrire les tests qui échouent** (valeurs fictives : société « Exemple Sécurité », jamais un vrai client) :

```ts
it('estRepondue : texte vide = non', () => assert.equal(estRepondue(qSociete, { societe: '  ' }), false))
it('estRepondue : option autre sans texte = non', () => assert.equal(estRepondue(qServices, { services: ['autre'] }), false))
it('estRepondue : auMoinsUn (legal) avec plus-tard = oui', () => assert.equal(estRepondue(qLegal, { legal_plus_tard: 'plus-tard' }), true))
it('questionsVisibles avec lien retire couleur et logo', () => assert.ok(!questionsVisibles(jeu, true)[1].champs.some(c => c.id === 'couleur')))
it('carte : nom en capitales, tags dans l’ordre, dernier ajouté', () => {
  const c = carte(jeu, { societe: 'Exemple Sécurité', services: ['incendie', 'securite-privee'], zones: ['dakar'] }, ['Sécurité privée', 'Dakar'])
  assert.equal(c.nom, 'EXEMPLE SÉCURITÉ'); assert.deepEqual(c.tags, ['Sécurité privée', 'Sécurité incendie', 'Dakar']); assert.equal(c.dernier, 'Sécurité incendie')
})
it('titreDossier', () => assert.equal(titreDossier(jeu, { societe: 'Exemple Sécurité' }), 'Exemple Sécurité, prête à être trouvée.'))
it('resumeTexte coupé à 1 500', () => assert.ok(resumeTexte(jeu, { societe: 'x'.repeat(5000) }).length <= 1500))
it('texteSur', () => { assert.equal(texteSur('#045b5b'), '#ffffff'); assert.equal(texteSur('#f39221'), '#1b1b1b') })
it('progression', () => { assert.equal(progression(0, 13), 0); assert.equal(progression(13, 13), 100) })
```

- [ ] **Step 2:** `node --test src/lib/demarrer/moteur.test.ts` → FAIL.
- [ ] **Step 3:** Implémenter `moteur.ts` (fonctions pures, aucune dépendance au DOM).
- [ ] **Step 4:** `node --test src/lib/demarrer/` → PASS (Task 1 + Task 2).
- [ ] **Step 5: Commit** — `git add src/lib/demarrer/moteur.ts src/lib/demarrer/moteur.test.ts` ; message « Démarrer : moteur (carte, dossier, résumé) ».

---

### Task 3: Brouillon et envoi (côté navigateur, testables sans navigateur)

**Files:**
- Create: `src/lib/demarrer/brouillon.ts`, `src/lib/demarrer/envoi.ts`
- Test: `src/lib/demarrer/brouillon.test.ts`, `src/lib/demarrer/envoi.test.ts`

**Interfaces:**
- Consumes: `Reponses` (Task 1).
- Produces:
  - `interface Brouillon { index: number; reponses: Reponses; idDossier: string }`
  - `cleBrouillon(jeuId: string, jeton: string | null): string` → `demarrer:${jeuId}:${jeton ?? "libre"}`
  - `lireBrouillon(stockage: Pick<Storage,"getItem">, cle: string): Brouillon | null` — JSON invalide, forme inattendue ou exception ⇒ `null`.
  - `ecrireBrouillon(stockage: Pick<Storage,"setItem">, cle: string, b: Brouillon): void` — avale toute exception.
  - `effacerBrouillon(stockage: Pick<Storage,"removeItem">, cle: string): void` — idem (appelé après un 200).
  - `interface Dossier { version: 1; idDossier: string; jeu: string; jeton: string | null; envoyeLe: string; reponses: Reponses }`
  - `URL_AGENT = "https://agent.saibodanfakha.com"`
  - `envoyerDossier(d: Dossier, f: typeof fetch = fetch): Promise<{ ok: true } | { ok: false; message: string }>` — `POST ${URL_AGENT}/dossier`, `Content-Type: application/json`, délai max 20 s (`AbortSignal.timeout(20000)`) ; `ok` seulement sur statut 200 ; messages : réseau/délai ⇒ « La connexion a échoué. Vos réponses sont gardées : réessayez dans un instant. » ; 429 ⇒ « Trop d'envois d'un coup. Réessayez dans une heure, vos réponses sont gardées. » ; autre ⇒ « L'envoi n'a pas abouti. Vos réponses sont gardées : réessayez, ou envoyez-les-moi sur WhatsApp. »
  - `chargerConfig(jeton: string, f: typeof fetch = fetch): Promise<ConfigClient | null>` — `GET ${URL_AGENT}/config/${jeton}` ; jeton hors `^[A-Za-z0-9_-]{16,64}$`, 404, réseau ⇒ `null` (le parcours s'ouvre en mode libre).

- [ ] **Step 1: Tests qui échouent**

```ts
// brouillon.test.ts — faux stockage en Map
it('reprise : écrit puis relit le même brouillon', ...)
it('stockage qui lève : lire → null, écrire/effacer ne lèvent pas', ...)   // Review Focus 3
it('JSON abîmé → null', ...)
// envoi.test.ts — faux fetch
it('200 → ok', ...)
it('échec réseau garde la saisie : ok false + message « Vos réponses sont gardées »', ...)  // Review Focus 1
it('429 → message « dans une heure »', ...)
it('500 → ok false', ...)
it('chargerConfig : jeton "../x" → null sans appel réseau', ...)
it('chargerConfig : 404 → null', ...)
```

- [ ] **Step 2:** `node --test src/lib/demarrer/` → FAIL sur les nouveaux fichiers.
- [ ] **Step 3:** Implémenter les deux modules.
- [ ] **Step 4:** `node --test src/lib/demarrer/` → PASS.
- [ ] **Step 5: Commit** — « Démarrer : brouillon local et envoi à l'agent ».

---

### Task 4: Le dossier en image (PNG)

**Files:**
- Create: `src/lib/demarrer/png.ts`
- Test: `src/lib/demarrer/png.test.ts`

**Interfaces:**
- Consumes: `lignesDossier`, `titreDossier`, `texteSur` (Task 2) ; `ConfigClient` couleurs.
- Produces:
  - `couperLignes(texte: string, largeurMax: number, mesurer: (s: string) => number): string[]` — coupe aux espaces ; un mot plus long que la ligne est coupé en force.
  - `dessinerDossier(ctx: CanvasRenderingContext2D, d: { date: string; titre: string; lignes: {libelle:string;valeur:string}[]; chemin: string[]; couleur: string; accent: string; logo?: HTMLImageElement }): void` — format **1080 × 1920**, fond `couleur`, texte `texteSur(couleur)`, mêmes blocs que l'écran du dossier (maquette ③) : « Dossier de démarrage · {date} », titre 800, « Ce que vous m'avez dit », « Le chemin » (une pastille par étape, la première en `accent`), « Je reviens vers vous sous 48 h avec la proposition chiffrée. », pied « saibodanfakha.com ». Police `"Schibsted Grotesk Variable"` chargée avant (`document.fonts.load`).
  - `partagerOuTelecharger(canvas: HTMLCanvasElement, nomFichier: string): Promise<void>` — `navigator.canShare({ files })` ⇒ `navigator.share` (le client l'envoie sur WhatsApp en un geste) ; sinon lien `download`. Nom : `dossier-de-demarrage.png` (aucun nom de client dans le nom de fichier).

- [ ] **Step 1: Tests qui échouent** (seulement `couperLignes`, avec `mesurer = s => s.length * 10`) : phrase coupée à 100 px en lignes ≤ 100 ; mot de 30 lettres coupé en force ; chaîne vide ⇒ `[]`.
- [ ] **Step 2:** `node --test src/lib/demarrer/png.test.ts` → FAIL.
- [ ] **Step 3:** Implémenter `png.ts`.
- [ ] **Step 4:** PASS ; le rendu réel se vérifie dans la recette de la Task 5.
- [ ] **Step 5: Commit** — « Démarrer : dossier en PNG (partage ou téléchargement) ».

---

### Task 5: La page `/demarrer/`

**Files:**
- Create: `src/layouts/LayoutDemarrer.astro`, `src/pages/demarrer/index.astro`, `src/scripts/demarrer.ts`
- Create: `public/demarrer/saibo.jpg` (depuis `marque/photos-saibo/saibo-portrait-face.jpg`, recadré carré 192 × 192, JPEG qualité 82, ≤ 25 Ko)
- Modify: `astro.config.mjs` (filtre du sitemap), `package.json` (`@fontsource-variable/schibsted-grotesk`)

**Interfaces:**
- Consumes: tout `src/lib/demarrer/` (Tasks 1-4).
- Produces: la page. Rien d'autre ne dépend d'elle.

- [ ] **Step 1: Dépendance et sitemap** — `npm install @fontsource-variable/schibsted-grotesk@^5.3.0` ; dans `astro.config.mjs` : `sitemap({ filter: (page) => !page.includes('/demarrer/') })`.
- [ ] **Step 2: `LayoutDemarrer.astro`** — page autonome (sans `Header`/`Footer` ni script de thème du site) : `<meta name="robots" content="noindex, nofollow">`, titre « Démarrer votre projet — Saïbo Danfakha », pas de balises Open Graph d'image, import de la police, fond `#f6f3ee`, `max-width: 480px` centré (le téléphone d'abord ; sur ordinateur la colonne reste au centre).
- [ ] **Step 3: `index.astro` + `demarrer.ts`** — le comportement :
  1. Lecture de `location.hash` (`#t=`) ⇒ `chargerConfig` ; config ⇒ mode lien (couleurs, logo, « Bonjour {prenom} », champs `prerempli` remplis, champs `sansLien` retirés) ; sinon mode libre.
  2. Écran d'accueil : photo de Saïbo, « Bonjour {prenom}, » ou « Bonjour, », « Je vais vous poser 13 questions, environ 8 minutes. Vos réponses me permettent de vous préparer une proposition juste. », bouton « Commencer » (reprend le brouillon s'il existe : « Reprendre là où vous en étiez »).
  3. Un écran par question (maquette ①-②) : en-tête photo + « Saïbo Danfakha » + « question n sur 13 » + barre `progression` ; titre ; encadré « **Pourquoi je vous le demande :** {pourquoi} » ; champs (puces à toucher, cibles de 44 px min.) ; « Continuer » désactivé tant que `estRepondue` est faux ; « Retour » discret. Le brouillon s'écrit à chaque changement.
  4. Carte du projet fixée en bas : vide (« Votre projet se dessine au fil de vos réponses… », bordure en pointillés) puis couleur du client, `nom`, `tags`, tag `dernier` sur fond `accent` ; logo en haut à droite si présent. Le logo déposé est réduit à 256 px max (canvas) en PNG avant d'être gardé ; types acceptés : PNG, JPEG.
  5. Dernière question ⇒ bouton « Envoyer mon dossier » (désactivé pendant l'envoi : Review Focus 4). Erreur ⇒ message de `envoyerDossier` + « Réessayer » + lien « Envoyer sur WhatsApp à la place ».
  6. 200 ⇒ `effacerBrouillon`, puis la carte devient le dossier : `document.startViewTransition` avec `view-transition-name: carte` sur la carte et sur le dossier ; sans l'API ou avec `prefers-reduced-motion`, bascule directe. Dossier (maquette ③) + « Enregistrer mon dossier » (`partagerOuTelecharger`) + « Envoyer aussi à Saïbo sur WhatsApp » (`https://wa.me/221775277164?text=` + `encodeURIComponent(resumeTexte(...))`, facultatif).
- [ ] **Step 4: Construire** — `npm run build` → sans erreur ; `dist/demarrer/index.html` contient `noindex` ; `grep -c demarrer dist/sitemap-0.xml` → `0`.
- [ ] **Step 5: Recette navigateur** (playwright-core + Chromium ms-playwright, serveur `npm run preview -- --host 127.0.0.1`, agent local de la Task 7 sur `ORIGINE_DEV=http://127.0.0.1:4321`) à 390 × 844 puis 1280 × 800 : parcours complet en mode libre ; rechargement à la question 6 ⇒ reprise à la 6 ; agent arrêté ⇒ message + « Réessayer », réponses gardées ; agent relancé ⇒ 200 ⇒ dossier ; PNG téléchargé ouvert et regardé (texte lisible, rien ne déborde) ; aucun défilement horizontal. Captures dans le dossier temporaire, pas dans le dépôt.
- [ ] **Step 6: Commit** — `git add` des fichiers listés + `package.json` `package-lock.json` `astro.config.mjs` ; message « Démarrer : la page /demarrer/ (noindex, hors sitemap) ».

---

### Task 6: Agent — validation et résumé d'un dossier

**Files (dans `E:\DOSSIER FREELANCE\Projets Web\Agent WhatsApp Perso\`) :**
- Create: `src/dossier.js`, `jeux/visibilite-securite.json` (copie conforme de `saibodanfakha/src/data/demarrer/visibilite-securite.json`)
- Test: `test-dossier.js` (style `test-partage.js` : `check(label, cond)`, sortie 1 si échec)

**Interfaces:**
- Consumes: le format `Dossier` et le JSON du jeu (Tasks 1 et 3) — mêmes noms de champs.
- Produces:
  - `chargerJeux(dossier: string): Record<string, Jeu>` — lit `jeux/*.json`.
  - `validerDossier(corps: unknown, jeux): { ok: true, dossier } | { ok: false, raison: string }` — `version === 1` ; `idDossier` = UUID v4 ; `jeu` connu ; `jeton` `null` ou `^[A-Za-z0-9_-]{16,64}$` ; `envoyeLe` date ISO ; toute clé de `reponses` = un id de champ du jeu ou `${id}.autre` (sinon refus) ; texte ≤ `max` du champ (défaut 300), autre ≤ 100 ; `choix` ∈ options ; `puces` ⊆ options (+ `autre`), sans doublon ; `couleur` = une option du champ ; `logo` commence par `data:image/png;base64,` ou `data:image/jpeg;base64,` et ≤ 120 000 caractères ; `prenom`, `societe`, `budget_depart`, `budget_mois` présents.
  - `resumeWhatsApp(dossier, jeu): { societe: string, prenom: string, resume: string }` — chaque valeur : retours à la ligne et tabulations ⇒ « · », espaces multiples ⇒ un seul, `societe`/`prenom` ≤ 60, `resume` ≤ 600 (services, zones, cibles, autorisation, budgets ; coupé avec « … »).
  - `nomFichier(maintenant: Date, idDossier: string): string` → `2026-11-22_163005_<8 premiers caractères de l'id>.json`.

- [ ] **Step 1: Tests qui échouent** — dossier fictif valide ⇒ `ok` ; clé inconnue ⇒ refus ; choix hors options ⇒ refus ; logo `data:image/svg+xml` ⇒ refus ; texte de 301 caractères dans `societe` (max 100) ⇒ refus ; `__proto__` comme clé de réponse ⇒ refus ; **résumé d'un texte hostile** (émojis, `\n\t`, 1 000 caractères, 6 espaces) ⇒ une ligne, ≤ 600, `!/[\n\t]| {4,}/` (Review Focus 5) ; `nomFichier`.
- [ ] **Step 2:** `node test-dossier.js` → échecs.
- [ ] **Step 3:** Implémenter `src/dossier.js` (ESM, sans dépendance).
- [ ] **Step 4:** `node test-dossier.js` → tout ✅ ; `node test-partage.js` et `node test-alerte.js` toujours verts.

---

### Task 7: Agent — les routes `/dossier` et `/config`, le mail

**Files:**
- Create: `src/mail.js`, `src/serveur-dossier.js` (les dossiers `dossiers/` et `clients/` n'existent que sur le VPS, Task 9)
- Modify: `src/cloud.js` (le `http.createServer` : 2 routes + `OPTIONS`, avant le `404` final ; rien d'autre ne bouge)
- Modify: `package.json` (`nodemailer@^10.6.1`)
- Test: `test-serveur-dossier.js`

**Interfaces:**
- Consumes: `validerDossier`, `resumeWhatsApp`, `nomFichier`, `chargerJeux` (Task 6) ; `envoyerCorps`/`sendText` et `alerterSaibo` existants de `cloud.js`.
- Produces:
  - `creerLimiteur({ parIp: number, total: number, fenetreMs: number, maintenant: () => number }): (ip: string) => boolean` — `true` = autorisé.
  - `entetesCors(origine: string | undefined, autorisees: string[]): Record<string,string>` — `Access-Control-Allow-Origin` = l'origine seulement si elle est dans la liste ; `Allow-Methods: POST, GET, OPTIONS` ; `Allow-Headers: Content-Type` ; `Vary: Origin`.
  - `traiterDossier(req, res, deps): Promise<void>` avec `deps = { jeux, ecrire(nom, contenu), dejaVu(id): boolean, marquer(id), limiteur, notifier(dossier), origines }` — ordre : origine refusée ⇒ 403 ; limiteur ⇒ 429 ; corps > 256 Ko ⇒ 413 (lecture interrompue) ; JSON invalide ou `validerDossier` refuse ⇒ 400 `{ "erreur": raison }` ; `dejaVu(idDossier)` ⇒ 200 sans rien réécrire ni notifier (Review Focus 4) ; sinon `ecrire` (fichier `0600` dans `DOSSIERS_DIR`) **puis** 200 `{ "ok": true }`, **puis** `notifier` sans `await` dans la réponse (ses erreurs sont journalisées et passent par `alerterSaibo`).
  - `traiterConfig(req, res, jeton, deps)` — jeton hors regex ⇒ 404 ; lit `CLIENTS_DIR/<jeton>.json` ⇒ 200 JSON `ConfigClient` ; absent ⇒ 404 ; même CORS ; limiteur dédié (30/h/IP).
  - `notifier(dossier)` dans `cloud.js` : (1) modèle WhatsApp `process.env.WA_MODELE_DOSSIER`, langue `fr`, 3 paramètres de corps `{societe}`, `{prenom}`, `{resume}`, vers `SAIBO_WA` ; s'il échoue ⇒ `sendText` du même texte (passe si la fenêtre de 24 h est ouverte) ; (2) `envoyerMail(dossier, resume)` — indépendants : l'échec de l'un n'empêche pas l'autre.
  - `envoyerMail({ sujet, texte, piecesJointes })` dans `src/mail.js` : `nodemailer.createTransport({ host: SMTP_HOST, port: 587, secure: false, requireTLS: true, auth: { user: SMTP_USER, pass: SMTP_PASS } })`, vers `MAIL_TO` ; sujet `Nouveau dossier : {societe} · {prenom}` ; corps = `resumeTexte` lisible ; pièce jointe = le JSON du dossier.
  - IP du client : en-tête `X-Real-IP` (posé par nginx, Task 9), sinon `req.socket.remoteAddress`.
  - Nouvelles variables `.env` : `DOSSIERS_DIR=/root/agent-whatsapp/dossiers`, `CLIENTS_DIR=/root/agent-whatsapp/clients`, `ORIGINES=https://saibodanfakha.com` (en local : `,http://127.0.0.1:4321`), `WA_MODELE_DOSSIER`, `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, `MAIL_TO`. Absentes ⇒ la route `/dossier` répond 503 et l'agent continue de répondre aux contacts (ne jamais `process.exit` pour elles).

- [ ] **Step 1: Tests qui échouent** (`test-serveur-dossier.js`, serveur `http` local sur un port libre, dépendances factices, **aucun appel réseau externe**) : origine `https://evil.example` ⇒ 403 ; `OPTIONS` depuis l'origine permise ⇒ 204 + en-têtes CORS ; 6ᵉ envoi de la même IP dans l'heure ⇒ 429 ; corps de 300 Ko ⇒ 413 ; dossier valide ⇒ 200 **et** `ecrire` appelé avant la réponse **et** `notifier` appelé une fois ; **même idDossier deux fois** ⇒ 2 × 200, 1 écriture, 1 notification ; `notifier` qui lève ⇒ toujours 200 ; `/config/../../etc/passwd` ⇒ 404 ; `/config/<jeton inconnu>` ⇒ 404 ; variables absentes ⇒ 503.
- [ ] **Step 2:** `node test-serveur-dossier.js` → échecs.
- [ ] **Step 3:** Implémenter `src/serveur-dossier.js`, `src/mail.js` ; brancher dans `cloud.js` (import + routes + `notifier`). `dejaVu`/`marquer` : un `Set` en mémoire + la présence d'un fichier dont le nom contient l'id (survit à un redémarrage).
- [ ] **Step 4:** `npm install nodemailer@^10.6.1` ; `node test-serveur-dossier.js` → tout ✅ ; `node test-dossier.js`, `test-partage.js`, `test-alerte.js`, `test-memory.js`, `test-decoupe.js`, `test-reessai.js` → verts.
- [ ] **Step 5: Essai local de bout en bout** — `.env` local avec `ORIGINES=...,http://127.0.0.1:4321`, `DOSSIERS_DIR` dans le dossier temporaire, `notifier` remplacé par un journal (`DOSSIER_ESSAI=1` : ni WhatsApp ni mail) ; la recette de la Task 5 tourne contre lui.

---

### Task 8: Relecture de sécurité (agent séparé, lecture seule)

**Files:** aucun en écriture par le relecteur.

- [ ] **Step 1:** Lancer un agent `ecc:security-reviewer` **en lecture seule** sur : `saibodanfakha/src/lib/demarrer/`, `src/pages/demarrer/`, `src/scripts/demarrer.ts`, et `Agent WhatsApp Perso/src/{dossier,serveur-dossier,mail,cloud}.js`. Points imposés : CORS et origine, limites de taille et de fréquence, traversée de chemin sur `/config/`, pollution de prototype par les clés de `reponses`, injection dans le mail (en-têtes, sujet), paramètres du modèle WhatsApp, données de client possibles dans le dépôt public ou les journaux (`pino` : ne jamais journaliser le corps), jeton dans le fragment seulement, `innerHTML` côté page (tout texte du client passe par `textContent`).
- [ ] **Step 2:** Corriger chaque point retenu, avec un test quand c'est testable ; relancer les suites des Tasks 1-7 → vertes.
- [ ] **Step 3:** Contre-relecture courte par un second agent sur les seuls correctifs.
- [ ] **Step 4: Commit** portfolio des correctifs éventuels — « Démarrer : correctifs de la relecture de sécurité ».

---

### Task 9: Mise en service

Chaque étape marquée **Saïbo** attend sa réponse ; rien ne se publie avant les étapes 1 à 3.

- [ ] **Step 1 (Saïbo) : valider les contenus** — les 13 questions et leurs « pourquoi » (Task 1), les tranches de budget, les 5 étapes du chemin sans durée, la phrase « sous 48 h ». Écarts ⇒ corriger le JSON (portfolio **et** copie de l'agent), relancer `node --test src/lib/demarrer/` et `node test-dossier.js`.
- [ ] **Step 2 (Saïbo) : soumettre le modèle WhatsApp** dans le gestionnaire WhatsApp de Meta : nom `nouveau_dossier`, catégorie **Utility**, langue **French**, corps exact : `Nouveau dossier de démarrage : {{1}} · {{2}}. Résumé : {{3}}. Le dossier complet est dans votre boîte mail.` (exemples : `Exemple Sécurité`, `Awa`, `Services : sécurité privée · Zones : Dakar`). En attendant l'approbation, le repli en texte simple et le mail couvrent.
- [ ] **Step 3 (Saïbo) : la boîte d'envoi** — une adresse du domaine (ex. `dossiers@saibodanfakha.com` chez Hostinger) et son mot de passe, collés par lui dans le `.env` du VPS (secret par presse-papiers, jamais dans le chat) ; `MAIL_TO` = l'adresse où il veut recevoir.
- [ ] **Step 4: VPS** (`ssh -i <clé SSH du VPS> root@<VPS>`) — `nc -zv smtp.hostinger.com 587` → ouvert (Hetzner bloque 25 et 465) ; `mkdir -m 700 /root/agent-whatsapp/{dossiers,clients,jeux}` ; dans le bloc nginx d'`agent.saibodanfakha.com` : `proxy_set_header X-Real-IP $remote_addr;` si absent, `nginx -t && systemctl reload nginx`.
- [ ] **Step 5: Déployer l'agent** — sauvegarder `src/cloud.js` et `package.json` en `*.bak-<date>` ; `scp` de `src/{dossier,serveur-dossier,mail,cloud}.js`, `package.json`, `jeux/visibilite-securite.json`, les 2 fichiers de test ; `npm install` ; ajouter les variables au `.env` ; lancer les suites de tests sur le VPS → vertes ; `pm2 restart agent-whatsapp` ; `pm2 logs --lines 30` sans erreur ; un message de contact réel passe toujours (rien de cassé).
- [ ] **Step 6: Essai réel de l'endpoint** — `curl -X POST https://agent.saibodanfakha.com/dossier -H "Origin: https://saibodanfakha.com" -H "Content-Type: application/json" --data @dossier-fictif.json` → `{"ok":true}` ; fichier présent dans `dossiers/` (mode `-rw-------`) ; WhatsApp reçu par Saïbo ; mail reçu ; même requête sans `Origin` ⇒ 403. Puis supprimer le dossier fictif.
- [ ] **Step 7: Publier la page** — `git push origin feat/demarrer` ; aperçu Vercel vérifié par contenu ; fusion dans `main` (accord de Saïbo) ; en prod : `/demarrer/` répond, `noindex` présent, absente de `sitemap-0.xml`, un parcours complet sur le téléphone de Saïbo (artefact ou lien direct) aboutit à « Envoyé » et à ses deux notifications.
- [ ] **Step 8: Commiter la spec et le plan** (accord de Saïbo, dépôt public : relus pour vérifier qu'ils ne contiennent aucune donnée de client) — `git add docs/superpowers/specs/2026-11-21-questionnaire-demarrage-design.md docs/superpowers/plans/2026-11-22-questionnaire-demarrage.md`.

---

### Task 10: Le lien personnalisé du premier client

Rien de ce qui suit n'entre dans un dépôt.

- [ ] **Step 1:** Logo : rendre `<dossier du client>\logo\<logo vectoriel>.pdf` en PNG 512 px à fond transparent (sans retoucher le logo), puis l'encoder en data URL ≤ 120 000 caractères.
- [ ] **Step 2:** Jeton : `node -e "console.log(require('crypto').randomBytes(18).toString('base64url'))"` (24 caractères).
- [ ] **Step 3:** Écrire `CLIENTS_DIR/<jeton>.json` sur le VPS (mode `0600`) : `{ "prenom": "<prénom>", "societe": "<société>", "couleur": "<couleur du logo>", "accent": "<accent du logo>", "logo": "data:image/png;base64,…", "jeu": "visibilite-securite" }`.
- [ ] **Step 4:** Ouvrir `https://saibodanfakha.com/demarrer/#t=<jeton>` à 390 px : « Bonjour <prénom> », carte vert pétrole avec le logo, société préremplie, pas de question de couleur ni de logo. Saïbo fait le parcours une fois sur son téléphone (dossier d'essai supprimé ensuite).
- [ ] **Step 5:** Le lien va à Saïbo, qui l'envoie lui-même à son client (règle des 48 h : on lui demande d'abord quel jour il part). Inscrire l'envoi au tableau de score et dans `<dossier du client>\FICHE-RDV.md`.
