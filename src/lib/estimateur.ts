/**
 * L'estimateur de saibodanfakha.com (16/11/2026), règles pures.
 *
 * Il donne un ORDRE DE GRANDEUR, jamais un prix : le chiffrage reste sur devis
 * (décision du 12/10). Les cinq fourchettes sont exactement celles, déjà
 * publiques, de la liste « Budget envisagé » du formulaire de contact — il
 * n'ajoute aucun prix au site. Calées sur des devis réels.
 */

export const FOURCHETTES = [
  'moins de 175 000 F',
  '175 000 – 350 000 F',
  '350 000 – 800 000 F',
  '800 000 – 1 600 000 F',
  'plus de 1 600 000 F',
] as const

export const TYPES = {
  vitrine: { libelle: 'Site vitrine', cran: 1, pagesPrevues: 5, delai: '1 à 3 semaines' },
  complet: { libelle: 'Site complet ou blog', cran: 2, pagesPrevues: 10, delai: '4 à 8 semaines' },
  boutique: { libelle: 'Boutique en ligne', cran: 3, pagesPrevues: 10, delai: '4 à 8 semaines' },
  application: { libelle: 'Application sur mesure', cran: 4, pagesPrevues: Infinity, delai: 'à fixer ensemble, par étapes' },
} as const

export const PAGES = { '1-3': { libelle: '1 à 3 pages', max: 3 }, '4-5': { libelle: '4 à 5 pages', max: 5 }, '6-10': { libelle: '6 à 10 pages', max: 10 }, '11+': { libelle: 'plus de 10 pages', max: 99 } } as const

export const FONCTIONS = {
  paiement: 'Paiement Wave / Orange Money',
  reservation: 'Prise de rendez-vous ou réservation',
  membres: 'Espace membres (comptes, connexion)',
  langues: 'Plusieurs langues',
} as const

export const CONTENUS = { prets: 'Textes et photos déjà prêts', 'a-creer': 'Textes et photos à créer' } as const
export const DELAIS = { normal: 'Pas pressé', urgent: 'Urgent (moins d’un mois)' } as const

export type Reponses = {
  type: keyof typeof TYPES
  pages: keyof typeof PAGES
  fonctions: (keyof typeof FONCTIONS)[]
  contenus: keyof typeof CONTENUS
  delai: keyof typeof DELAIS
}

export function estimer(r: Reponses) {
  const type = TYPES[r.type]
  let cran: number = type.cran
  // Une petite vitrine, textes prêts, sans fonction : le premier cran.
  if (r.type === 'vitrine' && r.pages === '1-3' && r.fonctions.length === 0 && r.contenus === 'prets') cran = 0
  if (PAGES[r.pages].max > type.pagesPrevues) cran += 1
  if (r.type !== 'boutique' && r.type !== 'application' && r.fonctions.some((f) => f === 'paiement' || f === 'membres')) cran += 1
  cran = Math.min(cran, FOURCHETTES.length - 1)

  const notes: string[] = []
  if (r.contenus === 'a-creer') notes.push('La rédaction des textes et la recherche de photos s’ajoutent au devis.')
  if (r.fonctions.includes('langues')) notes.push('Chaque langue en plus demande sa traduction et sa relecture.')
  if (r.delai === 'urgent') notes.push('Un délai court se discute : il dépend du calendrier du moment.')
  if (r.type === 'application') notes.push('Une application se découpe en étapes, chacune avec son prix et son essai.')
  return { fourchette: FOURCHETTES[cran], cran, delai: type.delai, notes }
}

export function messageWhatsApp(r: Reponses) {
  const e = estimer(r)
  const fonctions = r.fonctions.length ? r.fonctions.map((f) => FONCTIONS[f].toLowerCase()).join(', ') : 'aucune'
  return [
    'Bonjour Saïbo, j’ai utilisé l’estimateur de votre site.',
    `Projet : ${TYPES[r.type].libelle}, ${PAGES[r.pages].libelle}.`,
    `Fonctions : ${fonctions}.`,
    `${CONTENUS[r.contenus]}. Délai : ${DELAIS[r.delai].toLowerCase()}.`,
    `Ordre de grandeur affiché : ${e.fourchette}.`,
    'Pouvons-nous en parler ?',
  ].join('\n')
}
