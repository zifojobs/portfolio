import assert from 'node:assert/strict'
import { describe, it } from 'node:test'

import { couperLignes } from './png.ts'

const mesurer = (s: string) => s.length * 10

describe('couperLignes', () => {
  it('coupe aux espaces, chaque ligne ≤ largeur', () => {
    const l = couperLignes('Sécurité privée, Télésurveillance, Sécurité incendie', 100, mesurer)
    assert.ok(l.length > 1)
    for (const x of l) assert.ok(mesurer(x) <= 100, x)
    assert.equal(l.join(' '), 'Sécurité privée, Télésurveillance, Sécurité incendie')
  })
  it('un mot plus long que la ligne est coupé en force', () => {
    const l = couperLignes('a'.repeat(30), 100, mesurer)
    assert.deepEqual(l, ['a'.repeat(10), 'a'.repeat(10), 'a'.repeat(10)])
  })
  it('chaîne vide → []', () => assert.deepEqual(couperLignes('', 100, mesurer), []))
})
