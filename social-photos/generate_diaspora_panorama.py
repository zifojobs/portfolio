"""Post 2 de l'article du 24/11/2026 (Faire créer son site au Sénégal depuis la France) — skill visuel-projet.
Même direction que generate_restaurant_panorama.py (décidée le 19/11) : couleurs de la fiche Google, Schibsted
Grotesk seule, carte dessinée continue, écrans qui flottent, aucune photo, jamais le vert de WhatsApp.
Idée : le trajet en pointillés part de Paris (diapo 1) et arrive à Dakar (diapo 7).
Textes : SEO/posts/2026-11-24.md (Post 2) et l'article. Aucun montant (barres grises).
Usage : python generate_diaspora_panorama.py  →  visuels-diaspora-panorama-png/Instagram-01..07.png"""
import asyncio
import os

from PIL import Image
from playwright.async_api import async_playwright

import generate_fiche_gb_panorama as gb
import generate_restaurant_panorama as r
from generate_fiche_gb_panorama import CAFE, CREME, SABLE1, SABLE6, TERRA, SAVANE, W, H, N, MAP_TOP, MAP_BOT, fl, pin, ondes, pied
from generate_restaurant_panorama import texte, bar, navig, telephone

OUT_DIR = os.path.join(gb.base.BASE_DIR, "visuels-diaspora-panorama-png")
CSS = r.CSS + f"""
.ville{{position:absolute;z-index:4;background:{CAFE};color:{CREME};border-radius:999px;padding:12px 24px;font-size:24px;font-weight:700;
  box-shadow:0 16px 30px -8px rgba(42,24,16,.35)}}
.ville.dk{{background:{TERRA}}}
.tuile{{flex:1;height:150px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800;color:{CREME}}}
.step{{display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid #eee;font-size:22px;font-weight:600}}
.step .n{{width:44px;height:44px;border-radius:50%;background:{SABLE1};border:2px solid {CAFE};display:flex;align-items:center;justify-content:center;font-weight:800}}
.fact{{margin-left:auto;font-size:16px;font-weight:700;color:{SAVANE};background:#EEF0E2;border-radius:999px;padding:6px 14px}}
.cle{{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid #eee;font-size:21px}}
.cle b{{color:{SAVANE}}}
"""

# ---------- la vraie carte : de Paris à Dakar, déroulée sur les 7 diapos ----------
# Projection équirectangulaire (cos 32°), tournée pour que l'axe Paris → Dakar soit horizontal.
import json
import math

PARIS, DAKAR = (2.3522, 48.8566), (-17.4677, 14.7167)
K = math.cos(math.radians(32))
X_PARIS, X_DAKAR, Y_AXE, ARC = 640, 6480 + 720, 930, 110


def _p(lon, lat):
    return lon * K, lat


_px, _py = _p(*PARIS)
_dx, _dy = _p(*DAKAR)
_L = math.hypot(_dx - _px, _dy - _py)
_ux, _uy = (_dx - _px) / _L, (_dy - _py) / _L
ECH = (X_DAKAR - X_PARIS) / _L          # pixels par degré
SENS = -1                                # l'océan (l'ouest) en haut


def proj(lon, lat):
    x, y = _p(lon, lat)
    a = (x - _px) * _ux + (y - _py) * _uy
    b = (x - _px) * -_uy + (y - _py) * _ux
    return X_PARIS + a * ECH, Y_AXE + SENS * b * ECH


def arc_y(x):
    t = (x - X_PARIS) / (X_DAKAR - X_PARIS)
    return Y_AXE - ARC * math.sin(math.pi * max(0, min(1, t)))


gb.ETAPES = [(X_PARIS if k == 0 else X_DAKAR if k == 6 else k * 1080 + 700, 0) for k in range(7)]
gb.ETAPES[:] = [(x, round(arc_y(x))) for x, _ in gb.ETAPES]
E = gb.ETAPES

PAYS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "carte-france-senegal.json"), encoding="utf-8"))["pays"]
TERRE, COTE, FR, SN = "#E7D8BC", "#D8C9AC", "#F4CDAE", "#D3DDBA"


def carte_geo():
    parts = []
    # houle discrète sur l'océan
    for k in range(-2, 16):
        y0 = 120 + k * 70
        parts.append(f'<path d="M-50 {y0} q 60 -14 120 0 t 120 0 t 120 0" stroke="#EBD9BA" stroke-width="3" fill="none" '
                     f'transform="translate({(k % 3) * 40} 0)"/>')
    for pays in PAYS:
        g = pays["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        fond = FR if pays["nom"] == "France" else SN if pays["nom"] == "Senegal" else TERRE
        d = ""
        for poly in polys:
            for anneau in poly:
                pts = [proj(lo, la) for lo, la in anneau]
                if all(x < -400 or x > W + 400 for x, _ in pts) or all(y < -400 or y > H + 400 for _, y in pts):
                    continue
                d += "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + "Z"
        if d:
            parts.append(f'<path d="{d}" fill="{fond}" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>')
    return f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'


def trajet_geo():
    d = f"M{X_PARIS} {Y_AXE}" + "".join(f" L{x} {arc_y(x):.0f}" for x in range(X_PARIS + 40, X_DAKAR + 1, 40))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{TERRA}"/>' for x, y in E[1:-1])
    return (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;z-index:1" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="{d}" stroke="{TERRA}" stroke-width="7" fill="none" stroke-dasharray="2 20" stroke-linecap="round"/>{dots}</svg>')


def nom_pays(nom, lon, lat, taille=30):
    return nom_px(nom, *proj(lon, lat), taille)


def nom_px(nom, x, y, taille=30):
    return (f'<div style="position:absolute;z-index:0;left:{x:.0f}px;top:{y:.0f}px;transform:translate(-50%,-50%);font-size:{taille}px;'
            f'font-weight:700;letter-spacing:.18em;color:#A6977A;white-space:nowrap">{nom}</div>')


def svg(x, y, w, h, inner, z=2):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;z-index:{z};left:{x}px;top:{y}px;overflow:visible" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg>')


def tour_eiffel(x, y, h=300):
    """Tour Eiffel dessinée à ses vraies proportions (330 m ; étages à 57, 115 et 276 m ; base de 125 m),
    treillis en hachures, arche sous le 1er étage. Base centrée en (x, y)."""
    s = h / 330.0
    w = 125 * s + 20
    c = w / 2

    def ext(z):                        # demi-largeur extérieure, en mètres
        if z <= 115:
            return 62.5 * math.exp(-0.0099 * z)
        if z <= 276:
            return 8 + 12 * ((276 - z) / 161) ** 1.7
        if z <= 300:
            return 8 + (3.5 - 8) * (z - 276) / 24
        return 3.5 + (1.6 - 3.5) * (z - 300) / 12

    def inte(z):                       # demi-largeur de l'ouverture entre les pieds
        if z <= 57:
            return 36.5 + (16 - 36.5) * (z / 57) ** 0.8
        return 16 + (0 - 16) * (z - 57) / 58

    P = lambda u, z: f"{c + u * s:.1f} {h - z * s:.1f}"
    zs = [k * 3 for k in range(105)]   # 0 → 312 m
    dehors = "M" + " L".join(P(-ext(z), z) for z in zs) + " L" + " L".join(P(ext(z), z) for z in reversed(zs)) + "Z"
    zi = [k * 2.3 for k in range(51)]  # 0 → 115 m
    dedans = "M" + " L".join(P(-inte(z), z) for z in zi) + " L" + " L".join(P(inte(z), z) for z in reversed(zi)) + "Z"
    pas = max(4.0, h / 46)
    motif = (f'<defs><pattern id="treillis{int(x)}" patternUnits="userSpaceOnUse" width="{pas:.1f}" height="{pas:.1f}">'
             f'<path d="M0 0 L{pas:.1f} {pas:.1f} M{pas:.1f} 0 L0 {pas:.1f}" stroke="{CAFE}" stroke-width="{max(.8, h / 330):.2f}"/></pattern></defs>')

    def plateau(z, ep, deb):
        return (f'<rect x="{c - (ext(z) + deb) * s:.1f}" y="{h - (z + ep) * s:.1f}" width="{2 * (ext(z) + deb) * s:.1f}" '
                f'height="{ep * s:.1f}" fill="{CAFE}"/>')

    arche = (f'<path d="M{P(-inte(4), 4)} Q {P(0, 52)} {P(inte(4), 4)}" fill="none" stroke="{CAFE}" stroke-width="{max(2.5, 3.2 * s):.1f}"/>'
             f'<path d="M{P(-inte(10), 10)} Q {P(0, 50)} {P(inte(10), 10)}" fill="none" stroke="{CAFE}" stroke-width="{max(1, 1.2 * s):.1f}" opacity=".6"/>')
    n_arc = 9
    larg = 2 * (ext(57) + 4) / n_arc
    arcades = (f'<path d="' + "".join(f"M{P(-ext(57) - 4 + k * larg, 57)} Q {P(-ext(57) - 4 + (k + .5) * larg, 50.5)} {P(-ext(57) - 4 + (k + 1) * larg, 57)} "
                                    for k in range(n_arc)) + f'" fill="none" stroke="{CAFE}" stroke-width="{max(1, 1.4 * s):.1f}"/>')
    t = (motif
         + f'<path d="{dehors} {dedans}" fill-rule="evenodd" fill="url(#treillis{int(x)})" stroke="{CAFE}" stroke-width="{max(2, 2.4 * s):.1f}" stroke-linejoin="round"/>'
         + f'<path d="M{P(-ext(0) + 26, 0)} L{P(-inte(57) - 4, 57)} M{P(ext(0) - 26, 0)} L{P(inte(57) + 4, 57)}" stroke="{CAFE}" stroke-width="{max(1, 1.2 * s):.1f}" opacity=".5"/>'
         + arche + plateau(57, 6, 4) + arcades + plateau(115, 5, 3) + plateau(276, 4, 2)
         + f'<rect x="{c - 3.4 * s:.1f}" y="{h - 296 * s:.1f}" width="{6.8 * s:.1f}" height="{16 * s:.1f}" fill="{CAFE}"/>'
         + f'<path d="M{P(0, 312)} L{P(0, 330)}" stroke="{CAFE}" stroke-width="{max(2, 2 * s):.1f}"/>')
    return svg(x - c, y - h, w, h, t)


def baobab(x, y, h=300):
    w = h * 1.1
    c = w / 2
    t = (f'<path d="M{c-34} {h} C {c-30} {h*.7}, {c-40} {h*.5}, {c-26} {h*.36} L{c+26} {h*.36} C {c+40} {h*.5}, {c+30} {h*.7}, {c+34} {h} Z" fill="{CAFE}"/>'
         f'<g stroke="{CAFE}" stroke-width="12" stroke-linecap="round" fill="none">'
         f'<path d="M{c-14} {h*.4} Q {c-60} {h*.25} {c-120} {h*.2}"/><path d="M{c+14} {h*.4} Q {c+70} {h*.28} {c+130} {h*.18}"/>'
         f'<path d="M{c} {h*.38} L{c+6} {h*.1}"/></g>'
         + "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{SAVANE}" opacity=".92"/>'
                   for cx, cy, rx, ry in ((c-130, h*.17, 62, 34), (c+138, h*.15, 66, 34), (c+6, h*.07, 70, 36), (c-60, h*.11, 48, 28), (c+70, h*.09, 52, 28))))
    return svg(x - c, y - h, w, h, t)


def pirogue(x, y, w=300, rot=-3):
    h = w * 0.22
    t = (f'<g transform="rotate({rot} {w/2} {h/2})">'
         f'<path d="M0 {h*.25} Q {w/2} {h*1.35} {w} {h*.25} L {w-18} {h*.62} Q {w/2} {h*1.05} 18 {h*.62} Z" fill="{CAFE}"/>'
         f'<path d="M6 {h*.32} Q {w/2} {h*1.2} {w-6} {h*.32} L {w-12} {h*.46} Q {w/2} {h*1.1} 12 {h*.46} Z" fill="{TERRA}"/>'
         f'<path d="M14 {h*.5} Q {w/2} {h*1.06} {w-14} {h*.5} L {w-17} {h*.58} Q {w/2} {h*1.02} 17 {h*.58} Z" fill="{SAVANE}"/>'
         f'<path d="M-20 {h*.95} q 30 -10 60 0 t 60 0 M{w-80} {h*1.05} q 30 -10 60 0 t 60 0" stroke="#D9C7A6" stroke-width="4" fill="none"/></g>')
    return svg(x - w / 2, y - h, w, h * 1.3, t)


def avion(x, y, taille=70, rot=0):
    t = (f'<g transform="rotate({rot} 50 50)"><path d="M8 50 L92 50 M50 50 L32 16 L44 16 L66 50 L44 84 L32 84 Z M8 50 L4 36 L12 36 L22 50 L12 64 L4 64 Z" '
         f'fill="{CAFE}" stroke="{CAFE}" stroke-width="6" stroke-linejoin="round"/></g>')
    return svg(x - taille / 2, y - taille / 2, 100, 100, t, 3).replace(f'width="100" height="100"', f'width="{taille}" height="{taille}"', 1)


def etiquette(x, y, texte_, fond=CREME, encre=CAFE, rot=0):
    return (f'<div style="position:absolute;z-index:4;left:{x}px;top:{y}px;background:{fond};color:{encre};border:2.5px solid {CAFE};border-radius:999px;'
            f'padding:10px 22px;font-size:22px;font-weight:700;white-space:nowrap;transform:rotate({rot}deg);box-shadow:0 14px 26px -10px rgba(42,24,16,.3)">{texte_}</div>')


def ville(x, y, nom, dakar=False):
    return f'<div class="ville{" dk" if dakar else ""}" style="left:{x}px;top:{y}px">{nom}</div>'


def d1():
    x, y = E[0]
    return (texte(0, "Guide · diaspora", 'Tu es en France,<br><em>ton projet est au <span style="white-space:nowrap">Sénégal&nbsp;?</span></em>',
                  "Faire créer ton site à distance, sans mauvaise surprise.", 88)
            + tour_eiffel(x - 330, y + 150, 420) + ondes(x, y - 20) + pin(x, y) + ville(x - 60, y + 50, "Paris")
            + avion(x + 230, arc_y(x + 230) - 6, 78, -8)
            + etiquette(x + 120, y - 230, "4 205 km jusqu'à Dakar", rot=-3)
            + '<div class="swipe" style="left:780px;top:1170px">GLISSE →</div>' + pied(0))


def d2():
    x0 = 1080
    visio = fl(x0 + 80, 610, 460,
               f'<div style="padding:18px 20px"><div class="lbl">① L\'échange en visio</div>'
               f'<div style="display:flex;gap:12px;margin-top:12px"><div class="tuile" style="background:{CAFE}">P</div>'
               f'<div class="tuile" style="background:{SAVANE}">D</div></div>'
               f'<div style="display:flex;justify-content:center;gap:12px;margin-top:14px">'
               f'<i style="width:44px;height:44px;border-radius:50%;background:{SABLE1}"></i><i style="width:44px;height:44px;border-radius:50%;background:{TERRA}"></i></div></div>',
               "transform:rotate(-3deg)")
    ecrit = fl(x0 + 560, 680, 420,
               f'<div style="padding:24px 26px"><div style="font-size:30px;font-weight:800;letter-spacing:-.02em">Par écrit</div>'
               f'<div class="chk"><i>✓</i>Les pages</div><div class="chk"><i>✓</i>Les délais</div><div class="chk"><i>✓</i>Le devis</div>'
               f'<div style="margin-top:12px">{bar(300)}<br>{bar(220)}</div></div>',
               "border-radius:24px 0 24px 0;transform:rotate(2deg)")
    return (texte(1, "① Le cadrage", "Une visio,<br><em>puis tout par écrit</em>",
                  "Pages, délais, devis&nbsp;: tout est noté avant de commencer.")
            + visio + ecrit + pied(1))


def d3():
    x0 = 2160
    nav = fl(x0 + 80, 620, 600,
             navig("ton-site · version en ligne")
             + f'<div style="height:170px;background:#F3DCC6;margin:18px 22px 0;border-radius:12px"></div>'
             f'<div style="padding:16px 22px 22px">' + "".join(f'<div class="skel" style="width:{w}%;margin-top:12px"></div>' for w in (86, 70, 78)) + '</div>',
             "transform:rotate(-2deg)")
    page = (f'<div style="height:120px;background:#F3DCC6"></div><div style="padding:16px 18px">'
            + "".join(f'<div class="skel" style="width:{w}%;margin-top:12px"></div>' for w in (90, 72, 84, 60)) + '</div>')
    x, y = E[2]
    return (texte(2, "② La version en ligne", "Ton site en ligne,<br><em>des deux côtés</em>",
                  "Tu l'ouvres depuis Paris, ton associé depuis Dakar.")
            + nav + telephone(x0 + 700, 640, 5, page, 470)
            + ville(x0 + 120, 580, "Depuis Paris") + ville(x0 + 760, 590, "Depuis Dakar", True) + pied(2))


def d4():
    x0 = 3240
    chat = fl(x0 + 80, 620, 500,
              f'<div style="display:flex;align-items:center;gap:12px;padding:16px 22px;background:{SABLE1};border-bottom:1px solid #eee">'
              f'<div class="av" style="width:42px;height:42px;font-size:19px;background:{SAVANE}">S</div><div style="font-size:19px;font-weight:600">Suivi du site</div></div>'
              f'<div style="padding:20px;display:flex;flex-direction:column;gap:12px">'
              f'<div class="bub">La page Accueil est en ligne, tu peux regarder&nbsp;?</div>'
              f'<div class="bub me">Vu, c\'est bon pour moi&nbsp;!</div></div>',
              "transform:rotate(-2deg)")
    mail = fl(x0 + 560, 900, 420,
              f'<div style="padding:20px 24px"><div class="lbl">E-mail</div>'
              f'<div style="font-size:21px;font-weight:700;margin-top:8px">Objet&nbsp;: validation de la page Accueil</div>'
              f'<div style="margin-top:12px">{bar(320)}<br>{bar(240)}</div></div>',
              "border-radius:24px 0 24px 0;transform:rotate(3deg)")
    return (texte(3, "③ Le suivi", "WhatsApp pour aller vite,<br><em>l'e-mail pour garder</em>",
                  "L'échange rapide sur WhatsApp. Ce qui doit rester écrit, par e-mail.", 74)
            + chat + mail + avion(x0 + 640, arc_y(x0 + 640) - 4, 70, 0)
            + etiquette(x0 + 470, 1100, "1 h de décalage en hiver, 2 h en été", rot=-2) + pied(3))


def d5():
    x0 = 4320
    etapes = "".join(f'<div class="step"><div class="n">{k}</div>{t}<span class="fact">Facture ✓</span></div>'
                     for k, t in ((1, "Acompte au démarrage"), (2, "Validation"), (3, "Mise en ligne")))
    pay = fl(x0 + 140, 630, 640,
             f'<div style="padding:24px 30px"><div class="lbl">④ Le paiement, en trois temps</div>{etapes}'
             f'<div style="display:flex;align-items:center;gap:12px;margin-top:16px"><div class="ko" style="width:40px;height:40px;font-size:20px">✕</div>'
             f'<span style="font-size:19px;color:{SABLE6}">Tout payer avant de voir le site</span></div></div>',
             "transform:rotate(-2deg)")
    return (texte(4, "④ Le paiement", "Payer par étapes,<br><em>jamais tout d'avance</em>",
                  "Une facture à chaque versement, même pour un petit montant.")
            + pay + pied(4))


def d6():
    x0 = 5400
    cles = "".join(f'<div class="cle"><span>{a}</span><b>À ton nom ✓</b></div>' for a in ("Nom de domaine", "Hébergement", "Accès"))
    titre = fl(x0 + 80, 640, 560,
               f'<div style="padding:24px 30px"><div class="lbl">⑤ Qui possède quoi</div>{cles}</div>',
               "transform:rotate(-2deg)")
    cle = (f'<div style="position:absolute;z-index:4;left:{x0 + 700}px;top:700px;width:220px;height:220px;border-radius:50%;background:#fff;'
           f'border:8px solid {CAFE};box-shadow:0 30px 60px -12px rgba(42,24,16,.35);display:flex;flex-direction:column;align-items:center;'
           f'justify-content:center;transform:rotate(4deg)"><div style="font-size:60px;line-height:1">🔑</div>'
           f'<div style="font-size:19px;font-weight:700;color:{TERRA};margin-top:8px;text-align:center;line-height:1.15">Remis à la<br>fin du projet</div></div>')
    return (texte(5, "⑤ La propriété", "Domaine, hébergement,<br><em>accès&nbsp;: à ton nom</em>",
                  "Ton site t'appartient. Tout t'est remis à la fin.", 86)
            + titre + cle + pied(5))


def d7():
    x0 = 6480
    blog = fl(x0 + 60, 680, 480,
              navig("saibodanfakha.com/blog")
              + f'<div style="padding:26px 30px"><div style="font-size:16px;font-weight:700;color:{TERRA}">Blog · 24 novembre 2026</div>'
              f'<div style="font-size:34px;font-weight:800;line-height:1.08;letter-spacing:-0.02em;margin-top:12px">Faire créer son site au Sénégal depuis la France</div>'
              f'<div style="font-size:18px;color:{SABLE6};margin-top:12px">La méthode et les 7 questions à poser avant de signer</div></div>',
              "transform:rotate(-2deg)")
    x, y = E[6]
    return (texte(6, "La méthode complète", 'Un projet entre la France<br><em>et le <span style="white-space:nowrap">Sénégal&nbsp;?</span></em>',
                  "La méthode complète est dans l'article, lien en bio. Écris-moi.", 72)
            + baobab(x + 130, y + 130, 240) + pirogue(x - 60, y + 215, 380)
            + blog + ondes(x, y - 20, (110, 170, 230)) + pin(x, y) + ville(x - 70, y + 50, "Dakar", True)
            + pied(6, "LIEN EN BIO ↗"))


def html():
    corps = (carte_geo() + trajet_geo()
             + nom_px("FRANCE", 860, 1070) + nom_pays("ESPAGNE", -3.5, 40.0) + nom_px("MAROC", 4500, 1060)
             + nom_pays("MAURITANIE", -11.5, 20.5) + nom_pays("SÉNÉGAL", -14.8, 15.2)
             + nom_px("Océan Atlantique", 4760, 1196, 24)
             + f'<div class="fade" style="top:0;height:{MAP_TOP + 140}px;background:linear-gradient({CREME} 72%,rgba(254,243,226,0))"></div>'
             + f'<div class="fade" style="top:{MAP_BOT - 20}px;bottom:0;background:linear-gradient(rgba(254,243,226,0),{CREME} 45%)"></div>'
             + "".join(f'<div class="ribbon" style="left:{k * 1080}px;right:auto;width:1080px"><i style="background:{CAFE}"></i><i style="background:{TERRA}"></i><i style="background:{SAVANE}"></i></div>' for k in range(N))
             + d1() + d2() + d3() + d4() + d5() + d6() + d7())
    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">{r.FONTS}<style>{CSS}</style></head>'
            f'<body><div class="pano">{corps}</div></body></html>')


async def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "_panorama.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html())
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H})
        await pg.goto("file:///" + path.replace("\\", "/"), wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        bad = await pg.evaluate("""() => [...document.querySelectorAll('.tx, .foot, .swipe, .fl, .tile, .ville')].map(e => {
            const r = e.getBoundingClientRect(); return [Math.floor(r.left / 1080), Math.floor((r.right - 1) / 1080), e.className, Math.round(r.bottom)] })
            .filter(a => a[0] !== a[1])""")
        print("éléments à cheval sur deux diapos :", bad or "aucun")
        full = os.path.join(OUT_DIR, "_panorama.png")
        await pg.screenshot(path=full)
        await b.close()
    os.remove(path)
    im = Image.open(full)
    for i in range(N):
        im.crop((i * 1080, 0, (i + 1) * 1080, H)).save(os.path.join(OUT_DIR, f"Instagram-{i + 1:02d}.png"))
    im.resize((W // 4, H // 4)).save(os.path.join(OUT_DIR, "_panorama-apercu.png"))
    print("[OK] 7 diapos")


if __name__ == "__main__":
    asyncio.run(main())
