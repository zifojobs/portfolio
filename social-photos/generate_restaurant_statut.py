"""Statut WhatsApp 1080x1920 du post 2 (article du 17/11/2026, site web pour restaurant à Dakar), même style que le
carrousel generate_restaurant_panorama.py (couleurs de la fiche Google, police Schibsted Grotesk, aucune photo) :
le menu en PDF barré et, au bout du trajet, le téléphone avec le menu lisible et les boutons.
Texte du statut : SEO/posts/2026-11-17.md (post 2), le lien va sous l'image.
Usage : python generate_restaurant_statut.py  →  visuels-restaurant-panorama-png/Statut-WhatsApp.png"""
import asyncio
import os

from playwright.async_api import async_playwright

import generate_fiche_gb_panorama as gb
import generate_restaurant_panorama as r
from generate_fiche_gb_panorama import CAFE, CREME, SABLE3, SABLE6, TERRA, SAVANE, OR, LOGO_URI

W, H = 1080, 1920
gb.W, gb.H, gb.MAP_TOP, gb.MAP_BOT = W, H, 760, 1700

BIG = f"""html,body,.pano{{width:{W}px!important;height:{H}px!important}}
.tx{{top:190px}} .kick{{font-size:32px}} .trema i{{width:15px;height:15px}} h1{{font-size:112px}}
.sub{{font-size:40px;max-width:920px}} .foot img{{height:44px;width:calc(44px * {gb.LOGO_RATIO:.3f})}} .cta{{font-size:28px}}
.plat{{font-size:23px}}"""


def telephone(px, py):
    plats = "".join(f'<div class="plat">{p}{r.bar(60)}</div>' for p in ("Thiéboudienne", "Yassa poulet", "Mafé", "Jus de bissap"))
    page = (f'<div style="padding:40px 28px 0"><div style="font-size:34px;font-weight:800;letter-spacing:-.02em">Ton restaurant</div>'
            f'<div style="font-size:19px;color:{SAVANE};font-weight:700;margin-top:6px">Ouvert maintenant · <span style="color:{OR}">★★★★★</span></div>'
            f'<div style="font-size:24px;font-weight:800;margin-top:26px">Menu</div>{plats}</div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0;padding:18px;display:flex;gap:10px;background:#fff;border-top:1px solid #eee">'
            f'<div style="flex:1;background:{TERRA};color:{CREME};border-radius:999px;padding:17px 0;text-align:center;font-weight:700;font-size:22px">Appeler</div>'
            f'<div style="flex:1;border:2.5px solid {CAFE};border-radius:999px;padding:15px 0;text-align:center;font-weight:700;font-size:22px">WhatsApp</div></div>')
    return (f'<div style="position:absolute;z-index:3;left:{px}px;top:{py}px;width:420px;height:760px;background:{CAFE};border-radius:58px;padding:16px;'
            f'box-shadow:0 60px 110px -20px rgba(42,24,16,.45);transform:rotate(5deg)">'
            f'<div style="background:#fff;height:100%;border-radius:44px;overflow:hidden;position:relative">{page}</div></div>')


def corps():
    pdf = gb.fl(80, 880, 400,
                f'<div style="height:300px;background:repeating-linear-gradient(0deg,#f3efe8 0 24px,#ebe5da 24px 28px);position:relative">'
                f'<div style="position:absolute;left:24px;top:24px;background:{CAFE};color:{CREME};font-weight:800;font-size:26px;padding:7px 16px;border-radius:6px">PDF</div>'
                f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><div class="ko" style="width:90px;height:90px;font-size:46px">✕</div></div></div>'
                f'<div style="padding:16px 22px;font-size:22px;color:#9b9488;text-decoration:line-through">carte-menu-scan.pdf</div>',
                "transform:rotate(-5deg);opacity:.92")
    trajet = (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0;z-index:1"><path d="M280 1300 C 320 1560, 480 1600, 600 1480" '
              f'stroke="{TERRA}" stroke-width="7" fill="none" stroke-dasharray="2 20" stroke-linecap="round"/></svg>')
    pied = f'<div class="foot" style="left:80px"><img src="{LOGO_URI}" alt="Saïbo Danfakha"><div class="cta">LIEN CI-DESSOUS ↓</div></div>'
    txt = (f'<div class="tx" style="left:80px"><div class="kick"><span class="trema"><i></i><i></i></span>Restaurateurs</div>'
           f'<h1>Ton menu se lit<br><em>sur <span style="white-space:nowrap">téléphone&nbsp;?</span></em></h1>'
           f'<p class="sub">Ce que ton site de restaurant doit&nbsp;contenir.</p></div>')
    return (gb.carte_svg() + trajet
            + f'<div class="fade" style="top:0;height:900px;background:linear-gradient({CREME} 75%,rgba(254,243,226,0))"></div>'
            + f'<div class="fade" style="top:1600px;bottom:0;background:linear-gradient(rgba(254,243,226,0),{CREME} 45%)"></div>'
            + f'<div class="ribbon"><i style="background:{CAFE}"></i><i style="background:{TERRA}"></i><i style="background:{SAVANE}"></i></div>'
            + txt + gb.ondes(790, 1340, (480, 600, 720)) + pdf + telephone(570, 860) + pied)


async def main():
    path = os.path.join(r.OUT_DIR, "_statut.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">{r.FONTS}<style>{r.CSS}{BIG}</style></head>'
                f'<body><div class="pano">{corps()}</div></body></html>')
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H})
        await pg.goto("file:///" + path.replace("\\", "/"), wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.screenshot(path=os.path.join(r.OUT_DIR, "Statut-WhatsApp.png"))
        await b.close()
    os.remove(path)
    print("[OK] Statut-WhatsApp.png")


if __name__ == "__main__":
    asyncio.run(main())
