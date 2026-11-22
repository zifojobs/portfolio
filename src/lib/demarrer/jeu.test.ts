// node --test src/lib/demarrer/   (Node lit le TypeScript directement)
//
// Le jeu de questions du questionnaire de démarrage (22/11/2026).
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { describe, it } from 'node:test'

import type { Jeu } from './types.ts'
import { verifierJeu } from './jeu.ts'

const lire = (): Jeu =>
  JSON.parse(readFileSync(new URL('../../data/demarrer/visibilite-securite.json', import.meta.url), 'utf8'))

describe('Jeu « visibilité, sécurité privée »', () => {
  const jeu = lire()

  it('10 questions (3, 4 et 10 retirées par Saïbo le 22/11), ids uniques, budget en dernier', () => {
    assert.equal(jeu.questions.length, 10)
    assert.equal(jeu.questions.at(-1)!.id, 'budget')
    assert.deepEqual(verifierJeu(jeu), [])
  })

  it('chaque question a un pourquoi non vide', () => {
    for (const q of jeu.questions) assert.ok(q.pourquoi.trim(), q.id)
  })

  it('aucun prix dans les titres ni les pourquoi (hors budget)', () => {
    const texte = jeu.questions
      .filter((q) => q.id !== 'budget')
      .map((q) => `${q.titre} ${q.pourquoi}`)
      .join(' ')
    assert.ok(!/\d[\d   ]*\s?F\b/.test(texte))
  })
})

describe('verifierJeu', () => {
  it('signale un id de champ dupliqué', () => {
    const copie = lire()
    copie.questions[2].champs[0].id = 'societe'
    assert.match(verifierJeu(copie).join(' | '), /dupliqué/)
  })

  it('signale un budget qui n’est pas en dernier', () => {
    const inverse = lire()
    inverse.questions.reverse()
    assert.match(verifierJeu(inverse).join(' | '), /budget/)
  })

  it('signale un choix avec moins de 2 options… sauf une case « plus tard » facultative', () => {
    const copie = lire()
    const services = copie.questions.find((q) => q.id === 'services')!
    services.champs[0].options = [{ v: 'seul', l: 'Seul' }]
    assert.match(verifierJeu(copie).join(' | '), /services/)
  })
})
