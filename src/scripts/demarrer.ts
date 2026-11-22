// Le parcours du questionnaire de démarrage, côté navigateur.
// Tout texte venant du client ou d'une config passe par textContent, jamais innerHTML.
import { cleBrouillon, effacerBrouillon, ecrireBrouillon, lireBrouillon } from '../lib/demarrer/brouillon.ts'
import { chargerConfig, envoyerDossier, JETON_VALIDE, type Dossier } from '../lib/demarrer/envoi.ts'
import { chargerJeu, JEUX } from '../lib/demarrer/jeu.ts'
import {
  carte,
  estRepondue,
  lignesDossier,
  progression,
  questionsVisibles,
  resumeTexte,
  texteSur,
  titreDossier,
} from '../lib/demarrer/moteur.ts'
import { dessinerDossier, partagerOuTelecharger, POLICE } from '../lib/demarrer/png.ts'
import type { Champ, ConfigClient, Jeu, Question, Reponses, Valeur } from '../lib/demarrer/types.ts'

const WHATSAPP = '221775277164'
const JEU_PAR_DEFAUT = 'visibilite-securite'
const LOGO_MAX = 256

const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T
const el = <K extends keyof HTMLElementTagNameMap>(tag: K, props: Partial<HTMLElementTagNameMap[K]> = {}, ...enfants: (Node | string)[]) => {
  const e = Object.assign(document.createElement(tag), props)
  e.append(...enfants)
  return e
}

let stockage: Storage | null = null
try {
  stockage = window.localStorage
} catch {
  stockage = null
}
const sto = {
  getItem: (k: string) => stockage?.getItem(k) ?? null,
  setItem: (k: string, v: string) => stockage?.setItem(k, v),
  removeItem: (k: string) => stockage?.removeItem(k),
}

const etat = {
  jeu: null as unknown as Jeu,
  config: null as ConfigClient | null,
  jeton: null as string | null,
  questions: [] as Question[],
  index: -1,
  reponses: {} as Reponses,
  idDossier: '',
  tagsAvant: [] as string[],
  envoiEnCours: false,
}

const cle = () => cleBrouillon(etat.jeu.id, etat.jeton)
const sauver = () => ecrireBrouillon(sto, cle(), { index: etat.index, reponses: etat.reponses, idDossier: etat.idDossier })

function nouvelId(): string {
  if (crypto.randomUUID) return crypto.randomUUID()
  const b = crypto.getRandomValues(new Uint8Array(16))
  b[6] = (b[6] & 0x0f) | 0x40
  b[8] = (b[8] & 0x3f) | 0x80
  const h = [...b].map((x) => x.toString(16).padStart(2, '0')).join('')
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`
}

function setValeur(cleR: string, v: Valeur | undefined) {
  const videV = v === undefined || (Array.isArray(v) ? v.length === 0 : v.trim() === '')
  if (videV) delete etat.reponses[cleR]
  else etat.reponses[cleR] = v
}

// ---------- Couleurs du client ----------
function couleurs(): { couleur: string; accent: string } {
  if (etat.config) return { couleur: etat.config.couleur, accent: etat.config.accent }
  const champ = etat.jeu.questions.flatMap((q) => q.champs).find((c) => c.type === 'couleur')
  const opt = champ?.options?.find((o) => o.v === etat.reponses[champ.id])
  return { couleur: opt?.v ?? '#1b1b1b', accent: opt?.accent ?? '#f39221' }
}

function appliquerCouleurs() {
  const { couleur, accent } = couleurs()
  const s = document.documentElement.style
  s.setProperty('--client', couleur)
  s.setProperty('--client-texte', texteSur(couleur))
  s.setProperty('--accent', accent)
  s.setProperty('--accent-texte', texteSur(accent))
}

const logoActuel = (): string | undefined =>
  etat.config?.logo ?? (typeof etat.reponses.logo === 'string' ? etat.reponses.logo : undefined)

// ---------- La carte ----------
function majCarte() {
  appliquerCouleurs()
  const c = carte(etat.jeu, etat.reponses, etat.tagsAvant)
  const boite = $('carte')
  boite.classList.toggle('vide', !c.nom && c.tags.length === 0)
  $('carte-nom').textContent = c.nom
  const tags = $('carte-tags')
  tags.replaceChildren(...c.tags.map((t) => el('span', { textContent: t, className: t === c.dernier ? 'nouveau' : '' })))
  const logo = $<HTMLImageElement>('carte-logo')
  const src = logoActuel()
  logo.hidden = !src
  if (src) logo.src = src
  etat.tagsAvant = c.tags
}

// ---------- Les champs ----------
function champTexte(c: Champ, maj: () => void) {
  const id = `c-${c.id}`
  const input = el('input', {
    id,
    type: c.id === 'numero_valeur' ? 'tel' : 'text',
    className: 'dm-texte',
    maxLength: c.max ?? 300,
    value: typeof etat.reponses[c.id] === 'string' ? (etat.reponses[c.id] as string) : '',
    autocomplete: c.id === 'prenom' ? 'given-name' : c.id === 'nom' ? 'family-name' : 'off',
  })
  input.addEventListener('input', () => {
    setValeur(c.id, input.value)
    maj()
  })
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      ;($('suivant') as HTMLButtonElement | null)?.click()
    }
  })
  const bloc = el('div', { className: 'dm-champ' })
  if (c.libelle) bloc.append(el('label', { className: 'dm-lbl', htmlFor: id, textContent: c.libelle }))
  else input.setAttribute('aria-labelledby', 'titre-question')
  bloc.append(input)
  return bloc
}

function champOptions(c: Champ, maj: () => void) {
  const multiple = c.type === 'puces'
  const fs = el('fieldset', { className: 'dm-champ' })
  if (c.libelle) fs.append(el('legend', { textContent: c.libelle }))
  else fs.setAttribute('aria-labelledby', 'titre-question')
  const zone = el('div', { className: 'dm-puces' })
  const options = [...(c.options ?? []), ...(c.autre ? [{ v: 'autre', l: 'Autre' }] : [])]
  const choisis = (): string[] => {
    const v = etat.reponses[c.id]
    return Array.isArray(v) ? v : typeof v === 'string' ? [v] : []
  }
  const autreInput = el('input', {
    type: 'text',
    className: 'dm-texte',
    maxLength: 100,
    placeholder: 'Précisez',
    value: typeof etat.reponses[`${c.id}.autre`] === 'string' ? (etat.reponses[`${c.id}.autre`] as string) : '',
  })
  autreInput.setAttribute('aria-label', `${c.libelle ?? 'Autre'} : précisez`)
  autreInput.style.marginTop = '10px'
  autreInput.addEventListener('input', () => {
    setValeur(`${c.id}.autre`, autreInput.value)
    maj()
  })
  const majAutre = () => {
    autreInput.hidden = !choisis().includes('autre')
  }
  const boutons = options.map((o) => {
    const b = el('button', { type: 'button', className: 'dm-puce', textContent: o.l })
    b.setAttribute('aria-pressed', String(choisis().includes(o.v)))
    b.addEventListener('click', () => {
      const avant = choisis()
      let apres: string[]
      if (multiple) apres = avant.includes(o.v) ? avant.filter((x) => x !== o.v) : [...avant, o.v]
      // Un choix facultatif se décoche ; un choix obligatoire reste choisi.
      else apres = avant.includes(o.v) && c.facultatif ? [] : [o.v]
      setValeur(c.id, multiple ? apres : apres[0])
      if (!apres.includes('autre')) {
        delete etat.reponses[`${c.id}.autre`]
        autreInput.value = ''
      }
      for (const [i, bb] of boutons.entries()) bb.setAttribute('aria-pressed', String(apres.includes(options[i].v)))
      majAutre()
      maj()
      if (o.v === 'autre' && apres.includes('autre')) autreInput.focus()
    })
    return b
  })
  zone.append(...boutons)
  fs.append(zone)
  if (c.autre) {
    majAutre()
    fs.append(autreInput)
  }
  return fs
}

function champCouleur(c: Champ, maj: () => void) {
  const fs = el('fieldset', { className: 'dm-champ' }, el('legend', { textContent: c.libelle ?? 'Couleur' }))
  const zone = el('div', { className: 'dm-puces' })
  const boutons = (c.options ?? []).map((o) => {
    const b = el('button', { type: 'button', className: 'dm-pastille' })
    b.style.background = o.v
    b.setAttribute('aria-label', o.l)
    b.title = o.l
    b.setAttribute('aria-pressed', String(etat.reponses[c.id] === o.v))
    b.addEventListener('click', () => {
      setValeur(c.id, o.v)
      for (const bb of boutons) bb.setAttribute('aria-pressed', String(bb === b))
      maj()
    })
    return b
  })
  zone.append(...boutons)
  fs.append(zone)
  return fs
}

async function reduireLogo(fichier: File): Promise<string> {
  const url = URL.createObjectURL(fichier)
  try {
    const img = new Image()
    img.src = url
    await img.decode()
    const r = Math.min(1, LOGO_MAX / Math.max(img.naturalWidth, img.naturalHeight))
    const toile = el('canvas', { width: Math.round(img.naturalWidth * r), height: Math.round(img.naturalHeight * r) })
    toile.getContext('2d')!.drawImage(img, 0, 0, toile.width, toile.height)
    return toile.toDataURL('image/png')
  } finally {
    URL.revokeObjectURL(url)
  }
}

function champLogo(c: Champ, maj: () => void) {
  const id = `c-${c.id}`
  const bloc = el('div', { className: 'dm-champ' }, el('label', { className: 'dm-lbl', htmlFor: id, textContent: c.libelle ?? 'Logo' }))
  const input = el('input', { id, type: 'file', accept: 'image/png,image/jpeg' })
  const apercu = el('div', { className: 'dm-logo-apercu' })
  const erreur = el('p', { className: 'dm-erreur', hidden: true })
  const montrer = () => {
    const v = etat.reponses[c.id]
    if (typeof v !== 'string') return apercu.replaceChildren()
    const retirer = el('button', { type: 'button', className: 'dm-lien', textContent: 'Retirer' })
    retirer.addEventListener('click', () => {
      delete etat.reponses[c.id]
      input.value = ''
      montrer()
      maj()
    })
    apercu.replaceChildren(el('img', { src: v, alt: 'Votre logo' }), retirer)
  }
  input.addEventListener('change', async () => {
    erreur.hidden = true
    const f = input.files?.[0]
    if (!f) return
    if (!['image/png', 'image/jpeg'].includes(f.type)) {
      erreur.textContent = 'Choisissez une image PNG ou JPEG.'
      erreur.hidden = false
      return
    }
    try {
      const data = await reduireLogo(f)
      if (data.length > 120000) throw new Error('trop lourd')
      setValeur(c.id, data)
    } catch {
      erreur.textContent = "Ce fichier n'a pas pu être lu. Essayez une autre image, ou passez : on s'en occupera ensemble."
      erreur.hidden = false
    }
    montrer()
    maj()
  })
  montrer()
  bloc.append(input, apercu, erreur)
  return bloc
}

function rendreChamp(c: Champ, maj: () => void) {
  if (c.type === 'texte') return champTexte(c, maj)
  if (c.type === 'couleur') return champCouleur(c, maj)
  if (c.type === 'logo') return champLogo(c, maj)
  return champOptions(c, maj)
}

// ---------- Les écrans ----------
function enTete(n: number | null) {
  const total = etat.questions.length
  $('sous').textContent = n === null ? 'Développeur web' : `question ${n} sur ${total}`
  $('barre').hidden = n === null
  $('barre-i').style.width = `${progression(n === null ? 0 : n - 1, total)}%`
}

function focusTitre() {
  const h = document.getElementById('titre-question')
  h?.focus({ preventScroll: false })
  window.scrollTo({ top: 0 })
}

function ecranAccueil() {
  etat.index = -1
  enTete(null)
  const prenom = etat.config?.prenom
  const brouillon = lireBrouillon(sto, cle())
  const n = etat.questions.length
  const zone = $('ecran')
  const h = el('h1', { id: 'titre-question', tabIndex: -1, textContent: prenom ? `Bonjour ${prenom},` : 'Bonjour,' })
  const intro = el('p', {
    className: 'dm-intro',
    textContent: `Je vais vous poser ${n} questions, environ 8 minutes. Vos réponses me permettent de vous préparer une proposition juste.`,
  })
  const actions = el('div', { className: 'dm-apres' })
  if (brouillon && brouillon.index >= 0) {
    const reprendre = el('button', { type: 'button', className: 'dm-btn large', textContent: 'Reprendre là où vous en étiez' })
    reprendre.addEventListener('click', () => {
      etat.reponses = brouillon.reponses
      etat.idDossier = brouillon.idDossier
      ecranQuestion(Math.min(brouillon.index, n - 1))
    })
    const recommencer = el('button', { type: 'button', className: 'dm-lien', textContent: 'Recommencer depuis le début' })
    recommencer.addEventListener('click', () => {
      effacerBrouillon(sto, cle())
      demarrerVierge()
      ecranQuestion(0)
    })
    actions.append(reprendre, recommencer)
  } else {
    const commencer = el('button', { type: 'button', className: 'dm-btn large', textContent: 'Commencer' })
    commencer.addEventListener('click', () => ecranQuestion(0))
    actions.append(commencer)
  }
  zone.replaceChildren(h, intro, actions)
  majCarte()
  focusTitre()
}

function ecranQuestion(i: number) {
  etat.index = i
  const q = etat.questions[i]
  const dernier = i === etat.questions.length - 1
  enTete(i + 1)
  const suivant = el('button', {
    type: 'button',
    id: 'suivant',
    className: 'dm-btn',
    textContent: dernier ? 'Envoyer mon dossier' : 'Continuer',
  })
  const maj = () => {
    suivant.disabled = etat.envoiEnCours || !estRepondue(q, etat.reponses)
    sauver()
    majCarte()
  }
  const champs = q.champs.map((c) => rendreChamp(c, maj))
  const retour = el('button', { type: 'button', className: 'dm-lien', textContent: 'Retour' })
  retour.addEventListener('click', () => (i === 0 ? ecranAccueil() : ecranQuestion(i - 1)))
  const erreur = el('div', { id: 'erreur-envoi', hidden: true })
  suivant.addEventListener('click', () => {
    if (suivant.disabled) return
    if (dernier) void envoyer(suivant, erreur)
    else ecranQuestion(i + 1)
  })
  $('ecran').replaceChildren(
    el('h1', { id: 'titre-question', tabIndex: -1, textContent: q.titre }),
    el('p', { className: 'dm-pourquoi' }, el('b', { textContent: 'Pourquoi je vous le demande : ' }), q.pourquoi),
    ...champs,
    el('div', { className: 'dm-actions' }, suivant, retour),
    erreur,
  )
  maj()
  focusTitre()
}

function lienWhatsApp(): string {
  return `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(resumeTexte(etat.jeu, etat.reponses))}`
}

async function envoyer(bouton: HTMLButtonElement, zoneErreur: HTMLElement) {
  if (etat.envoiEnCours) return
  etat.envoiEnCours = true
  bouton.disabled = true
  bouton.textContent = 'Envoi en cours…'
  zoneErreur.hidden = true
  const dossier: Dossier = {
    version: 1,
    idDossier: etat.idDossier,
    jeu: etat.jeu.id,
    jeton: etat.jeton,
    envoyeLe: new Date().toISOString(),
    reponses: etat.reponses,
  }
  const r = await envoyerDossier(dossier)
  etat.envoiEnCours = false
  if (r.ok) {
    effacerBrouillon(sto, cle())
    const montrer = () => ecranDossier()
    if (document.startViewTransition && !matchMedia('(prefers-reduced-motion: reduce)').matches)
      document.startViewTransition(montrer)
    else montrer()
    return
  }
  bouton.disabled = false
  bouton.textContent = 'Réessayer'
  const wa = el('a', { className: 'dm-lien', href: lienWhatsApp(), target: '_blank', rel: 'noopener noreferrer', textContent: 'Envoyer sur WhatsApp à la place' })
  zoneErreur.replaceChildren(el('p', { className: 'dm-erreur', textContent: r.message }), wa)
  zoneErreur.hidden = false
}

function dateCourte(): string {
  return new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

function ecranDossier() {
  enTete(null)
  $('ecran').replaceChildren()
  $('ecran').hidden = true
  $('carte').hidden = true
  const d = $('dossier')
  const lignes = lignesDossier(etat.jeu, etat.reponses)
  const dl = el('dl')
  for (const l of lignes) dl.append(el('dt', { textContent: l.libelle }), el('dd', { textContent: l.valeur }))
  const chemin = el('div', { className: 'dm-chemin' }, ...etat.jeu.chemin.map(() => el('i')))
  const logo = logoActuel()
  d.replaceChildren(
    ...(logo ? [el('img', { src: logo, alt: '', className: 'dm-carte-logo' })] : []),
    el('span', { className: 'k', textContent: `Dossier de démarrage · ${dateCourte()}` }),
    el('h1', { id: 'titre-question', tabIndex: -1, textContent: titreDossier(etat.jeu, etat.reponses) }),
    el('div', { className: 'boite' }, el('b', { textContent: "Ce que vous m'avez dit" }), dl),
    el('div', { className: 'boite' }, el('b', { textContent: 'Le chemin' }), chemin, etat.jeu.chemin.join(' → ')),
    el('p', { className: 'dm-promesse', textContent: 'Je reviens vers vous sous 48 h avec la proposition chiffrée.' }),
  )
  d.hidden = false

  const enregistrer = el('button', { type: 'button', className: 'dm-btn large', textContent: 'Enregistrer mon dossier' })
  enregistrer.addEventListener('click', async () => {
    enregistrer.disabled = true
    try {
      await document.fonts.load(`800 40px ${POLICE}`)
      await document.fonts.load(`400 20px ${POLICE}`)
      const { couleur, accent } = couleurs()
      let img: HTMLImageElement | undefined
      if (logo) {
        img = new Image()
        img.src = logo
        await img.decode()
      }
      const toile = $<HTMLCanvasElement>('toile')
      dessinerDossier(toile.getContext('2d')!, {
        date: dateCourte(),
        titre: titreDossier(etat.jeu, etat.reponses),
        lignes,
        chemin: etat.jeu.chemin,
        couleur,
        accent,
        logo: img,
      })
      await partagerOuTelecharger(toile)
    } finally {
      enregistrer.disabled = false
    }
  })
  const wa = el('a', {
    className: 'dm-btn large secondaire',
    href: lienWhatsApp(),
    target: '_blank',
    rel: 'noopener noreferrer',
    textContent: 'Envoyer aussi à Saïbo sur WhatsApp',
  })
  const merci = el('p', { className: 'dm-merci', textContent: 'Votre dossier m’est bien parvenu. Merci pour votre temps.' })
  d.after(el('div', { className: 'dm-apres' }, enregistrer, wa, merci))
  focusTitre()
}

function demarrerVierge() {
  etat.reponses = {}
  etat.idDossier = nouvelId()
  etat.tagsAvant = []
  if (etat.config) {
    etat.reponses.prenom = etat.config.prenom
    etat.reponses.societe = etat.config.societe
  }
}

async function init() {
  const jeton = new URLSearchParams(location.hash.slice(1)).get('t')
  etat.jeton = jeton && JETON_VALIDE.test(jeton) ? jeton : null
  etat.config = etat.jeton ? await chargerConfig(etat.jeton) : null
  // Lien inconnu ou expiré : le parcours s'ouvre en mode libre, sans message d'erreur.
  if (!etat.config) etat.jeton = null
  etat.jeu = chargerJeu(etat.config && JEUX[etat.config.jeu] ? etat.config.jeu : JEU_PAR_DEFAUT)
  etat.questions = questionsVisibles(etat.jeu, !!etat.config)
  demarrerVierge()
  ecranAccueil()
}

void init()
