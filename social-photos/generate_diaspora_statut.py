"""Statut WhatsApp 1080x1920 du post 2 (article du 24/11/2026, faire créer son site au Sénégal depuis la France),
même style que generate_diaspora_panorama.py. Le format vertical permet une carte nord en haut : Paris en haut,
Dakar en bas, l'Atlantique à gauche. Texte du statut : SEO/posts/2026-11-24.md (post 2), le lien va sous l'image.
Usage : python generate_diaspora_statut.py  →  visuels-diaspora-panorama-png/Statut-WhatsApp.png"""
import asyncio
import math
import os

from playwright.async_api import async_playwright

import generate_fiche_gb_panorama as gb
import generate_diaspora_panorama as dp
from generate_fiche_gb_panorama import CAFE, CREME, TERRA, SAVANE, LOGO_URI

W, H = 1080, 1920
dp.W, dp.H = W, H

Y_PARIS, Y_DAKAR, X_PARIS = 800, 1640, 760
S = (Y_DAKAR - Y_PARIS) / (dp.PARIS[1] - dp.DAKAR[1])     # pixels par degré de latitude


def proj(lon, lat):
    return X_PARIS + (lon - dp.PARIS[0]) * dp.K * S, Y_PARIS + (dp.PARIS[1] - lat) * S


dp.proj = proj
XP, YP = proj(*dp.PARIS)
XD, YD = proj(*dp.DAKAR)

BIG = f"""html,body,.pano{{width:{W}px!important;height:{H}px!important}}
.tx{{top:190px}} .kick{{font-size:32px}} .trema i{{width:15px;height:15px}} h1{{font-size:104px}}
.sub{{font-size:40px;max-width:920px}} .foot img{{height:44px;width:calc(44px * {gb.LOGO_RATIO:.3f})}} .cta{{font-size:28px}}
.ville{{font-size:30px;padding:14px 28px}}"""


def trajet():
    cx, cy = (XP + XD) / 2 - 260, (YP + YD) / 2
    d = f"M{XP:.0f} {YP:.0f} Q {cx:.0f} {cy:.0f} {XD:.0f} {YD:.0f}"
    # l'avion au milieu de la courbe, tourné selon la tangente
    t = 0.5
    mx = (1 - t) ** 2 * XP + 2 * (1 - t) * t * cx + t ** 2 * XD
    my = (1 - t) ** 2 * YP + 2 * (1 - t) * t * cy + t ** 2 * YD
    tx, ty = 2 * (1 - t) * (cx - XP) + 2 * t * (XD - cx), 2 * (1 - t) * (cy - YP) + 2 * t * (YD - cy)
    ang = math.degrees(math.atan2(ty, tx))
    return (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;z-index:1"><path d="{d}" stroke="{TERRA}" stroke-width="8" '
            f'fill="none" stroke-dasharray="2 22" stroke-linecap="round"/></svg>' + dp.avion(mx, my, 90, ang)
            + dp.etiquette(mx + 70, my - 20, "4 205 km", rot=-3))


def corps():
    txt = (f'<div class="tx" style="left:80px"><div class="kick"><span class="trema"><i></i><i></i></span>Diaspora</div>'
           f'<h1>Tu es en France,<br><em>ton projet est au <span style="white-space:nowrap">Sénégal&nbsp;?</span></em></h1>'
           f'<p class="sub">Comment faire créer ton site à distance, sans mauvaise&nbsp;surprise.</p></div>')
    pied = f'<div class="foot" style="left:80px"><img src="{LOGO_URI}" alt="Saïbo Danfakha"><div class="cta">LIEN CI-DESSOUS ↓</div></div>'
    return (dp.carte_geo() + trajet()
            + dp.nom_px("FRANCE", XP + 60, YP + 130) + dp.nom_px("ESPAGNE", *proj(-3.5, 39.6)) + dp.nom_px("MAROC", *proj(-6.0, 31.6))
            + dp.nom_px("MAURITANIE", *proj(-10.5, 20.2)) + dp.nom_px("SÉNÉGAL", XD + 190, YD + 70)
            + dp.nom_px("Océan Atlantique", 200, 1010, 26)
            + f'<div class="fade" style="top:0;height:820px;background:linear-gradient({CREME} 78%,rgba(254,243,226,0))"></div>'
            + f'<div class="fade" style="top:1720px;bottom:0;background:linear-gradient(rgba(254,243,226,0),{CREME} 55%)"></div>'
            + f'<div class="ribbon"><i style="background:{CAFE}"></i><i style="background:{TERRA}"></i><i style="background:{SAVANE}"></i></div>'
            + txt
            + dp.tour_eiffel(XP + 190, YP + 120, 250) + dp.ondes(XP, YP - 20) + gb.pin(XP, YP) + dp.ville(XP - 60, YP + 50, "Paris")
            + dp.baobab(XD + 500, YD + 110, 200) + dp.pirogue(XD - 150, YD - 40, 220)
            + dp.ondes(XD, YD - 20) + gb.pin(XD, YD) + dp.ville(XD - 70, YD + 50, "Dakar", True)
            + pied)


async def main():
    path = os.path.join(dp.OUT_DIR, "_statut.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">{dp.r.FONTS}<style>{dp.CSS}{BIG}</style></head>'
                f'<body><div class="pano">{corps()}</div></body></html>')
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H})
        await pg.goto("file:///" + path.replace("\\", "/"), wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.screenshot(path=os.path.join(dp.OUT_DIR, "Statut-WhatsApp.png"))
        await b.close()
    os.remove(path)
    print("[OK] Statut-WhatsApp.png", round(XP), round(YP), round(XD), round(YD))


if __name__ == "__main__":
    asyncio.run(main())
