// Le questionnaire de démarrage (22/11/2026) : un moteur unique, les jeux de questions sont des données.
// Spec : docs/superpowers/specs/2026-11-21-questionnaire-demarrage-design.md

export type TypeChamp = 'texte' | 'choix' | 'puces' | 'couleur' | 'logo'

export interface Option {
  v: string
  l: string
  /** Couleur d'accent associée (champ « couleur » seulement). */
  accent?: string
}

export interface Champ {
  id: string
  type: TypeChamp
  libelle?: string
  options?: Option[]
  /** Ajoute une option « Autre » suivie d'un texte libre (clé `${id}.autre`). */
  autre?: boolean
  /** Champ « couleur » : toute couleur #rrggbb est acceptée en plus des options. */
  libre?: boolean
  max?: number
  facultatif?: boolean
  carte?: 'nom' | 'tags'
  /** Champ montré seulement sans lien personnalisé. */
  sansLien?: boolean
  prerempli?: 'prenom' | 'societe'
  /** Libellé de la ligne dans « Ce que vous m'avez dit ». */
  dossier?: string
}

export interface Question {
  id: string
  titre: string
  pourquoi: string
  champs: Champ[]
  /** Un seul champ rempli suffit. */
  auMoinsUn?: boolean
}

export interface Jeu {
  id: string
  version: number
  titreDossier: string
  chemin: string[]
  questions: Question[]
}

export type Valeur = string | string[]
export type Reponses = Record<string, Valeur>

export interface ConfigClient {
  prenom: string
  societe: string
  couleur: string
  accent: string
  logo?: string
  jeu: string
}
