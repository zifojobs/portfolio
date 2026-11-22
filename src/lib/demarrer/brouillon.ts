// Brouillon gardé dans le navigateur pendant le parcours. Le stockage peut manquer ou lever
// (navigation privée, iOS) : le parcours continue alors sans brouillon, sans erreur.
import type { Reponses } from './types.ts'

export interface Brouillon {
  index: number
  reponses: Reponses
  idDossier: string
}

export const cleBrouillon = (jeuId: string, jeton: string | null) => `demarrer:${jeuId}:${jeton ?? 'libre'}`

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
