import type { Jeu } from './types.ts'
import visibiliteSecurite from '../../data/demarrer/visibilite-securite.json' with { type: 'json' }

export const JEUX: Record<string, Jeu> = {
  [visibiliteSecurite.id]: visibiliteSecurite as Jeu,
}

export function chargerJeu(id: string): Jeu {
  const jeu = JEUX[id]
  if (!jeu) throw new Error(`Jeu de questions inconnu : ${id}`)
  return jeu
}

/** Liste les défauts d'un jeu ; vide s'il est correct. */
export function verifierJeu(jeu: Jeu): string[] {
  const erreurs: string[] = []
  const idsQuestions = new Set<string>()
  const idsChamps = new Set<string>()

  for (const q of jeu.questions) {
    if (idsQuestions.has(q.id)) erreurs.push(`question ${q.id} : id dupliqué`)
    idsQuestions.add(q.id)
    if (!q.pourquoi?.trim()) erreurs.push(`question ${q.id} : pourquoi vide`)
    for (const c of q.champs) {
      if (idsChamps.has(c.id)) erreurs.push(`question ${q.id} : champ ${c.id} dupliqué`)
      idsChamps.add(c.id)
      const aOptions = c.type === 'choix' || c.type === 'puces' || c.type === 'couleur'
      // Une case unique (« Je les envoie plus tard ») n'a de sens que facultative.
      const minimum = c.facultatif ? 1 : 2
      if (aOptions && (c.options?.length ?? 0) < minimum)
        erreurs.push(`question ${q.id} : champ ${c.id} a moins de ${minimum} options`)
    }
  }
  if (jeu.questions.at(-1)?.id !== 'budget') erreurs.push('la question budget doit être la dernière')
  return erreurs
}
