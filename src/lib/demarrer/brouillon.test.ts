import assert from 'node:assert/strict'
import { describe, it } from 'node:test'

import { cleBrouillon, effacerBrouillon, ecrireBrouillon, lireBrouillon, type Brouillon } from './brouillon.ts'

const fauxStockage = () => {
  const m = new Map<string, string>()
  return {
    getItem: (k: string) => m.get(k) ?? null,
    setItem: (k: string, v: string) => void m.set(k, v),
    removeItem: (k: string) => void m.delete(k),
  }
}
const quiLeve = {
  getItem: () => { throw new Error('SecurityError') },
  setItem: () => { throw new Error('QuotaExceededError') },
  removeItem: () => { throw new Error('SecurityError') },
}
const b: Brouillon = { index: 5, reponses: { societe: 'Exemple Sécurité', zones: ['dakar'] }, idDossier: '6f1c2b0e-8d1a-4c4e-9b8a-2f3d4e5f6a7b' }

describe('brouillon', () => {
  it('clé : jeton ou « libre »', () => {
    assert.equal(cleBrouillon('visibilite-securite', null), 'demarrer:visibilite-securite:libre')
    assert.equal(cleBrouillon('visibilite-securite', 'abc'), 'demarrer:visibilite-securite:abc')
  })
  it('reprise : écrit puis relit le même brouillon', () => {
    const s = fauxStockage()
    ecrireBrouillon(s, 'k', b)
    assert.deepEqual(lireBrouillon(s, 'k'), b)
  })
  it('effacer puis relire → null', () => {
    const s = fauxStockage()
    ecrireBrouillon(s, 'k', b)
    effacerBrouillon(s, 'k')
    assert.equal(lireBrouillon(s, 'k'), null)
  })
  it('stockage qui lève : lire → null, écrire/effacer ne lèvent pas', () => {
    assert.equal(lireBrouillon(quiLeve, 'k'), null)
    assert.doesNotThrow(() => ecrireBrouillon(quiLeve, 'k', b))
    assert.doesNotThrow(() => effacerBrouillon(quiLeve, 'k'))
  })
  it('JSON abîmé → null', () => {
    const s = fauxStockage()
    s.setItem('k', '{pas du json')
    assert.equal(lireBrouillon(s, 'k'), null)
  })
  it('forme inattendue → null', () => {
    const s = fauxStockage()
    s.setItem('k', JSON.stringify({ index: 'trois', reponses: [] }))
    assert.equal(lireBrouillon(s, 'k'), null)
  })
})
