// node --test src/lib/estimateur.test.ts   (Node lit le TypeScript directement)
//
// L'estimateur (16/11/2026) : les fourchettes sont celles du formulaire de contact,
// calées sur des devis réels.
import assert from 'node:assert/strict'
import { describe, it } from 'node:test'

import { estimer, FOURCHETTES, messageWhatsApp, type Reponses } from './estimateur.ts'

const base: Reponses = { type: 'vitrine', pages: '4-5', fonctions: [], contenus: 'prets', delai: 'normal' }

describe('Fourchette', () => {
  it('une vitrine de 4-5 pages tombe entre 175 000 et 350 000 F', () => {
    assert.equal(estimer(base).fourchette, FOURCHETTES[1])
  })
  it('une petite vitrine de 1 à 3 pages, textes prêts, reste sous 175 000 F', () => {
    assert.equal(estimer({ ...base, pages: '1-3' }).fourchette, FOURCHETTES[0])
  })
  it('un site complet ou un blog : 350 000 à 800 000 F', () => {
    assert.equal(estimer({ ...base, type: 'complet', pages: '6-10' }).fourchette, FOURCHETTES[2])
  })
  it('une boutique : 800 000 à 1 600 000 F', () => {
    assert.equal(estimer({ ...base, type: 'boutique', pages: '6-10' }).fourchette, FOURCHETTES[3])
  })
  it('une application sur mesure : plus de 1 600 000 F', () => {
    assert.equal(estimer({ ...base, type: 'application' }).fourchette, FOURCHETTES[4])
  })
  it('le paiement en ligne ou un espace membres monte d’un cran', () => {
    assert.equal(estimer({ ...base, fonctions: ['paiement'] }).fourchette, FOURCHETTES[2])
    assert.equal(estimer({ ...base, fonctions: ['membres', 'paiement'] }).fourchette, FOURCHETTES[2])
  })
  it('plus de pages que le type n’en prévoit monte d’un cran', () => {
    assert.equal(estimer({ ...base, pages: '6-10' }).fourchette, FOURCHETTES[2])
  })
  it('les textes à créer ne font pas monter le cran mais se signalent', () => {
    const r = estimer({ ...base, contenus: 'a-creer' })
    assert.equal(r.fourchette, FOURCHETTES[1])
    assert.ok(r.notes.some((n) => n.includes('rédaction')))
  })
  it('ne dépasse jamais le dernier cran', () => {
    assert.equal(estimer({ ...base, type: 'application', pages: '11+', fonctions: ['paiement', 'membres', 'langues'] }).fourchette, FOURCHETTES[4])
  })
})

describe('Message WhatsApp', () => {
  it('reprend les réponses et la fourchette, sans rien d’autre', () => {
    const m = messageWhatsApp({ ...base, fonctions: ['reservation'] })
    assert.match(m, /Site vitrine/)
    assert.match(m, /4 à 5 pages/)
    assert.match(m, /réservation/i)
    assert.match(m, /175 000 – 350 000 F/)
  })
})
