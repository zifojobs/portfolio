"""Corrige le slide 1 (hero) de brief-client-10-questions : chevauchement titre/sous-titre
sur Instagram et LinkedIn + garantit le chargement des polices (Fraunces/Inter) avant capture."""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "visuels-brief-client-png")

CREME = "#FEF3E2"
CREME_SOFT = "#FAF6EE"
TERRACOTTA = "#C2410C"
MUTED = "#C9BBA5"
DARK_BASE = "#1A1410"

GLOW = ("radial-gradient(820px 620px at 90% -8%, rgba(194,65,12,0.30), transparent 60%), "
        "radial-gradient(700px 560px at -8% 112%, rgba(101,115,58,0.20), transparent 60%), "
        + DARK_BASE)

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'

BADGE_DATE = "Blog · 07/07"
NUMBER = "09"
TITLE = "Le brief qui décide tout"
SUBTITLE_MAIN = "10 questions avant de démarrer un site"
SUBTITLE_NOTE = "Un guide par Saïbo Danfakha"

# format: (nom, largeur, hauteur, dossier, fichier)
FORMATS = [
    ("instagram", 1080, 1080, "instagram-1080x1080", "01-ig-1-hero-1080x1080.png"),
    ("linkedin", 1080, 1350, "linkedin-1080x1350", "01-li-1-hero-1080x1350.png"),
    ("whatsapp", 1080, 1920, "whatsapp-1080x1920", "01-wa-1-hero-1080x1920.png"),
]


def build_hero_html(width, height):
    # tailles adaptees au format (mêmes proportions que le reste du set)
    if height <= 1080:
        number_size, title_size, sub_main_size, sub_note_size, badge_top = 120, 44, 20, 14, 60
    elif height <= 1350:
        number_size, title_size, sub_main_size, sub_note_size, badge_top = 130, 46, 21, 15, 70
    else:
        number_size, title_size, sub_main_size, sub_note_size, badge_top = 160, 52, 24, 16, 80

    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {width}px; height: {height}px; overflow: hidden; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }}
.canvas {{ width: {width}px; height: {height}px; position: relative; background: {GLOW}; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 60px; }}
.badge {{ position: absolute; top: {badge_top}px; left: 60px; border: 1px solid rgba(201,187,165,0.4); color: {MUTED}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ text-align: center; max-width: 900px; display: flex; flex-direction: column; align-items: center; gap: 28px; }}
.number {{ font-family: 'Fraunces', serif; font-size: {number_size}px; font-weight: 600; color: {TERRACOTTA}; line-height: 1; }}
.title-block {{ display: flex; flex-direction: column; gap: 20px; }}
.title {{ font-family: 'Fraunces', serif; font-size: {title_size}px; font-weight: 600; color: {CREME}; line-height: 1.35; letter-spacing: -0.02em; }}
.subtitle-main {{ font-family: 'Inter', sans-serif; font-size: {sub_main_size}px; color: {MUTED}; font-weight: 500; }}
.subtitle-note {{ font-family: 'Inter', sans-serif; font-size: {sub_note_size}px; color: {MUTED}; font-style: italic; }}
.brand {{ position: absolute; bottom: {badge_top}px; right: 60px; font-family: 'Fraunces', serif; font-size: 18px; font-weight: 600; color: {CREME}; letter-spacing: -0.02em; }}
</style></head>
<body><div class="canvas">
    <div class="badge">{BADGE_DATE}</div>
    <div class="content">
        <div class="number">{NUMBER}</div>
        <div class="title-block">
            <div class="title">{TITLE}</div>
            <div class="subtitle-main">{SUBTITLE_MAIN}</div>
        </div>
        <div class="subtitle-note">{SUBTITLE_NOTE}</div>
    </div>
    <div class="brand">Saïbo Danfakha</div>
</div></body></html>"""
    return html


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--disable-lcd-text", "--font-render-hinting=none", "--force-color-profile=srgb"])
        for name, width, height, folder, filename in FORMATS:
            html = build_hero_html(width, height)
            html_path = os.path.join(BASE_DIR, f"_tmp_hero_{name}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

            page = await browser.new_page(viewport={"width": width, "height": height})
            await page.goto(f"file:///{html_path.replace(chr(92), '/')}")
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(150)  # marge de securite apres fonts.ready
            out_path = os.path.join(OUT_DIR, folder, filename)
            await page.screenshot(path=out_path)
            await page.close()
            os.remove(html_path)
            print(f"[OK] {out_path}")

        await browser.close()
        print("\n[SUCCESS] Hero brief-client-10-questions corrige (3 formats)")

if __name__ == "__main__":
    asyncio.run(main())
