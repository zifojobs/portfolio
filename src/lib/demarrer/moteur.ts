// Le moteur du questionnaire de démarrage : fonctions pures, sans DOM.
import type { Champ, Jeu, Question, Reponses } from './types.ts'

const vide = (v: unknown) => (Array.isArray(v) ? v.length === 0 : typeof v !== 'string' || v.trim() === '')

function champRempli(c: Champ, r: Reponses): boolean {
  const v = r[c.id]
  if (vide(v)) return false
  const choisis = Array.isArray(v) ? v : [v as string]
  if (c.autre && choisis.includes('autre')) return !vide(r[`${c.id}.autre`])
  return true
}

/** Les 13 questions ; avec un lien personnalisé, les champs « sansLien » (couleur, logo) disparaissent. */
export function questionsVisibles(jeu: Jeu, avecLien: boolean): Question[] {
  if (!avecLien) return jeu.questions
  return jeu.questions.map((q) => ({ ...q, champs: q.champs.filter((c) => !c.sansLien) }))
}

export function estRepondue(q: Question, r: Reponses): boolean {
  if (q.auMoinsUn) return q.champs.some((c) => champRempli(c, r))
  return q.champs.every((c) => c.facultatif || champRempli(c, r))
}

const libelleOption = (c: Champ, v: string) => c.options?.find((o) => o.v === v)?.l ?? v

/** Les valeurs lisibles d'un champ : libellés des options, texte « autre » à la place de « autre ». */
function valeursLisibles(c: Champ, r: Reponses): string[] {
  const v = r[c.id]
  if (vide(v)) return []
  if (c.type === 'texte') return [(v as string).trim()]
  if (c.type === 'logo') return []
  const choisis = Array.isArray(v) ? v : [v as string]
  // Ordre du jeu, pas ordre des clics.
  const ordonnes = (c.options ?? []).filter((o) => choisis.includes(o.v)).map((o) => o.l)
  const inconnus = choisis.filter((x) => x !== 'autre' && !c.options?.some((o) => o.v === x)).map((x) => libelleOption(c, x))
  const autre = c.autre && choisis.includes('autre') && !vide(r[`${c.id}.autre`]) ? [(r[`${c.id}.autre`] as string).trim()] : []
  return [...ordonnes, ...inconnus, ...autre]
}

const tousLesChamps = (jeu: Jeu) => jeu.questions.flatMap((q) => q.champs)

export function carte(jeu: Jeu, r: Reponses, avant?: string[]): { nom: string; tags: string[]; dernier: string | null } {
  const champs = tousLesChamps(jeu)
  const champNom = champs.find((c) => c.carte === 'nom')
  const nom = champNom ? (valeursLisibles(champNom, r)[0] ?? '').toLocaleUpperCase('fr') : ''
  const tags = champs.filter((c) => c.carte === 'tags').flatMap((c) => valeursLisibles(c, r))
  const dernier = avant ? (tags.filter((t) => !avant.includes(t)).at(-1) ?? null) : null
  return { nom, tags, dernier }
}

export function lignesDossier(jeu: Jeu, r: Reponses): { libelle: string; valeur: string }[] {
  return tousLesChamps(jeu)
    .filter((c) => c.dossier)
    .map((c) => ({ libelle: c.dossier!, valeur: valeursLisibles(c, r).join(', ') }))
    .filter((l) => l.valeur)
}

export function titreDossier(jeu: Jeu, r: Reponses): string {
  const societe = typeof r.societe === 'string' ? r.societe.trim() : ''
  return jeu.titreDossier.replace('{societe}', societe || 'Votre société')
}

const MAX_RESUME = 1500

/** Le résumé multi-lignes du message WhatsApp que le client peut envoyer lui-même. */
export function resumeTexte(jeu: Jeu, r: Reponses): string {
  const lignes = jeu.questions
    .map((q) => {
      const valeurs = q.champs.flatMap((c) => valeursLisibles(c, r))
      return valeurs.length ? `${q.titre} ${valeurs.join(' · ')}` : ''
    })
    .filter(Boolean)
  const texte = ['Bonjour Saïbo, voici mon dossier de démarrage.', '', ...lignes].join('\n')
  if (texte.length <= MAX_RESUME) return texte
  // Par caractères entiers : un émoji coupé en deux ferait lever encodeURIComponent (lien WhatsApp).
  const car = Array.from(texte)
  let coupe = ''
  for (const c of car) {
    if (coupe.length + c.length > MAX_RESUME - 1) break
    coupe += c
  }
  return coupe + '…'
}

function luminance(hex: string): number {
  const n = parseInt(hex.replace('#', ''), 16)
  const canal = (x: number) => {
    const s = x / 255
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4
  }
  return 0.2126 * canal((n >> 16) & 255) + 0.7152 * canal((n >> 8) & 255) + 0.0722 * canal(n & 255)
}

const contraste = (a: number, b: number) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)

/** La couleur de texte la plus lisible sur un fond donné. */
export function texteSur(hex: string): '#ffffff' | '#1b1b1b' {
  const l = luminance(hex)
  return contraste(l, 1) >= contraste(l, luminance('#1b1b1b')) ? '#ffffff' : '#1b1b1b'
}

export function progression(index: number, total: number): number {
  if (total <= 0) return 0
  return Math.round((Math.min(Math.max(index, 0), total) / total) * 100)
}

/** Typographie française : espace fine insécable avant ? ! : ; (un « ? » ne passe jamais seul à la ligne). */
export const typo = (s: string): string => s.replace(/ ([?!:;])/g, '\u202f$1')
