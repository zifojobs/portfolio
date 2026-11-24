"""Post 2 de l'article du 17/11/2026 (Site web pour restaurant à Dakar) — skill visuel-projet.
Demande de Saïbo (19/11) : l'esprit et les couleurs du panorama de la fiche Google (crème, noir café, terracotta,
savane ; carte dessinée continue, trajet en pointillés, écrans qui flottent), MAIS la police du nouveau style du
portfolio (Schibsted Grotesk seule). Aucune photo, aucune personne. Jamais le vert de WhatsApp.
Textes : SEO/posts/2026-11-17.md (Post 2) et l'article. Aucun prix inventé (barres grises).
Usage : python generate_restaurant_panorama.py  →  visuels-restaurant-panorama-png/Instagram-01..07.png"""
import asyncio
import os

from PIL import Image
from playwright.async_api import async_playwright

import generate_fiche_gb_panorama as gb
from generate_fiche_gb_panorama import (CAFE, CREME, SABLE1, SABLE3, SABLE6, TERRA, SAVANE, SEARCH, OR, N, W, H,
                                        MAP_TOP, MAP_BOT, fl, pin, ondes, pied)

OUT_DIR = os.path.join(gb.base.BASE_DIR, "visuels-restaurant-panorama-png")
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&display=swap" '
         'rel="stylesheet">')
CSS = gb.CSS + f"""
html,body{{font-family:'Schibsted Grotesk',sans-serif}}
h1{{font-family:'Schibsted Grotesk',sans-serif;font-weight:800;letter-spacing:-0.025em;line-height:1.02;font-size:94px}}
h1 em{{font-style:normal;font-weight:800;color:{TERRA}}}
.kick{{letter-spacing:0;text-transform:none;font-size:25px;font-weight:600}}
.lbl{{letter-spacing:0;text-transform:none;font-size:17px;font-weight:600}}
.av{{font-family:'Schibsted Grotesk',sans-serif}}
.cta,.swipe{{letter-spacing:.5px}}
.bar{{display:inline-block;height:14px;border-radius:7px;background:#e6e1d8}}
.plat{{display:flex;justify-content:space-between;align-items:center;padding:15px 0;border-bottom:1px solid #eee;font-size:23px;font-weight:500}}
"""

# trajet : de la recherche (diapo 1) jusqu'au restaurant (diapo 7)
gb.ETAPES = [(820, 960), (1080 + 760, 1000), (2160 + 820, 880), (3240 + 860, 1010), (4320 + 880, 1060),
             (5400 + 760, 1080), (6480 + 300, 1000)]
E = gb.ETAPES


def texte(i, kick, titre, sub, taille=94):
    x = i * 1080 + 80
    return (f'<div class="tx" style="left:{x}px"><div class="kick"><span class="trema"><i></i><i></i></span>{kick}</div>'
            f'<h1 style="font-size:{taille}px">{titre}</h1><p class="sub">{sub}</p></div>')


def bar(w):
    return f'<i class="bar" style="width:{w}px"></i>'


def navig(url):
    return (f'<div style="display:flex;align-items:center;gap:8px;padding:14px 18px;background:{SABLE1};border-bottom:1px solid #eee">'
            f'<i style="width:12px;height:12px;border-radius:50%;background:{TERRA}"></i><i style="width:12px;height:12px;border-radius:50%;background:{SAVANE}"></i>'
            f'<div style="margin-left:10px;flex:1;background:#fff;border-radius:999px;padding:8px 16px;font-size:17px;color:{SABLE6}">{url}</div></div>')


def d1():
    rech = fl(80, 610, 640,
              f'<div style="padding:22px 24px 12px"><div class="gbar">{SEARCH}<span>restaurant ouvert Plateau</span></div></div>'
              + "".join(f'<div class="row"><div style="flex:1"><div class="skel" style="width:{a}%;height:17px"></div>'
                        f'<div class="skel" style="width:{b}%;margin-top:10px"></div></div>'
                        f'<div class="ok" style="background:#c9c4ba">{k}</div></div>' for k, a, b in ((1, 58, 84), (2, 50, 76), (3, 62, 70))),
              "transform:rotate(-2deg)")
    x, y = E[0]
    montre = (f'<div style="position:absolute;z-index:3;left:{x - 40}px;top:{y - 250}px;width:190px;height:190px;border-radius:50%;'
              f'background:#fff;border:8px solid {CAFE};box-shadow:0 30px 60px -12px rgba(42,24,16,.35);display:flex;flex-direction:column;'
              f'align-items:center;justify-content:center"><div style="font-size:46px;font-weight:800;letter-spacing:-.02em">13:00</div>'
              f'<div style="font-size:17px;line-height:1.15;text-align:center;color:{TERRA};font-weight:700">1 minute<br>pour choisir</div></div>')
    return (texte(0, "Guide · site de restaurant", 'Ton client trouve-t-il<br><em>ce qu\'il <span style="white-space:nowrap">cherche&nbsp;?</span></em>',
                  "Ton restaurant a un site. Voici ce qu'il doit contenir, dans l'ordre d'importance.", 90)
            + pin(300, 1110, True) + pin(560, 1150, True) + rech + montre
            + '<div class="swipe" style="left:780px;top:1170px">GLISSE →</div>' + pied(0))


def d2():
    x0 = 1080
    pdf = fl(x0 + 110, 600, 340,
             f'<div style="height:250px;background:repeating-linear-gradient(0deg,#f3efe8 0 22px,#ebe5da 22px 26px);position:relative">'
             f'<div style="position:absolute;left:22px;top:22px;background:{CAFE};color:{CREME};font-weight:800;font-size:22px;padding:6px 14px;border-radius:6px">PDF</div>'
             f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><div class="ko" style="width:76px;height:76px;font-size:40px">✕</div></div></div>'
             f'<div style="padding:14px 20px;font-size:19px;color:#9b9488;text-decoration:line-through">carte-menu-scan.pdf · 8 Mo</div>',
             "transform:rotate(-6deg);opacity:.92")
    plats = "".join(f'<div class="plat">{p}{bar(80)}</div>' for p in ("Thiéboudienne", "Yassa poulet", "Mafé", "Jus de bissap"))
    menu = fl(x0 + 400, 690, 540,
              f'<div style="padding:24px 30px 18px"><div class="lbl">① Le menu, en texte</div>'
              f'<div style="font-size:34px;font-weight:800;letter-spacing:-.02em;margin-top:8px">Menu du jour</div>{plats}'
              f'<div style="display:flex;align-items:center;gap:12px;margin-top:16px"><div class="ok">✓</div>'
              f'<span style="font-size:19px;color:{SABLE6}">Se lit sur téléphone, sans zoomer</span></div></div>',
              "transform:rotate(2deg)")
    return (texte(1, "① Le menu", "Le menu en texte,<br><em>avec les prix</em>",
                  "Pas un PDF, pas une photo de la carte. Google le lit, ton client aussi.")
            + pdf + menu + pied(1))


def d3():
    x0 = 2160
    jours = "".join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:9px 0;font-size:21px'
                    f'{";font-weight:700;color:" + TERRA if j == "Jeudi" else ""}"><span>{j}</span>{bar(150 if j != "Lundi" else 90)}</div>'
                    for j in ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"))
    horaires = fl(x0 + 80, 600, 400,
                  f'<div style="padding:24px 28px"><div class="lbl">② Les horaires, jour par jour</div><div style="margin-top:8px">{jours}</div></div>',
                  "transform:rotate(-2deg)")
    x, y = E[2]
    adresse = fl(x0 + 560, 1010, 420,
                 f'<div style="padding:20px 24px"><div class="lbl">L\'adresse, avec des repères</div>'
                 f'<div style="font-size:21px;margin-top:8px;line-height:1.35">{bar(300)}<br>{bar(220)}</div>'
                 f'<div style="margin-top:16px"><span class="btn">Itinéraire →</span></div></div>',
                 "border-radius:24px 0 24px 0;transform:rotate(2deg)")
    return (texte(2, "② Horaires et adresse", "Les horaires exacts,<br><em>la bonne adresse</em>",
                  "Jour par jour. Puis l'adresse avec des repères et un bouton «&nbsp;Itinéraire&nbsp;».")
            + horaires + ondes(x, y - 20) + pin(x, y) + adresse + pied(2))


def telephone(px, py, rot, contenu, h=640):
    return (f'<div style="position:absolute;z-index:3;left:{px}px;top:{py}px;width:340px;height:{h}px;background:{CAFE};border-radius:50px;padding:14px;'
            f'box-shadow:0 50px 90px -20px rgba(42,24,16,.45);transform:rotate({rot}deg)">'
            f'<div style="background:#fff;height:100%;border-radius:38px;overflow:hidden;position:relative">{contenu}</div></div>')


def d4():
    x0 = 3240
    page = (f'<div style="padding:34px 24px 0"><div style="font-size:27px;font-weight:800;letter-spacing:-.02em">Ton restaurant</div>'
            f'<div style="font-size:16px;color:{SAVANE};font-weight:700;margin-top:4px">Ouvert maintenant</div>'
            + "".join(f'<div class="skel" style="width:{w}%;margin-top:14px"></div>' for w in (90, 76, 84))
            + f'<div style="height:150px;border-radius:14px;background:#F3DCC6;margin-top:20px"></div>'
            + "".join(f'<div class="skel" style="width:{w}%;margin-top:14px"></div>' for w in (80, 64)) + '</div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0;padding:16px;display:flex;gap:10px;background:#fff;border-top:1px solid #eee">'
            f'<div style="flex:1;background:{TERRA};color:{CREME};border-radius:999px;padding:15px 0;text-align:center;font-weight:700;font-size:19px">Appeler</div>'
            f'<div style="flex:1;border:2.5px solid {CAFE};border-radius:999px;padding:13px 0;text-align:center;font-weight:700;font-size:19px">WhatsApp</div></div>')
    pouce = fl(x0 + 80, 760, 380,
               f'<div style="padding:22px 26px"><div class="lbl">③ À portée de pouce</div>'
               f'<div class="chk"><i>✓</i>Sur chaque page</div><div class="chk"><i>✓</i>Fixés en bas de l\'écran</div>'
               f'<div class="chk"><i>✓</i>Un toucher, l\'appel part</div></div>',
               "border-radius:40px 0 40px 0;transform:rotate(-3deg)")
    return (texte(3, "③ Les boutons", "Appeler, WhatsApp&nbsp;:<br><em>toujours visibles</em>",
                  "Deux boutons, sur chaque page. Ton client ne doit jamais chercher ton numéro.")
            + pouce + telephone(x0 + 570, 560, 4, page, 590) + pied(3))


def d5():
    x0 = 4320

    def assiette(couleurs):
        c1, c2, c3 = couleurs
        return (f'<div style="position:absolute;left:50%;top:50%;width:150px;height:150px;margin:-75px 0 0 -75px;border-radius:50%;background:#fff;'
                f'box-shadow:0 8px 18px rgba(42,24,16,.15)"><div style="position:absolute;inset:22px;border-radius:50%;background:{c1}"></div>'
                f'<div style="position:absolute;left:44px;top:40px;width:40px;height:30px;border-radius:50%;background:{c2}"></div>'
                f'<div style="position:absolute;left:76px;top:74px;width:34px;height:26px;border-radius:50%;background:{c3}"></div></div>')

    def tuile(x, y, w, rot, titre, fond, motif):
        return (f'<div class="tile" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'
                f'<div class="img" style="height:{int(w * 0.72)}px;background:{fond}">{motif}</div><div class="cap">{titre}</div></div>')
    salle = ('<div style="position:absolute;left:10%;right:10%;top:58%;height:9%;background:rgba(42,24,16,.28);border-radius:5px"></div>'
             + "".join(f'<div style="position:absolute;left:{a}%;top:20%;width:14%;height:30%;background:rgba(255,255,255,.7);border-radius:50% 50% 6px 6px"></div>' for a in (16, 43, 70)))
    poids = (f'<div style="position:absolute;z-index:4;left:{x0 + 720}px;top:1040px;background:{SAVANE};color:{CREME};border-radius:999px;'
             f'padding:14px 24px;font-size:20px;font-weight:700;box-shadow:0 16px 30px -8px rgba(42,24,16,.35);transform:rotate(-4deg)">Allégées pour le téléphone</div>')
    return (texte(4, "④ Les photos", "De vraies photos<br><em>de tes plats</em>",
                  "Et de ta salle. Tes vrais plats, pas des images d'internet.")
            + tuile(x0 + 80, 640, 320, -6, "Ton plat du jour", "#F3DCC6", assiette(("#E4A25A", "#C2410C", "#65733A")))
            + tuile(x0 + 370, 700, 320, 3, "Ta salle", "#E5E8D6", salle)
            + tuile(x0 + 650, 610, 310, -2, "Tes desserts", "#FCEBDD", assiette(("#F1D9B5", "#B3261E", "#E8A33A")))
            + poids + pied(4))


def d6():
    x0 = 5400
    chat = fl(x0 + 80, 620, 520,
              f'<div style="display:flex;align-items:center;gap:12px;padding:16px 22px;background:{SABLE1};border-bottom:1px solid #eee">'
              f'<div class="av" style="width:42px;height:42px;font-size:19px;background:{SAVANE}">C</div><div style="font-size:19px;font-weight:600">Un client</div></div>'
              f'<div style="padding:20px;display:flex;flex-direction:column;gap:12px">'
              f'<div class="bub">Bonjour, une table pour 4 ce soir&nbsp;?</div>'
              f'<div class="bub me">Oui, c\'est noté&nbsp;! <b style="color:{TERRA}">20 h, à votre nom</b></div></div>',
              "transform:rotate(-2deg)")
    modes = fl(x0 + 640, 640, 340,
               f'<div style="padding:22px 24px 14px"><div class="lbl" style="margin-bottom:12px">⑤ Selon ta façon de travailler</div>'
               f'<span class="chip">Commande</span><span class="chip">Livraison</span><span class="chip">Réservation</span></div>',
               "border-radius:24px 0 24px 0;transform:rotate(3deg)")
    avis = fl(x0 + 220, 980, 480,
              f'<div style="padding:20px 24px"><div style="color:{OR};font-size:24px;letter-spacing:2px">★★★★★</div>'
              f'<div style="font-size:20px;margin-top:6px">« Le menu est clair, j\'ai réservé en deux minutes. »</div>'
              f'<div style="margin-top:12px;padding:12px 16px;background:{SABLE1};border-radius:0 16px 0 16px;font-size:17px;color:{SABLE6}">'
              f'<b style="color:{CAFE}">Ta fiche Google</b> · les avis à côté de ton site</div></div>',
              "transform:rotate(2deg)")
    return (texte(5, "⑤ Commander, réserver", "Commande, livraison<br><em>ou réservation</em>",
                  "Ce que tu proposes vraiment, pas plus. Puis les avis, avec ta fiche Google.", 86)
            + chat + modes + avis + pied(5))


def d7():
    x0 = 6480
    blog = fl(x0 + 80, 700, 500,
              navig("saibodanfakha.com/blog")
              + f'<div style="padding:26px 30px"><div style="font-size:16px;font-weight:700;color:{TERRA}">Blog · 17 novembre 2026</div>'
              f'<div style="font-size:35px;font-weight:800;line-height:1.08;letter-spacing:-0.02em;margin-top:12px">Site web pour restaurant à Dakar&nbsp;: ce qu\'il doit contenir</div>'
              f'<div style="font-size:18px;color:{SABLE6};margin-top:12px">La liste, dans l\'ordre d\'importance</div></div>',
              "transform:rotate(-2deg)")
    px, py = x0 + 640, 600
    page = (f'<div style="height:150px;background:#F3DCC6;position:relative"><div style="position:absolute;left:44%;top:40px;width:40px;height:40px;background:{TERRA};'
            f'border-radius:50% 50% 50% 0;transform:rotate(-45deg)"></div></div>'
            f'<div style="padding:18px 20px"><div style="font-size:25px;font-weight:800;line-height:1.15">Ton restaurant</div>'
            f'<div style="font-size:15px;color:{SABLE6};margin-top:6px"><span style="color:{OR}">★★★★★</span> · Ouvert</div>'
            f'<div style="margin-top:14px">' + "".join(f'<div class="plat" style="font-size:17px;padding:9px 0">{p}{bar(50)}</div>' for p in ("Thiéboudienne", "Yassa", "Mafé")) + '</div>'
            f'<div style="margin-top:16px;background:{TERRA};color:{CREME};border-radius:999px;padding:14px;text-align:center;font-weight:700;font-size:19px">Appeler</div></div>')
    return (texte(6, "La liste complète", "Ton menu se lit<br><em>sur téléphone&nbsp;?</em>",
                  "Tout est dans l'article, lien en bio. Un avis sur le site de ton restaurant&nbsp;? Écris-moi.")
            + ondes(px + 170, py + 300, (420, 520, 620)) + blog + telephone(px - 20, py, 5, page, 580) + pied(6, "LIEN EN BIO ↗"))


def html():
    corps = (gb.carte_svg() + gb.trajet_svg()
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
        bad = await pg.evaluate("""() => [...document.querySelectorAll('.tx, .foot, .swipe, .fl, .tile')].map(e => {
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
