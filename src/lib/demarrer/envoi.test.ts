import assert from 'node:assert/strict'
import { describe, it } from 'node:test'

import { chargerConfig, delai, envoyerDossier, URL_AGENT, type Dossier } from './envoi.ts'

const d: Dossier = {
  version: 1,
  idDossier: '6f1c2b0e-8d1a-4c4e-9b8a-2f3d4e5f6a7b',
  jeu: 'visibilite-securite',
  jeton: null,
  envoyeLe: '2026-11-22T16:30:00.000Z',
  reponses: { prenom: 'Awa', societe: 'Exemple Sécurité' },
}
const repondre = (status: number, corps: unknown = {}) =>
  (async () => new Response(JSON.stringify(corps), { status })) as unknown as typeof fetch

describe('envoyerDossier', () => {
  it('200 → ok, POST JSON vers /dossier', async () => {
    let appel: [string, RequestInit] | undefined
    const f = (async (url: string, init: RequestInit) => {
      appel = [url, init]
      return new Response('{"ok":true}', { status: 200 })
    }) as unknown as typeof fetch
    assert.deepEqual(await envoyerDossier(d, f), { ok: true })
    assert.equal(appel![0], `${URL_AGENT}/dossier`)
    assert.equal(appel![1].method, 'POST')
    assert.deepEqual(JSON.parse(appel![1].body as string), d)
  })
  it('échec réseau garde la saisie : ok false + « Vos réponses sont gardées »', async () => {
    const f = (async () => { throw new TypeError('Failed to fetch') }) as unknown as typeof fetch
    const r = await envoyerDossier(d, f)
    assert.equal(r.ok, false)
    assert.match((r as { message: string }).message, /Vos réponses sont gardées/)
  })
  it('429 → « dans une heure »', async () => {
    const r = await envoyerDossier(d, repondre(429))
    assert.match((r as { message: string }).message, /dans une heure/)
  })
  it('500 → ok false, message WhatsApp', async () => {
    const r = await envoyerDossier(d, repondre(500))
    assert.equal(r.ok, false)
    assert.match((r as { message: string }).message, /WhatsApp/)
  })
})

describe('chargerConfig', () => {
  it('jeton "../x" → absent sans appel réseau', async () => {
    let appels = 0
    const f = (async () => { appels++; return new Response('{}') }) as unknown as typeof fetch
    assert.deepEqual(await chargerConfig('../x', f), { statut: 'absent' })
    assert.equal(appels, 0)
  })
  it('404 → absent', async () => assert.deepEqual(await chargerConfig('a'.repeat(24), repondre(404)), { statut: 'absent' }))
  it('réseau coupé → erreur (pas absent : le lien reste valable)', async () => {
    const f = (async () => { throw new TypeError('Failed to fetch') }) as unknown as typeof fetch
    assert.deepEqual(await chargerConfig('a'.repeat(24), f), { statut: 'erreur' })
  })
  it('429 → erreur', async () => assert.deepEqual(await chargerConfig('a'.repeat(24), repondre(429)), { statut: 'erreur' }))
  it('200 → la config', async () => {
    const config = { prenom: 'Awa', societe: 'Exemple Sécurité', couleur: '#045b5b', accent: '#f39221', jeu: 'visibilite-securite' }
    assert.deepEqual(await chargerConfig('a'.repeat(24), repondre(200, config)), { statut: 'ok', config })
  })
  it('200 mais forme fausse → absent', async () =>
    assert.deepEqual(await chargerConfig('a'.repeat(24), repondre(200, { prenom: 3 })), { statut: 'absent' }))
})

describe('navigateurs anciens (iOS 15)', () => {
  it('sans AbortSignal.timeout, l’envoi part quand même', async () => {
    const original = AbortSignal.timeout
    // @ts-expect-error simulation d'un Safari 15
    delete AbortSignal.timeout
    try {
      assert.equal(typeof (AbortSignal as { timeout?: unknown }).timeout, 'undefined')
      assert.deepEqual(await envoyerDossier(d, repondre(200)), { ok: true })
      assert.ok(delai(1000) instanceof AbortSignal)
    } finally {
      AbortSignal.timeout = original
    }
  })
})
