"""Generate les 6 slides Instagram + 6 slides WhatsApp pour l'article 5."""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Palette
CREME = "#FEF3E2"
CREME_SOFT = "#FAF6EE"
TERRACOTTA = "#C2410C"
NOIR_CAFE = "#2A1810"
NOIR_CAFE_DARK = "#3D2520"
SABLE_TEXT = "#7A6F5A"

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'

# Contenu des 6 slides
SLIDES = [
    {
        "type": "hero",
        "number": "05",
        "title": "5 erreurs fatales",
        "subtitle_main": "que les entreprises sénégalaises font avec leur site web",
        "subtitle_note": "Un guide par Saïbo Danfakha",
    },
    {
        "type": "error",
        "title": "ERREUR 1",
        "error_name": "TEMPLATE GÉNÉRIQUE",
        "points": [
            "Votre site ressemble à tous les autres",
            "Zéro différenciation, zéro mémoire",
            "Les clients ne cliquent pas",
        ],
    },
    {
        "type": "error",
        "title": "ERREUR 2",
        "error_name": "PAS DE CALL-TO-ACTION",
        "points": [
            "Les visiteurs ne savent pas quoi faire",
            "95% partent sans agir",
            "Vous perdez les leads",
        ],
    },
    {
        "type": "error",
        "title": "ERREUR 3",
        "error_name": "SITE LENT & NON-MOBILE",
        "points": [
            "8 secondes = départ garanti",
            "75% des recherches sur mobile",
            "La vitesse tue vos ventes",
        ],
    },
    {
        "type": "error",
        "title": "ERREUR 4",
        "error_name": "ZÉRO SEO LOCAL",
        "points": [
            "Google ne sait pas que vous existez",
            "Vos clients vous cherchent, Google non",
            "Zéro trafic organique",
        ],
    },
    {
        "type": "error",
        "title": "ERREUR 5",
        "error_name": "SITE MORT & JAMAIS MÀJ",
        "points": [
            "Pire qu'aucun site",
            "Prix, adresses, infos obsolètes",
            "Déconfiance totale",
        ],
    },
]


def build_instagram_slide(slide, idx, total):
    """1080x1080 - fond creme."""
    bg = f"linear-gradient(135deg, {CREME} 0%, {CREME_SOFT} 100%)"

    if slide["type"] == "hero":
        body_html = f"""
        <div class="badge">Blog · 05/06</div>
        <div class="content">
            <div class="number">{slide['number']}</div>
            <div class="title">{slide['title']}</div>
            <div class="subtitle-main">{slide['subtitle_main']}</div>
            <div class="subtitle-note">{slide['subtitle_note']}</div>
        </div>
        <div class="swipe">Swipe →</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    elif slide["type"] == "error":
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

    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1080px; overflow: hidden; font-family: 'Inter', sans-serif; }}
.canvas {{ width: 1080px; height: 1080px; position: relative; background: {bg}; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 60px; }}
.badge {{ position: absolute; top: 60px; left: 60px; background: {TERRACOTTA}; color: {CREME}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ text-align: center; max-width: 900px; }}
.number {{ font-family: 'Fraunces', serif; font-size: 120px; font-weight: 600; color: {TERRACOTTA}; line-height: 1; margin-bottom: 20px; }}
.title {{ font-family: 'Fraunces', serif; font-size: 44px; font-weight: 600; color: {NOIR_CAFE}; line-height: 1.2; margin-bottom: 16px; letter-spacing: -0.02em; }}
.subtitle-main {{ font-size: 20px; color: {SABLE_TEXT}; margin-bottom: 12px; font-weight: 500; }}
.subtitle-note {{ font-size: 14px; color: {SABLE_TEXT}; font-style: italic; }}
.error-name {{ font-family: 'Fraunces', serif; font-size: 36px; font-weight: 600; color: {NOIR_CAFE}; margin-bottom: 20px; letter-spacing: -0.02em; }}
.content-error {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
.points {{ display: flex; flex-direction: column; gap: 16px; align-items: center; }}
.point {{ display: flex; align-items: flex-start; gap: 12px; text-align: left; max-width: 800px; }}
.point span {{ font-size: 18px; color: {NOIR_CAFE}; line-height: 1.3; font-weight: 500; }}
.point svg {{ flex-shrink: 0; margin-top: 2px; }}
.swipe {{ position: absolute; bottom: 60px; left: 60px; font-size: 16px; color: {SABLE_TEXT}; font-weight: 600; letter-spacing: 0.05em; }}
.pagination {{ position: absolute; bottom: 60px; left: 60px; font-size: 16px; color: {SABLE_TEXT}; font-weight: 600; letter-spacing: 0.05em; }}
.brand {{ position: absolute; bottom: 60px; right: 60px; font-family: 'Fraunces', serif; font-size: 18px; font-weight: 600; color: {NOIR_CAFE}; letter-spacing: -0.02em; }}
</style></head>
<body><div class="canvas">{body_html}</div></body></html>"""
    return html


def build_whatsapp_slide(slide, idx, total):
    """1080x1920 - fond noir cafe."""
    bg = f"linear-gradient(180deg, {NOIR_CAFE} 0%, {NOIR_CAFE_DARK} 100%)"

    if slide["type"] == "hero":
        body_html = f"""
        <div class="badge">Blog · 05/06</div>
        <div class="content">
            <div class="number">{slide['number']}</div>
            <div class="title">{slide['title']}</div>
            <div class="subtitle-main">{slide['subtitle_main']}</div>
            <div class="subtitle-note">{slide['subtitle_note']}</div>
        </div>
        <div class="swipe">Swipe →</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    elif slide["type"] == "error":
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

    html = f"""<!DOCTYPE html>
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
.error-name {{ font-family: 'Fraunces', serif; font-size: 44px; font-weight: 600; color: {CREME}; margin-bottom: 24px; letter-spacing: -0.02em; }}
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
    return html


async def main():
    """Generate les 12 HTML et convertit en PNG."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for idx, slide in enumerate(SLIDES, start=1):
            # Instagram (1080x1080)
            ig_html = build_instagram_slide(slide, idx, len(SLIDES))
            ig_path = os.path.join(BASE_DIR, f"article5-instagram-{idx:02d}.html")
            ig_png = os.path.join(BASE_DIR, f"Instagram 05-{idx:02d}.png")

            with open(ig_path, "w", encoding="utf-8") as f:
                f.write(ig_html)

            page = await browser.new_page(viewport={"width": 1080, "height": 1080})
            await page.goto(f"file:///{ig_path.replace(chr(92), '/')}")
            await page.screenshot(path=ig_png)
            await page.close()
            print(f"[OK] Instagram 05-{idx:02d}.png")

            # WhatsApp (1080x1920)
            wa_html = build_whatsapp_slide(slide, idx, len(SLIDES))
            wa_path = os.path.join(BASE_DIR, f"article5-whatsapp-{idx:02d}.html")
            wa_png = os.path.join(BASE_DIR, f"Whatsapp 05-{idx:02d}.png")

            with open(wa_path, "w", encoding="utf-8") as f:
                f.write(wa_html)

            page = await browser.new_page(viewport={"width": 1080, "height": 1920})
            await page.goto(f"file:///{wa_path.replace(chr(92), '/')}")
            await page.screenshot(path=wa_png)
            await page.close()
            print(f"[OK] Whatsapp 05-{idx:02d}.png")

        await browser.close()
        print("\n[SUCCESS] Article 5 - 12 slides generees (6 Instagram + 6 WhatsApp)")

if __name__ == "__main__":
    asyncio.run(main())
