// Le dossier de démarrage en image (1080 × 1920), à garder ou à partager sur WhatsApp.
import { texteSur } from './moteur.ts'

export const POLICE = '"Schibsted Grotesk Variable", "Schibsted Grotesk", system-ui, sans-serif'
const L = 1080
const H_MIN = 1920
const PIED = 140
const MARGE = 96

/** Coupe un texte en lignes qui tiennent dans `largeurMax` ; un mot trop long est coupé en force. */
export function couperLignes(texte: string, largeurMax: number, mesurer: (s: string) => number): string[] {
  const lignes: string[] = []
  let courante = ''
  for (const mot of texte.split(/\s+/).filter(Boolean)) {
    const essai = courante ? `${courante} ${mot}` : mot
    if (mesurer(essai) <= largeurMax) {
      courante = essai
      continue
    }
    if (courante) lignes.push(courante)
    courante = ''
    let reste = mot
    while (mesurer(reste) > largeurMax) {
      let n = reste.length
      while (n > 1 && mesurer(reste.slice(0, n)) > largeurMax) n--
      lignes.push(reste.slice(0, n))
      reste = reste.slice(n)
    }
    courante = reste
  }
  if (courante) lignes.push(courante)
  return lignes
}

export interface DonneesDossier {
  date: string
  titre: string
  lignes: { libelle: string; valeur: string }[]
  chemin: string[]
  couleur: string
  accent: string
  logo?: HTMLImageElement
}

/** Rectangle arrondi ; Safari < 16 (iOS 15) n'a pas ctx.roundRect. */
export function arrondi(ctx: CanvasRenderingContext2D, x: number, y: number, l: number, h: number, r: number) {
  ctx.beginPath()
  if (typeof ctx.roundRect === 'function') {
    ctx.roundRect(x, y, l, h, r)
    return
  }
  const rr = Math.min(r, l / 2, h / 2)
  ctx.moveTo(x + rr, y)
  ctx.arcTo(x + l, y, x + l, y + h, rr)
  ctx.arcTo(x + l, y + h, x, y + h, rr)
  ctx.arcTo(x, y + h, x, y, rr)
  ctx.arcTo(x, y, x + l, y, rr)
  ctx.closePath()
}

function boite(ctx: CanvasRenderingContext2D, x: number, y: number, l: number, h: number, fond: string) {
  ctx.fillStyle = fond
  arrondi(ctx, x, y, l, h, 36)
  ctx.fill()
}

/** Dessine le dossier ; l'image s'allonge au-delà de 1920 px si le contenu le demande. */
export function dessinerDossier(ctx: CanvasRenderingContext2D, d: DonneesDossier): void {
  ctx.canvas.height = H_MIN
  const fin = peindre(ctx, d, H_MIN)
  if (fin + PIED > H_MIN) {
    ctx.canvas.height = fin + PIED
    peindre(ctx, d, fin + PIED)
  }
}

function peindre(ctx: CanvasRenderingContext2D, d: DonneesDossier, H: number): number {
  const encre = texteSur(d.couleur)
  const voile = encre === '#ffffff' ? 'rgba(255,255,255,0.10)' : 'rgba(0,0,0,0.07)'
  const largeur = L - 2 * MARGE
  const police = (poids: number, taille: number) => (ctx.font = `${poids} ${taille}px ${POLICE}`)
  const mesurer = (s: string) => ctx.measureText(s).width

  ctx.fillStyle = d.couleur
  ctx.fillRect(0, 0, L, H)
  ctx.textBaseline = 'top'

  if (d.logo) {
    boite(ctx, L - MARGE - 160, MARGE, 160, 160, '#ffffff')
    const echelle = Math.min(130 / d.logo.naturalWidth, 130 / d.logo.naturalHeight)
    const lw = d.logo.naturalWidth * echelle
    const lh = d.logo.naturalHeight * echelle
    ctx.drawImage(d.logo, L - MARGE - 80 - lw / 2, MARGE + 80 - lh / 2, lw, lh)
  }

  let y = MARGE + (d.logo ? 200 : 40)
  ctx.fillStyle = encre
  ctx.globalAlpha = 0.75
  police(500, 34)
  ctx.fillText(`Dossier de démarrage · ${d.date}`, MARGE, y)
  ctx.globalAlpha = 1
  y += 72

  police(800, 88)
  ctx.letterSpacing = '-2px'
  for (const l of couperLignes(d.titre, largeur, mesurer).slice(0, 4)) {
    ctx.fillText(l, MARGE, y)
    y += 96
  }
  ctx.letterSpacing = '0px'
  y += 40

  // Ce que vous m'avez dit
  const interieur = largeur - 2 * 48
  police(400, 34)
  const blocs = d.lignes.map((l) => couperLignes(l.valeur, interieur, mesurer).slice(0, 3))
  const hDit = 48 + 56 + blocs.reduce((s, b) => s + 46 + b.length * 46 + 16, 0) + 32
  boite(ctx, MARGE, y, largeur, hDit, voile)
  ctx.fillStyle = encre
  police(700, 38)
  ctx.fillText("Ce que vous m'avez dit", MARGE + 48, y + 48)
  let yy = y + 48 + 56
  d.lignes.forEach((l, i) => {
    police(700, 30)
    ctx.globalAlpha = 0.7
    ctx.fillText(l.libelle, MARGE + 48, yy)
    ctx.globalAlpha = 1
    yy += 46
    police(400, 34)
    for (const v of blocs[i]) {
      ctx.fillText(v, MARGE + 48, yy)
      yy += 46
    }
    yy += 16
  })
  y += hDit + 32

  // Le chemin
  police(400, 32)
  const etapes = couperLignes(d.chemin.join(' → '), interieur, mesurer)
  const hChemin = 48 + 56 + 24 + 32 + etapes.length * 44 + 40
  boite(ctx, MARGE, y, largeur, hChemin, voile)
  ctx.fillStyle = encre
  police(700, 38)
  ctx.fillText('Le chemin', MARGE + 48, y + 48)
  const n = d.chemin.length
  const pas = interieur / n
  d.chemin.forEach((_, i) => {
    ctx.fillStyle = i === 0 ? d.accent : encre === '#ffffff' ? 'rgba(255,255,255,0.28)' : 'rgba(0,0,0,0.18)'
    arrondi(ctx, MARGE + 48 + i * pas, y + 48 + 56, pas - 10, 16, 8)
    ctx.fill()
  })
  ctx.fillStyle = encre
  police(400, 32)
  let yc = y + 48 + 56 + 24 + 32
  for (const e of etapes) {
    ctx.fillText(e, MARGE + 48, yc)
    yc += 44
  }
  y += hChemin + 32

  // La promesse de Saïbo
  police(600, 36)
  const promesse = couperLignes('Je reviens vers vous sous 48 h avec la proposition chiffrée.', largeur - 96, mesurer)
  const hPromesse = 48 + promesse.length * 50 + 40
  boite(ctx, MARGE, y, largeur, hPromesse, d.accent)
  ctx.fillStyle = texteSur(d.accent)
  promesse.forEach((p, i) => ctx.fillText(p, MARGE + 48, y + 48 + i * 50))
  const fin = y + hPromesse

  ctx.fillStyle = encre
  ctx.globalAlpha = 0.7
  police(500, 30)
  ctx.fillText('Saïbo Danfakha · saibodanfakha.com', MARGE, H - MARGE)
  ctx.globalAlpha = 1
  return fin
}

/** Partage natif sur téléphone (WhatsApp en un geste) ; sur ordinateur, téléchargement. */
export async function partagerOuTelecharger(canvas: HTMLCanvasElement, nomFichier = 'dossier-de-demarrage.png'): Promise<void> {
  const blob = await new Promise<Blob | null>((ok) => canvas.toBlob(ok, 'image/png'))
  if (!blob) throw new Error("L'image n'a pas pu être créée.")
  const fichier = new File([blob], nomFichier, { type: 'image/png' })
  const tactile = matchMedia('(pointer: coarse)').matches
  if (tactile && navigator.canShare?.({ files: [fichier] })) {
    try {
      await navigator.share({ files: [fichier], title: 'Mon dossier de démarrage' })
      return
    } catch (e) {
      if ((e as DOMException).name === 'AbortError') return
    }
  }
  const url = URL.createObjectURL(blob)
  const a = Object.assign(document.createElement('a'), { href: url, download: nomFichier })
  document.body.append(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 10000)
}
