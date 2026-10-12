"""Generate les 7 slides Instagram + 7 slides WhatsApp pour l'article "Creer une boutique en ligne au Senegal".
Gabarit repris de generate_article7.py (style "dark warm + halos colores" valide par Saibo)."""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "visuels-boutique-en-ligne-png")
os.makedirs(OUT_DIR, exist_ok=True)

# Palette (identique au gabarit article 7)
CREME = "#FEF3E2"
CREME_SOFT = "#FAF6EE"
TERRACOTTA = "#C2410C"
MUTED = "#C9BBA5"
DARK_BASE = "#1A1410"
ACCENT_SOFT = "#E8915F"

GLOW_IG = ("radial-gradient(820px 620px at 90% -8%, rgba(194,65,12,0.30), transparent 60%), "
           "radial-gradient(700px 560px at -8% 112%, rgba(101,115,58,0.20), transparent 60%), "
           + DARK_BASE)
GLOW_WA = ("radial-gradient(900px 760px at 92% 4%, rgba(194,65,12,0.32), transparent 58%), "
           "radial-gradient(820px 700px at -10% 100%, rgba(101,115,58,0.20), transparent 60%), "
           + DARK_BASE)

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'

BADGE_DATE = "Blog · 21/07"

SLIDES = [
    {
        "type": "hero",
        "number": "13",
        "title": "Ce qui décide vraiment d'une boutique en ligne",
        "subtitle_main": "Créer une boutique en ligne au Sénégal",
        "subtitle_note": "Un guide par Saïbo Danfakha",
    },
    {
        "type": "error",
        "title": "CLÉ 1",
        "error_name": "LE PAIEMENT D'ABORD",
        "points": [
            "Au Sénégal, la carte n'est pas le réflexe",
            "Wave, Orange Money, paiement à la livraison",
            "Commencez simple, intégrez plus tard",
        ],
    },
    {
        "type": "error",
        "title": "CLÉ 2",
        "error_name": "LA LIVRAISON",
        "points": [
            "Zone assumée > zone promise et non tenue",
            "Qui livre, à quel prix, en combien de temps",
            "Un simple message WhatsApp suffit au début",
        ],
    },
    {
        "type": "error",
        "title": "CLÉ 3",
        "error_name": "LA CONFIANCE",
        "points": [
            "Payer d'avance un inconnu : ça se mérite",
            "Numéro visible, adresse, prix clairs",
            "De vraies photos, pas des visuels trouvés",
        ],
    },
    {
        "type": "error",
        "title": "CLÉ 4",
        "error_name": "LA VITESSE",
        "points": [
            "Vos clients sont sur mobile, souvent en 3G",
            "Un site lent = une vente perdue avant d'exister",
            "La performance se mesure en chiffre d'affaires",
        ],
    },
    {
        "type": "error",
        "title": "CLÉ 5",
        "error_name": "LE VRAI BUDGET",
        "points": [
            "Création + frais récurrents + votre temps",
            "Le temps est le poste le plus sous-estimé",
            "Méfiez-vous du prix donné sans questions",
        ],
    },
    {
        "type": "error",
        "title": "CLÉ 6",
        "error_name": "PAR OÙ COMMENCER",
        "points": [
            "Vos 20 meilleurs produits, pas les 400",
            "Paiement à la livraison + mobile money manuel",
            "Automatisez avec l'argent que ça rapporte",
        ],
    },
]


def build_instagram_slide(slide, idx, total):
    bg = GLOW_IG
    if slide["type"] == "hero":
        body_html = f"""
        <div class="badge">{BADGE_DATE}</div>
        <div class="content">
            <div class="number">{slide['number']}</div>
            <div class="title">{slide['title']}</div>
            <div class="subtitle-main">{slide['subtitle_main']}</div>
            <div class="subtitle-note">{slide['subtitle_note']}</div>
        </div>
        <div class="swipe">Swipe →</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    else:
        points_html = "".join([f"""
            <div class="point">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{TERRACOTTA}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>{p}</span>
            </div>""" for p in slide["points"]])
        body_html = f"""
        <div class="badge" style="background: {TERRACOTTA};">{slide['title']}</div>
        <div class="content content-error">
            <div class="error-name">{slide['error_name']}</div>
            <div class="points">{points_html}</div>
        </div>
        <div class="pagination">{idx}/{total}</div>
        <div class="brand">Saïbo Danfakha</div>
        """

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1080px; overflow: hidden; font-family: 'Inter', sans-serif; }}
.canvas {{ width: 1080px; height: 1080px; position: relative; background: {bg}; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 60px; }}
.badge {{ position: absolute; top: 60px; left: 60px; background: {TERRACOTTA}; color: {CREME}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ text-align: center; max-width: 900px; }}
.number {{ font-family: 'Fraunces', serif; font-size: 120px; font-weight: 600; color: {TERRACOTTA}; line-height: 1; margin-bottom: 20px; }}
.title {{ font-family: 'Fraunces', serif; font-size: 44px; font-weight: 600; color: {CREME}; line-height: 1.2; margin-bottom: 16px; letter-spacing: -0.02em; }}
.subtitle-main {{ font-size: 20px; color: {MUTED}; margin-bottom: 12px; font-weight: 500; }}
.subtitle-note {{ font-size: 14px; color: {MUTED}; font-style: italic; }}
.error-name {{ font-family: 'Fraunces', serif; font-size: 36px; font-weight: 600; color: {ACCENT_SOFT}; margin-bottom: 20px; letter-spacing: -0.02em; }}
.content-error {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
.points {{ display: flex; flex-direction: column; gap: 16px; align-items: center; }}
.point {{ display: flex; align-items: flex-start; gap: 12px; text-align: left; max-width: 800px; }}
.point span {{ font-size: 18px; color: {CREME}; line-height: 1.3; font-weight: 500; }}
.point svg {{ flex-shrink: 0; margin-top: 2px; }}
.swipe {{ position: absolute; bottom: 60px; left: 60px; font-size: 16px; color: {MUTED}; font-weight: 600; letter-spacing: 0.05em; }}
.pagination {{ position: absolute; bottom: 60px; left: 60px; font-size: 16px; color: {MUTED}; font-weight: 600; letter-spacing: 0.05em; }}
.brand {{ position: absolute; bottom: 60px; right: 60px; font-family: 'Fraunces', serif; font-size: 18px; font-weight: 600; color: {CREME}; letter-spacing: -0.02em; }}
</style></head>
<body><div class="canvas">{body_html}</div></body></html>"""


def build_whatsapp_slide(slide, idx, total):
    bg = GLOW_WA
    if slide["type"] == "hero":
        body_html = f"""
        <div class="badge">{BADGE_DATE}</div>
        <div class="content">
            <div class="number">{slide['number']}</div>
            <div class="title">{slide['title']}</div>
            <div class="subtitle-main">{slide['subtitle_main']}</div>
            <div class="subtitle-note">{slide['subtitle_note']}</div>
        </div>
        <div class="swipe">Swipe →</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    else:
        points_html = "".join([f"""
            <div class="point">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{TERRACOTTA}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>{p}</span>
            </div>""" for p in slide["points"]])
        body_html = f"""
        <div class="badge" style="background: {TERRACOTTA};">{slide['title']}</div>
        <div class="content content-error">
            <div class="error-name">{slide['error_name']}</div>
            <div class="points">{points_html}</div>
        </div>
        <div class="pagination">{idx}/{total}</div>
        <div class="brand">Saïbo</div>
        """

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; font-family: 'Inter', sans-serif; }}
.canvas {{ width: 1080px; height: 1920px; position: relative; background: {bg}; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 80px 60px; }}
.badge {{ position: absolute; top: 80px; left: 60px; background: {TERRACOTTA}; color: {CREME}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ text-align: center; max-width: 900px; }}
.number {{ font-family: 'Fraunces', serif; font-size: 160px; font-weight: 600; color: {TERRACOTTA}; line-height: 1; margin-bottom: 20px; }}
.title {{ font-family: 'Fraunces', serif; font-size: 52px; font-weight: 600; color: {CREME}; line-height: 1.2; margin-bottom: 16px; letter-spacing: -0.02em; }}
.subtitle-main {{ font-size: 24px; color: {CREME_SOFT}; margin-bottom: 12px; font-weight: 500; }}
.subtitle-note {{ font-size: 16px; color: {CREME_SOFT}; font-style: italic; }}
.error-name {{ font-family: 'Fraunces', serif; font-size: 44px; font-weight: 600; color: {ACCENT_SOFT}; margin-bottom: 24px; letter-spacing: -0.02em; }}
.content-error {{ display: flex; flex-direction: column; align-items: center; gap: 20px; }}
.points {{ display: flex; flex-direction: column; gap: 20px; align-items: center; }}
.point {{ display: flex; align-items: flex-start; gap: 16px; text-align: left; max-width: 900px; }}
.point span {{ font-size: 20px; color: {CREME}; line-height: 1.4; font-weight: 500; }}
.point svg {{ flex-shrink: 0; margin-top: 3px; }}
.swipe {{ position: absolute; bottom: 80px; left: 60px; font-size: 16px; color: {CREME_SOFT}; font-weight: 600; letter-spacing: 0.05em; }}
.pagination {{ position: absolute; bottom: 80px; left: 60px; font-size: 16px; color: {CREME_SOFT}; font-weight: 600; letter-spacing: 0.05em; }}
.brand {{ position: absolute; bottom: 80px; right: 60px; font-family: 'Fraunces', serif; font-size: 20px; font-weight: 600; color: {CREME}; letter-spacing: -0.02em; }}
</style></head>
<body><div class="canvas">{body_html}</div></body></html>"""


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for idx, slide in enumerate(SLIDES, start=1):
            ig_html = build_instagram_slide(slide, idx, len(SLIDES))
            ig_path = os.path.join(OUT_DIR, f"boutique-instagram-{idx:02d}.html")
            ig_png = os.path.join(OUT_DIR, f"Instagram 13-{idx:02d}.png")

            with open(ig_path, "w", encoding="utf-8") as f:
                f.write(ig_html)

            page = await browser.new_page(viewport={"width": 1080, "height": 1080})
            await page.goto(f"file:///{ig_path.replace(chr(92), '/')}")
            await page.screenshot(path=ig_png)
            await page.close()
            print(f"[OK] Instagram 13-{idx:02d}.png")

            wa_html = build_whatsapp_slide(slide, idx, len(SLIDES))
            wa_path = os.path.join(OUT_DIR, f"boutique-whatsapp-{idx:02d}.html")
            wa_png = os.path.join(OUT_DIR, f"Whatsapp 13-{idx:02d}.png")

            with open(wa_path, "w", encoding="utf-8") as f:
                f.write(wa_html)

            page = await browser.new_page(viewport={"width": 1080, "height": 1920})
            await page.goto(f"file:///{wa_path.replace(chr(92), '/')}")
            await page.screenshot(path=wa_png)
            await page.close()
            print(f"[OK] Whatsapp 13-{idx:02d}.png")

        await browser.close()
        print("\n[SUCCESS] Boutique en ligne - 14 slides generees (7 Instagram + 7 WhatsApp)")

if __name__ == "__main__":
    asyncio.run(main())
