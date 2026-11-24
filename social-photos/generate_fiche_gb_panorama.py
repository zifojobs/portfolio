"""Post 2 de l'article du 03/11/2026 (Fiche Google Business : le guide pour une PME à Dakar) — skill visuel-projet.
Style « interface vivante » (choix de Saïbo, 04/11) : UN panorama de 7 x 1080 px, une carte dessinée continue,
un trajet en pointillés qui passe d'une diapo à l'autre, des écrans qui flottent au-dessus. Découpé en 7 diapos 1080x1350.
Charte gardée (crème, noir café, terracotta, savane, Fraunces + Inter). Aucune personne, aucune photo, aucun fait
hors de src/pages/blog/fiche-google-business-pme-dakar.astro. Jamais le vert de WhatsApp.
Usage : python generate_fiche_gb_panorama.py   →  visuels-fiche-gb-panorama-png/Instagram-01..07.png (+ _panorama.png)"""
import asyncio
import os
import random
from PIL import Image
from playwright.async_api import async_playwright

import generate_seo_dakar as base
from generate_seo_dakar import CAFE, CREME, SABLE1, SABLE3, SABLE6, TERRA, SAVANE, SEARCH, FONTS, LOGO_URI, LOGO_RATIO

N = 7
W, H = 1080 * N, 1350
OUT_DIR = os.path.join(base.BASE_DIR, "visuels-fiche-gb-panorama-png")
ROUGE = "#B3261E"
OR = "#E8A33A"
MAP_TOP, MAP_BOT = 520, 1210


# ---------- la carte dessinée (SVG, déterministe) ----------
def carte_svg():
    rnd = random.Random(1103)
    parts = []
    # îlots
    x = -40
    while x < W + 40:
        bw = rnd.randint(110, 190)
        y = MAP_TOP - 40
        while y < MAP_BOT + 40:
            bh = rnd.randint(80, 150)
            c = rnd.choice(["#EDE4D2", "#E9DFCA", "#F1E9D9", "#E6DCC5"])
            if rnd.random() < 0.08:
                c = "#DCE3CB"  # jardin
            parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="{c}"/>')
            y += bh + 22
        x += bw + 22
    # avenues en diagonale et grande voie
    for k in range(9):
        x0 = k * 900 - 200
        parts.append(f'<path d="M{x0} {MAP_BOT + 60} L{x0 + 700} {MAP_TOP - 60}" stroke="#fff" stroke-width="30" stroke-linecap="round"/>')
    parts.append(f'<path d="M-50 {MAP_TOP + 300} C 1500 {MAP_TOP + 180}, 3000 {MAP_TOP + 470}, 4500 {MAP_TOP + 300} S 6800 {MAP_TOP + 220}, {W + 50} {MAP_TOP + 360}" '
                 f'stroke="#fff" stroke-width="38" fill="none" stroke-linecap="round"/>')
    return f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'


# trajet : une étape par diapo (coordonnées du panorama)
ETAPES = [(820, 930), (1080 + 700, 960), (2160 + 900, 860), (3240 + 820, 930), (4320 + 900, 1030), (5400 + 720, 1080), (6480 + 300, 1000)]


def trajet_svg():
    pts = ETAPES
    d = f"M{pts[0][0]} {pts[0][1]}"
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        cx = (x1 + x2) / 2
        d += f" C {cx} {y1 - 160}, {cx} {y2 + 160}, {x2} {y2}"
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{TERRA}"/>' for x, y in pts[1:-1])
    return (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;z-index:1" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="{d}" stroke="{TERRA}" stroke-width="6" fill="none" stroke-dasharray="2 18" stroke-linecap="round" opacity=".9"/>{dots}</svg>')


CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;font-family:'Inter',sans-serif;color:{CAFE};background:{CREME}}}
.pano{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{CREME}}}
.fade{{position:absolute;left:0;right:0;z-index:1;pointer-events:none}}
.ribbon{{position:absolute;top:0;left:0;right:0;height:10px;display:flex;z-index:5}} .ribbon i{{flex:1}}
.tx{{position:absolute;top:110px;width:920px;z-index:4}}
.kick{{display:flex;align-items:center;gap:14px;font-size:22px;font-weight:700;letter-spacing:3.5px;text-transform:uppercase;color:{TERRA}}}
.trema{{display:inline-flex;gap:7px}} .trema i{{width:11px;height:11px;border-radius:50%;background:{TERRA}}} .trema i+i{{background:{SAVANE}}}
h1{{font-family:'Fraunces',serif;font-weight:600;letter-spacing:-0.03em;line-height:1;margin-top:24px;font-size:98px}}
h1 em{{font-style:italic;font-weight:500;color:{TERRA}}}
.sub{{font-size:27px;line-height:1.45;color:{SABLE6};max-width:860px;margin-top:26px}}
.foot{{position:absolute;bottom:56px;width:920px;padding-top:28px;border-top:1.5px solid {SABLE3};display:flex;justify-content:space-between;align-items:center;z-index:4}}
.foot img{{height:32px;width:calc(32px * {LOGO_RATIO:.3f})}}
.dots{{display:flex;align-items:center;gap:10px}} .dots i{{width:12px;height:12px;border-radius:50%;background:{SABLE3}}}
.dots i.on{{width:34px;border-radius:6px;background:{TERRA}}}
.cta{{font-size:21px;font-weight:700;letter-spacing:3px;color:{TERRA}}}
.swipe{{position:absolute;z-index:4;font-size:20px;font-weight:700;letter-spacing:3px;color:{TERRA}}}
/* objets flottants */
.fl{{position:absolute;z-index:3;background:#fff;border-radius:0 40px 0 40px;overflow:hidden;
  box-shadow:0 2px 0 rgba(42,24,16,.04),0 18px 30px -8px rgba(42,24,16,.18),0 50px 90px -20px rgba(42,24,16,.28),0 0 0 1px rgba(42,24,16,.06)}}
.gbar{{display:flex;align-items:center;gap:16px;border:1.5px solid #dfe1e5;border-radius:999px;padding:16px 24px;font-size:25px;color:#202124;background:#fff}}
.lbl{{font-size:15px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{SABLE6}}}
.ok,.ko{{width:36px;height:36px;border-radius:50%;color:#fff;font-weight:700;font-size:19px;display:flex;align-items:center;justify-content:center;flex:none}}
.ok{{background:{SAVANE}}} .ko{{background:{ROUGE}}}
.btn{{display:inline-block;background:{TERRA};color:{CREME};font-weight:600;font-size:20px;border-radius:999px;padding:12px 24px}}
.skel{{height:13px;border-radius:7px;background:#eceae6}}
.pin{{position:absolute;z-index:3;width:74px;height:74px;margin:-74px 0 0 -37px}}
.pin b{{position:absolute;inset:0;background:{TERRA};border-radius:50% 50% 50% 0;transform:rotate(-45deg);box-shadow:0 10px 18px rgba(42,24,16,.3)}}
.pin b::after{{content:"";position:absolute;left:24px;top:24px;width:26px;height:26px;border-radius:50%;background:{CREME}}}
.pin.o b{{background:#c3bcae}}
.ombre{{position:absolute;z-index:2;width:60px;height:16px;margin:-6px 0 0 -30px;border-radius:50%;background:rgba(42,24,16,.22);filter:blur(3px)}}
.onde{{position:absolute;z-index:2;border-radius:50%;border:3px solid {TERRA};transform:translate(-50%,-50%)}}
.row{{display:flex;align-items:center;gap:18px;padding:20px 26px;border-top:1px solid #eee}}
.av{{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Fraunces,serif;font-size:24px;font-weight:600;color:#fff;flex:none}}
.row .m{{font-size:22px;font-weight:600}} .row .r{{font-size:17px;color:{SABLE6};margin-top:3px}}
.chip{{display:inline-block;font-size:19px;font-weight:600;border-radius:999px;padding:9px 18px;background:#EEF0E3;color:{SAVANE};margin:0 6px 8px 0}}
.bub{{max-width:82%;border-radius:20px 20px 20px 6px;padding:14px 18px;font-size:19px;line-height:1.4;background:{SABLE1}}}
.bub.me{{margin-left:auto;border-radius:20px 20px 6px 20px;background:#FCEBDD}}
.chk{{display:flex;align-items:center;gap:12px;font-size:19px;padding:8px 0}}
.chk i{{width:24px;height:24px;border-radius:7px;background:{SAVANE};color:#fff;font-style:normal;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none}}
.tile{{position:absolute;z-index:3;background:#fff;padding:14px 14px 20px;border-radius:6px;box-shadow:0 20px 40px -10px rgba(42,24,16,.3),0 0 0 1px rgba(42,24,16,.06)}}
.tile .img{{position:relative;width:100%;border-radius:3px;overflow:hidden}}
.tile .cap{{font-size:18px;font-weight:600;margin-top:12px}}
"""


def pin(x, y, gris=False):
    return f'<div class="ombre" style="left:{x}px;top:{y}px"></div><div class="pin{" o" if gris else ""}" style="left:{x}px;top:{y}px"><b></b></div>'


def ondes(x, y, rs=(110, 170, 230)):
    return "".join(f'<div class="onde" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;opacity:{0.55 - i * 0.17}"></div>' for i, r in enumerate(rs))


def texte(i, kick, titre, sub):
    x = i * 1080 + 80
    return (f'<div class="tx" style="left:{x}px"><div class="kick"><span class="trema"><i></i><i></i></span>{kick}</div>'
            f'<h1>{titre}</h1><p class="sub">{sub}</p></div>')


def pied(i, droite=None):
    x = i * 1080 + 80
    if droite is None:
        droite = '<div class="dots">' + "".join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(N)) + "</div>"
    else:
        droite = f'<div class="cta">{droite}</div>'
    return f'<div class="foot" style="left:{x}px"><img src="{LOGO_URI}" alt="Saïbo Danfakha">{droite}</div>'


def fl(x, y, w, inner, extra=""):
    return f'<div class="fl" style="left:{x}px;top:{y}px;width:{w}px;{extra}">{inner}</div>'


def skel_ligne():
    return ('<div style="flex:1"><div class="skel" style="width:58%;height:17px"></div>'
            '<div class="skel" style="width:84%;margin-top:10px"></div></div>')


# ---------- les 7 étapes ----------
def d1():
    x0 = 0
    rech = fl(x0 + 80, 600, 620,
              f'<div style="padding:22px 24px 12px"><div class="gbar">{SEARCH}<span>garage Pikine</span></div></div>'
              f'<div class="row">{skel_ligne()}<div class="ok" style="background:#c9c4ba">1</div></div>'
              f'<div class="row">{skel_ligne()}<div class="ok" style="background:#c9c4ba">2</div></div>',
              "transform:rotate(-2deg)")
    vide = (f'<div style="position:absolute;z-index:3;left:{ETAPES[0][0] - 70}px;top:{ETAPES[0][1] - 70}px;width:140px;height:140px;'
            f'border-radius:50%;border:4px dashed {TERRA};background:rgba(254,243,226,.7);display:flex;align-items:center;justify-content:center;'
            f'font-family:Fraunces,serif;font-size:64px;font-weight:600;color:{TERRA}">?</div>'
            f'<div style="position:absolute;z-index:3;left:{ETAPES[0][0] - 120}px;top:{ETAPES[0][1] + 84}px;width:240px;text-align:center;'
            f'font-size:21px;font-weight:700;color:{TERRA}">Votre entreprise&nbsp;?</div>')
    return (texte(0, "Guide · fiche Google Business", 'Votre PME est-elle<br><em>sur la <span style="white-space:nowrap">carte&nbsp;?</span></em>',
                  "Gratuite, et souvent laissée vide. Suivez le trajet&nbsp;: on la construit, étape par étape.")
            + pin(300, 1030, True) + pin(540, 1110, True) + rech + vide
            + f'<div class="swipe" style="left:{x0 + 760}px;top:1150px">GLISSEZ →</div>' + pied(0))


def d2():
    x0 = 1080
    doublon = fl(x0 + 150, 590, 470,
                 f'<div style="padding:22px 26px;opacity:.55"><div class="lbl">Fiche en double</div>'
                 f'<div style="font-family:Fraunces,serif;font-size:28px;font-weight:600;margin-top:8px">Le nom de votre entreprise</div></div>',
                 "transform:rotate(-4deg)")
    fiche = fl(x0 + 80, 720, 540,
               f'<div style="height:110px;background:#EEF0E6;position:relative"><div style="position:absolute;left:46%;top:18px">'
               f'<div style="width:40px;height:40px;background:{TERRA};border-radius:50% 50% 50% 0;transform:rotate(-45deg)"></div></div></div>'
               f'<div style="padding:22px 28px 26px"><div style="font-family:Fraunces,serif;font-size:32px;font-weight:600">Le nom de votre entreprise</div>'
               f'<div style="font-size:18px;color:{SABLE6};margin-top:6px">Créée par un ancien employé, un client… ou vous, il y a des années</div>'
               f'<div style="margin-top:20px;display:flex;align-items:center;gap:16px"><span class="btn">Revendiquer</span>'
               f'<span style="font-size:18px;color:{SABLE6}">Doublon&nbsp;? <b style="color:{CAFE}">Signalez-le</b></span></div></div>',
               "transform:rotate(1.5deg)")
    loupe = (f'<div style="position:absolute;z-index:3;left:{x0 + 700}px;top:740px;width:240px;height:240px;border-radius:50%;'
             f'border:12px solid #fff;background:#E9DFCA;box-shadow:0 30px 60px -10px rgba(42,24,16,.35)"></div>'
             f'<div style="position:absolute;z-index:3;left:{x0 + 905}px;top:950px;width:34px;height:120px;background:{CAFE};border-radius:17px;transform:rotate(-40deg)"></div>')
    return (texte(1, "① Cherchez d'abord", "Elle existe<br><em>peut-être déjà</em>",
                  "Cherchez votre nom sur Google Maps. Une fiche existe&nbsp;? Revendiquez-la au lieu d'en créer une deuxième.")
            + doublon + fiche + loupe + pin(x0 + 820, 870) + pied(1))


def d3():
    x0 = 2160
    rows = (f'<div class="row" style="border-top:none"><div class="av" style="background:{SAVANE}">E</div><div style="flex:1"><div class="m">Compte de l\'entreprise</div>'
            f'<div class="r">Propriétaire · reste à vous</div></div><div class="ok">✓</div></div>'
            f'<div class="row"><div class="av" style="background:{TERRA}">P</div><div style="flex:1"><div class="m">Votre prestataire</div>'
            f'<div class="r">Gestionnaire · ajouté par vous</div></div><div class="ok">✓</div></div>'
            f'<div class="row" style="color:#9b9488"><div class="av" style="background:#c9c4ba">S</div><div style="flex:1"><div class="m">Gmail perso d\'un stagiaire</div>'
            f'<div class="r">S\'il part, vous perdez l\'accès</div></div><div class="ko">✕</div></div>')
    carte = fl(x0 + 80, 640, 640, f'<div class="lbl" style="padding:24px 26px 8px">Accès à la fiche</div>{rows}', "transform:rotate(-1.5deg)")
    badge = (f'<div style="position:absolute;z-index:3;left:{x0 + 760}px;top:640px;width:170px;height:170px;border-radius:50%;background:{SAVANE};'
             f'color:{CREME};display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 30px 60px -12px rgba(42,24,16,.35);transform:rotate(8deg)">'
             f'<div style="font-family:Fraunces,serif;font-size:56px;line-height:1">✓</div><div style="font-size:16px;font-weight:700;letter-spacing:2px;margin-top:6px">À VOTRE NOM</div></div>')
    return (texte(2, "② Le bon compte", "À votre nom,<br><em>pas au sien</em>",
                  "Comme votre nom de domaine&nbsp;: ce qui porte le nom de l'entreprise reste à l'entreprise.")
            + carte + badge + pied(2))


def d4():
    x0 = 3240
    cat = fl(x0 + 80, 640, 460,
             f'<div style="padding:24px 26px"><div class="lbl">③ Catégorie principale</div>'
             f'<div style="margin-top:16px;display:flex;align-items:center;gap:14px;padding:16px 18px;background:#EEF0E3;border-radius:0 20px 0 20px">'
             f'<div class="ok">✓</div><div style="font-size:24px;font-weight:600">Pâtisserie</div></div>'
             f'<div style="margin-top:8px;display:flex;align-items:center;gap:14px;padding:16px 18px;color:#9b9488">'
             f'<div class="ko">✕</div><div style="font-size:21px">Magasin d\'alimentation</div></div>'
             f'<div style="font-size:17px;color:{SABLE6};line-height:1.4;margin-top:8px">La plus précise&nbsp;: elle dit à Google sur quelles recherches vous montrer.</div></div>',
             "transform:rotate(-2deg)")
    x, y = ETAPES[3]
    zone = (f'<div style="position:absolute;z-index:2;left:{x - 230}px;top:{y - 190}px;width:460px;height:300px;border-radius:50%;'
            f'border:3px dashed {SAVANE};background:rgba(101,115,58,.10)"></div>')
    etq = (f'<div style="position:absolute;z-index:3;left:{x + 40}px;top:{y - 150}px;background:#fff;border-radius:12px;padding:8px 14px;'
           f'font-size:18px;font-weight:700;box-shadow:0 8px 18px rgba(42,24,16,.18)">④ Votre porte</div>')
    zchips = fl(x0 + 590, 1090, 400, f'<div style="padding:16px 20px 10px"><div class="lbl" style="margin-bottom:10px">Ou une zone de service</div>'
                f'<span class="chip">Dakar</span><span class="chip">Pikine</span><span class="chip">Rufisque</span></div>', "border-radius:24px 0 24px 0")
    return (texte(3, "③ et ④ Catégorie, adresse", "Le bon rayon,<br><em>la bonne porte</em>",
                  "« Derrière la station » ne passe pas sur Google. Placez l'épingle à la main, sur votre porte.")
            + zone + ondes(x, y - 20) + pin(x, y) + etq + cat + zchips + pied(3))


def d5():
    x0 = 4320

    def tuile(x, y, w, rot, titre, fond, motif):
        return (f'<div class="tile" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'
                f'<div class="img" style="height:{int(w * 0.72)}px;background:{fond}">{motif}</div><div class="cap">{titre}</div></div>')
    facade = ('<div style="position:absolute;left:20%;right:20%;top:24%;bottom:0;border:3px solid rgba(42,24,16,.35);border-bottom:none"></div>'
              '<div style="position:absolute;left:41%;right:41%;top:50%;bottom:0;background:rgba(42,24,16,.28)"></div>'
              f'<div style="position:absolute;left:24%;right:24%;top:12%;height:12%;background:{TERRA};opacity:.75;border-radius:3px"></div>')
    interieur = ('<div style="position:absolute;left:10%;right:10%;top:56%;height:10%;background:rgba(42,24,16,.28);border-radius:5px"></div>'
                 '<div style="position:absolute;left:16%;width:26%;top:18%;height:24%;background:rgba(255,255,255,.7);border-radius:5px"></div>'
                 '<div style="position:absolute;left:56%;width:26%;top:18%;height:24%;background:rgba(255,255,255,.7);border-radius:5px"></div>')
    real = "".join(f'<div style="position:absolute;left:{a}%;top:30%;width:20%;height:44%;background:rgba(255,255,255,.65);border-radius:8px"></div>' for a in (12, 40, 68))
    faux = (f'<div class="tile" style="left:{x0 + 700}px;top:960px;width:260px;transform:rotate(7deg);opacity:.92">'
            f'<div class="img" style="height:150px;background:repeating-linear-gradient(45deg,#ddd 0 14px,#eee 14px 28px)">'
            f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><div class="ko" style="width:64px;height:64px;font-size:34px">✕</div></div></div>'
            f'<div class="cap" style="color:#9b9488;text-decoration:line-through">Image d\'internet</div></div>')
    return (texte(4, "⑤ Les photos", "Montrez ce que<br><em>le client verra</em>",
                  "La façade de jour, l'intérieur, vos réalisations. Ajoutez-en de nouvelles de temps en temps.")
            + tuile(x0 + 80, 650, 330, -6, "La façade, de jour", "#F3DCC6", facade)
            + tuile(x0 + 370, 700, 330, 3, "L'intérieur", "#E5E8D6", interieur)
            + tuile(x0 + 640, 620, 320, -2, "Vos réalisations", "#FCEBDD", real)
            + faux + pied(4))


def d6():
    x0 = 5400
    chat = fl(x0 + 80, 620, 520,
              f'<div style="display:flex;align-items:center;gap:12px;padding:16px 22px;background:{SABLE1};border-bottom:1px solid #eee">'
              f'<div class="av" style="width:42px;height:42px;font-size:19px;background:{SAVANE}">C</div><div style="font-size:19px;font-weight:600">Un client satisfait</div></div>'
              f'<div style="padding:20px;display:flex;flex-direction:column;gap:12px">'
              f'<div class="bub">Merci, tout est parfait&nbsp;!</div>'
              f'<div class="bub me">Merci à vous&nbsp;! Un avis sur Google nous aiderait&nbsp;: <b style="color:{TERRA}">le lien de la fiche</b></div></div>',
              "transform:rotate(-2deg)")
    avis = fl(x0 + 200, 960, 470,
              f'<div style="padding:20px 24px"><div style="color:{OR};font-size:24px;letter-spacing:2px">★★★★★</div>'
              f'<div style="font-size:19px;margin-top:6px">« Travail soigné, je recommande. »</div>'
              f'<div style="margin-top:12px;padding:12px 16px;background:{SABLE1};border-radius:0 16px 0 16px;font-size:17px;color:{SABLE6}">'
              f'<b style="color:{CAFE}">Réponse du propriétaire</b> · Merci pour votre confiance&nbsp;!</div></div>',
              "transform:rotate(2deg)")
    mois = "".join(f'<div class="chk"><i>✓</i>{t}</div>' for t in
                   ("Une actualité ou une offre", "2 ou 3 photos récentes", "Répondre aux avis", "Vérifier les infos", "Lire les statistiques"))
    cal = fl(x0 + 640, 640, 360, f'<div style="padding:24px 26px"><div class="lbl">⑦ Chaque mois</div><div style="margin-top:10px">{mois}</div></div>',
             "border-radius:40px 0 40px 0;transform:rotate(3deg)")
    return (texte(5, "⑥ et ⑦ Avis, rendez-vous", "Demandez des avis,<br><em>répondez à tous</em>",
                  "Le lien de la fiche sur WhatsApp, après chaque client satisfait. Puis un petit rendez-vous chaque mois.")
            + chat + avis + cal + pied(5))


def d7():
    x0 = 6480
    blog = fl(x0 + 80, 700, 500,
              f'<div style="display:flex;align-items:center;gap:8px;padding:14px 18px;background:{SABLE1};border-bottom:1px solid #eee">'
              f'<i style="width:12px;height:12px;border-radius:50%;background:{TERRA}"></i><i style="width:12px;height:12px;border-radius:50%;background:{SAVANE}"></i>'
              f'<div style="margin-left:10px;flex:1;background:#fff;border-radius:999px;padding:8px 16px;font-size:17px;color:{SABLE6}">saibodanfakha.com/blog</div></div>'
              f'<div style="padding:26px 30px"><div style="font-size:15px;font-weight:700;letter-spacing:3px;color:{TERRA}">BLOG · 3 NOVEMBRE 2026</div>'
              f'<div style="font-family:Fraunces,serif;font-size:34px;font-weight:600;line-height:1.1;letter-spacing:-0.02em;margin-top:12px">Fiche Google Business&nbsp;: le guide pour une PME à Dakar</div>'
              f'<div style="font-size:18px;color:{SABLE6};margin-top:12px">9 étapes · gratuit · sans jargon</div></div>',
              "transform:rotate(-2deg)")
    px, py = x0 + 640, 600
    tel = (f'<div style="position:absolute;z-index:3;left:{px}px;top:{py}px;width:300px;height:560px;background:{CAFE};border-radius:46px;padding:14px;'
           f'box-shadow:0 50px 90px -20px rgba(42,24,16,.45);transform:rotate(5deg)">'
           f'<div style="background:#fff;height:100%;border-radius:34px;overflow:hidden">'
           f'<div style="height:150px;background:#EEF0E6;position:relative"><div style="position:absolute;left:44%;top:40px;width:40px;height:40px;background:{TERRA};'
           f'border-radius:50% 50% 50% 0;transform:rotate(-45deg)"></div></div>'
           f'<div style="padding:18px 20px"><div style="font-family:Fraunces,serif;font-size:24px;font-weight:600;line-height:1.15">Votre entreprise</div>'
           f'<div style="font-size:15px;color:{SABLE6};margin-top:6px"><span style="color:{OR}">★★★★★</span> · Pâtisserie · Ouvert</div>'
           f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:14px">'
           f'<div style="height:60px;background:#F3DCC6;border-radius:6px"></div><div style="height:60px;background:#E5E8D6;border-radius:6px"></div><div style="height:60px;background:#FCEBDD;border-radius:6px"></div></div>'
           f'<div style="margin-top:18px;background:{TERRA};color:{CREME};border-radius:999px;padding:14px;text-align:center;font-weight:700;font-size:19px">Appeler</div>'
           f'<div style="margin-top:10px;border:2px solid {SABLE3};border-radius:999px;padding:12px;text-align:center;font-weight:600;font-size:17px;color:{SABLE6}">Itinéraire</div>'
           f'</div></div></div>')
    return (texte(6, "Le guide complet", "Et le client<br><em>appelle</em>",
                  "Les 9 étapes en détail sur mon blog. Un avis sur votre fiche&nbsp;? Écrivez-moi en message.")
            + ondes(px + 150, py + 300, (420, 520, 620)) + blog + tel + pied(6, "LIEN EN BIO ↗"))


def html():
    corps = (carte_svg() + trajet_svg()
             + f'<div class="fade" style="top:0;height:{MAP_TOP + 140}px;background:linear-gradient({CREME} 72%,rgba(254,243,226,0))"></div>'
             + f'<div class="fade" style="top:{MAP_BOT - 110}px;bottom:0;background:linear-gradient(rgba(254,243,226,0),{CREME} 45%)"></div>'
             + "".join(f'<div class="ribbon" style="left:{k * 1080}px;right:auto;width:1080px"><i style="background:{CAFE}"></i><i style="background:{TERRA}"></i><i style="background:{SAVANE}"></i></div>' for k in range(N))
             + d1() + d2() + d3() + d4() + d5() + d6() + d7())
    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">{FONTS}<style>{CSS}</style></head>'
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
        # contrôle : un texte ne doit jamais passer d'une diapo à l'autre
        bad = await pg.evaluate("""() => [...document.querySelectorAll('.tx, .foot, .swipe')].map(e => {
            const r = e.getBoundingClientRect(); return [Math.floor(r.left / 1080), Math.floor((r.right - 1) / 1080), e.className] })
            .filter(a => a[0] !== a[1])""")
        print("textes à cheval sur deux diapos :", bad or "aucun")
        full = os.path.join(OUT_DIR, "_panorama.png")
        await pg.screenshot(path=full)
        await b.close()
    os.remove(path)
    im = Image.open(full)
    for i in range(N):
        im.crop((i * 1080, 0, (i + 1) * 1080, H)).save(os.path.join(OUT_DIR, f"Instagram-{i + 1:02d}.png"))
    small = im.resize((W // 4, H // 4))
    small.save(os.path.join(OUT_DIR, "_panorama-apercu.png"))
    print("[OK] 7 diapos +", full)


if __name__ == "__main__":
    asyncio.run(main())
