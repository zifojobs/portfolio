// Envoi du dossier à l'agent de Saïbo (VPS) et lecture d'un lien personnalisé.
// « Envoyé » ne s'affiche qu'après un 200 : 200 = copie écrite sur le disque de l'agent.
import type { ConfigClient, Reponses } from './types.ts'

export const URL_AGENT = 'https://agent.saibodanfakha.com'

export interface Dossier {
  version: 1
  idDossier: string
  jeu: string
  jeton: string | null
  envoyeLe: string
  reponses: Reponses
}

export type ResultatEnvoi = { ok: true } | { ok: false; message: string }

const MESSAGES = {
  reseau: 'La connexion a échoué. Vos réponses sont gardées : réessayez dans un instant.',
  trop: "Trop d'envois d'un coup. Réessayez dans une heure, vos réponses sont gardées.",
  autre: "L'envoi n'a pas abouti. Vos réponses sont gardées : réessayez, ou envoyez-les-moi sur WhatsApp.",
}

/** Délai d'abandon d'une requête ; Safari < 16 (iOS 15) n'a pas AbortSignal.timeout. */
export function delai(ms: number): AbortSignal {
  if (typeof AbortSignal.timeout === 'function') return AbortSignal.timeout(ms)
  const c = new AbortController()
  setTimeout(() => c.abort(), ms)
  return c.signal
}

export async function envoyerDossier(d: Dossier, f: typeof fetch = fetch): Promise<ResultatEnvoi> {
  let res: Response
  try {
    res = await f(`${URL_AGENT}/dossier`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(d),
      signal: delai(20000),
    })
  } catch {
    return { ok: false, message: MESSAGES.reseau }
  }
  if (res.status === 200) return { ok: true }
  return { ok: false, message: res.status === 429 ? MESSAGES.trop : MESSAGES.autre }
}

export const JETON_VALIDE = /^[A-Za-z0-9_-]{16,64}$/
const HEX = /^#[0-9a-fA-F]{6}$/

export const estConfig = (x: unknown): x is ConfigClient => {
  if (!x || typeof x !== 'object') return false
  const c = x as Record<string, unknown>
  return (
    typeof c.prenom === 'string' &&
    typeof c.societe === 'string' &&
    typeof c.couleur === 'string' && HEX.test(c.couleur) &&
    typeof c.accent === 'string' && HEX.test(c.accent) &&
    typeof c.jeu === 'string' &&
    (c.logo === undefined || (typeof c.logo === 'string' && /^data:image\/(png|jpeg);base64,/.test(c.logo)))
  )
}

export type ResultatConfig = { statut: 'ok'; config: ConfigClient } | { statut: 'absent' } | { statut: 'erreur' }

/** La config d'un lien personnalisé. « absent » (lien inconnu) ⇒ mode libre ;
 *  « erreur » (réseau, 429…) ⇒ le lien reste valable, la page reprend la config gardée. */
export async function chargerConfig(jeton: string, f: typeof fetch = fetch): Promise<ResultatConfig> {
  if (!JETON_VALIDE.test(jeton)) return { statut: 'absent' }
  try {
    const res = await f(`${URL_AGENT}/config/${jeton}`, { signal: delai(10000) })
    if (res.status === 404) return { statut: 'absent' }
    if (res.status !== 200) return { statut: 'erreur' }
    const c = await res.json()
    return estConfig(c) ? { statut: 'ok', config: c } : { statut: 'absent' }
  } catch {
    return { statut: 'erreur' }
  }
}
