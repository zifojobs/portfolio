// Brouillon gardé dans le navigateur pendant le parcours. Le stockage peut manquer ou lever
// (navigation privée, iOS) : le parcours continue alors sans brouillon, sans erreur.
import { estConfig } from './envoi.ts'
import type { ConfigClient, Reponses } from './types.ts'

export interface Brouillon {
  index: number
  reponses: Reponses
  idDossier: string
}

// La version du jeu est dans la clé : un brouillon d'avant une modification du jeu n'est jamais repris.
export const cleBrouillon = (jeuId: string, version: number, jeton: string | null) =>
  `demarrer:${jeuId}:v${version}:${jeton ?? 'libre'}`

const estBrouillon = (x: unknown): x is Brouillon => {
  if (!x || typeof x !== 'object') return false
  const b = x as Record<string, unknown>
  return (
    Number.isInteger(b.index) &&
    typeof b.idDossier === 'string' &&
    !!b.reponses &&
    typeof b.reponses === 'object' &&
    !Array.isArray(b.reponses)
  )
}

export function lireBrouillon(stockage: Pick<Storage, 'getItem'>, cle: string): Brouillon | null {
  try {
    const brut = stockage.getItem(cle)
    if (!brut) return null
    const b = JSON.parse(brut)
    return estBrouillon(b) ? b : null
  } catch {
    return null
  }
}

export function ecrireBrouillon(stockage: Pick<Storage, 'setItem'>, cle: string, b: Brouillon): void {
  try {
    stockage.setItem(cle, JSON.stringify(b))
  } catch {
    /* stockage indisponible : on continue sans brouillon */
  }
}

export function effacerBrouillon(stockage: Pick<Storage, 'removeItem'>, cle: string): void {
  try {
    stockage.removeItem(cle)
  } catch {
    /* idem */
  }
}

const cleConfig = (jeton: string) => `demarrer:config:${jeton}`

/** Dernière config valide d'un lien, pour un réseau instable. */
export function lireConfigCache(stockage: Pick<Storage, 'getItem'>, jeton: string): ConfigClient | null {
  try {
    const c = JSON.parse(stockage.getItem(cleConfig(jeton)) ?? 'null')
    return estConfig(c) ? c : null
  } catch {
    return null
  }
}

export function ecrireConfigCache(stockage: Pick<Storage, 'setItem'>, jeton: string, c: ConfigClient): void {
  try {
    stockage.setItem(cleConfig(jeton), JSON.stringify(c))
  } catch {
    /* stockage indisponible */
  }
}
