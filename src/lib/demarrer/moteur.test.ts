// Le moteur du questionnaire de démarrage : fonctions pures, valeurs fictives seulement.
import assert from 'node:assert/strict'
import { describe, it } from 'node:test'

import { chargerJeu } from './jeu.ts'
import {
  carte,
  estRepondue,
  lignesDossier,
  progression,
  questionsVisibles,
  resumeTexte,
  texteSur,
  titreDossier,
  typo,
} from './moteur.ts'

const jeu = chargerJeu('visibilite-securite')
const q = (id: string) => jeu.questions.find((x) => x.id === id)!

describe('estRepondue', () => {
  it('texte vide = non', () => assert.equal(estRepondue(q('societe'), { societe: '  ', couleur: '#045b5b' }), false))
  it('texte rempli + couleur = oui', () =>
    assert.equal(estRepondue(q('societe'), { societe: 'Exemple Sécurité', couleur: '#045b5b' }), true))
  it('option autre sans texte = non', () => assert.equal(estRepondue(q('services'), { services: ['autre'] }), false))
  it('option autre avec texte = oui', () =>
    assert.equal(estRepondue(q('services'), { services: ['autre'], 'services.autre': 'Escorte' }), true))
  const auMoinsUn = {
    id: 'legal', titre: 'T', pourquoi: 'P', auMoinsUn: true,
    champs: [
      { id: 'ninea', type: 'texte' as const, facultatif: true },
      { id: 'plus_tard', type: 'choix' as const, facultatif: true, options: [{ v: 'plus-tard', l: 'Plus tard' }] },
    ],
  }
  it('auMoinsUn avec plus-tard = oui', () => assert.equal(estRepondue(auMoinsUn, { plus_tard: 'plus-tard' }), true))
  it('auMoinsUn sans rien = non', () => assert.equal(estRepondue(auMoinsUn, {}), false))
  it('photos : « Sinon » et « Qui » sont facultatifs', () => assert.equal(estRepondue(q('photos'), { photos: ['aucune'] }), true))
  it('les deux choix du budget sont exigés', () =>
    assert.equal(estRepondue(q('budget'), { budget_depart: 'en-parler' }), false))
  it('avec lien, couleur absente ne bloque pas', () => {
    const societe = questionsVisibles(jeu, true)[1]
    assert.equal(estRepondue(societe, { societe: 'Exemple Sécurité' }), true)
  })
})

describe('questionsVisibles', () => {
  it('avec lien retire couleur et logo, garde 10 questions', () => {
    const v = questionsVisibles(jeu, true)
    assert.equal(v.length, 10)
    assert.ok(!v[1].champs.some((c) => c.id === 'couleur' || c.id === 'logo'))
  })
  it('sans lien les garde', () => assert.ok(questionsVisibles(jeu, false)[1].champs.some((c) => c.id === 'couleur')))
})

describe('carte', () => {
  it('nom en capitales, tags dans l’ordre du jeu, dernier ajouté', () => {
    const c = carte(
      jeu,
      { societe: 'Exemple Sécurité', services: ['incendie', 'securite-privee'], zones: ['dakar'] },
      ['Sécurité privée', 'Dakar'],
    )
    assert.equal(c.nom, 'EXEMPLE SÉCURITÉ')
    assert.deepEqual(c.tags, ['Sécurité privée', 'Sécurité incendie', 'Dakar'])
    assert.equal(c.dernier, 'Sécurité incendie')
  })
  it('texte « autre » devient un tag', () => {
    const c = carte(jeu, { services: ['autre'], 'services.autre': 'Escorte' })
    assert.deepEqual(c.tags, ['Escorte'])
  })
  it('carte vide', () => assert.deepEqual(carte(jeu, {}), { nom: '', tags: [], dernier: null }))
})

describe('dossier', () => {
  it('lignesDossier : libellés, valeurs jointes, champs vides omis', () => {
    const l = lignesDossier(jeu, { services: ['securite-privee', 'incendie'], zones: ['dakar'] })
    assert.deepEqual(l, [
      { libelle: 'Services', valeur: 'Sécurité privée, Sécurité incendie' },
      { libelle: 'Zones', valeur: 'Dakar' },
    ])
  })
  it('titreDossier', () =>
    assert.equal(titreDossier(jeu, { societe: 'Exemple Sécurité' }), 'Exemple Sécurité, prête à être trouvée.'))
  it('resumeTexte reprend les réponses', () => {
    const r = resumeTexte(jeu, { prenom: 'Awa', societe: 'Exemple Sécurité', zones: ['dakar'] })
    assert.match(r, /Exemple Sécurité/)
    assert.match(r, /Dakar/)
  })
  it('resumeTexte ne coupe jamais un émoji en deux (lien WhatsApp valide)', () => {
    for (let n = 1480; n < 1500; n++) {
      const r = resumeTexte(jeu, { societe: 'x'.repeat(n - 80) + '😀'.repeat(200) })
      assert.doesNotThrow(() => encodeURIComponent(r), String(n))
      assert.ok(r.length <= 1500)
    }
  })
  it('resumeTexte coupé à 1 500', () => {
    const r = resumeTexte(jeu, { societe: 'x'.repeat(5000) })
    assert.ok(r.length <= 1500)
    assert.ok(r.endsWith('…'))
  })
})

describe('couleurs et progression', () => {
  it('texteSur', () => {
    assert.equal(texteSur('#045b5b'), '#ffffff')
    assert.equal(texteSur('#f39221'), '#1b1b1b')
  })
  it('progression', () => {
    assert.equal(progression(0, 13), 0)
    assert.equal(progression(13, 13), 100)
    assert.equal(progression(6, 13), 46)
  })
})

describe('typo', () => {
  it('espace insécable fine avant ? ! : ;', () =>
    assert.equal(typo('Votre société ? Oui : non ; si !'), 'Votre société\u202f? Oui\u202f: non\u202f; si\u202f!'))
})
