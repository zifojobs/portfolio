"""Genere l'ensemble des visuels sociaux pour l'article brief-client-10-questions :
Instagram (1080x1080), LinkedIn (1080x1350), WhatsApp (1080x1920).
Corrige le chevauchement titre/sous-titre du hero et garantit le chargement des polices
(Fraunces/Inter) avant chaque capture pour eviter tout rendu de police incoherent."""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "visuels-brief-client-png")

CREME = "#FEF3E2"
TERRACOTTA = "#C2410C"
ACCENT_SOFT = "#E8915F"
MUTED = "#C9BBA5"
DARK_BASE = "#1A1410"

GLOW = ("radial-gradient(820px 620px at 90% -8%, rgba(194,65,12,0.30), transparent 60%), "
        "radial-gradient(700px 560px at -8% 112%, rgba(101,115,58,0.20), transparent 60%), "
        + DARK_BASE)

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
BADGE_DATE = "Blog · 07/07"
BRAND = "Saïbo Danfakha"

# Contenu par slide : texte propre a chaque format (IG/WhatsApp partagent la meme
# formulation ; LinkedIn a sa propre formulation deja validee).
CATEGORY_SLIDES = [
    {
        "cat": "CATÉGORIE 1 / 4 · QUESTIONS 1 À 3",
        "title": "Objectif",
        "items_default": [("01", "Quel est l'objectif n°1 du site ?"), ("02", "Comment saurez-vous qu'il a réussi ?"), ("03", "Que doit faire le visiteur en arrivant ?")],
        "items_linkedin": [("01", "Quel est l'objectif prioritaire du site ?"), ("02", "À quels indicateurs mesurerez-vous sa réussite ?"), ("03", "Quelle action le visiteur doit-il accomplir ?")],
    },
    {
        "cat": "CATÉGORIE 2 / 4 · QUESTIONS 4 À 5",
        "title": "Audience",
        "items_default": [("04", "Qui est votre client idéal, précisément ?"), ("05", "Quels sites admirez-vous, et pourquoi ?")],
        "items_linkedin": [("04", "Quel est le profil précis de votre client cible ?"), ("05", "Quelles références appréciez-vous, et pourquoi ?")],
    },
    {
        "cat": "CATÉGORIE 3 / 4 · QUESTIONS 6 À 7",
        "title": "Matière",
        "items_default": [("06", "Qu'avez-vous déjà, et que faut-il créer ?"), ("07", "Qui gère le contenu après la mise en ligne ?")],
        "items_linkedin": [("06", "Quels contenus existent, lesquels sont à produire ?"), ("07", "Qui assurera la gestion du contenu après le lancement ?")],
    },
    {
        "cat": "CATÉGORIE 4 / 4 · QUESTIONS 8 À 10",
        "title": "Cadre",
        "items_default": [("08", "Quel est votre budget réel, et pour quand ?"), ("09", "Comment vos clients contactent et paient-ils ?"), ("10", "Que se passe-t-il après la mise en ligne ?")],
        "items_linkedin": [("08", "Quel budget et quelle échéance sont fixés ?"), ("09", "Comment vos clients vous contactent-ils et règlent-ils ?"), ("10", "Quel accompagnement après la mise en ligne ?")],
    },
]

CTA_DEFAULT = ("Le brief, c'est déjà", "la moitié du travail.")
CTA_LINKEDIN = ("Un brief solide, c'est", "la moitié du projet.")

# format: (nom, largeur, hauteur, dossier, prefixe_fichier, badge_top, cat_font, title_font,
#          num_font, item_font, item_gap, content_top)
FORMATS = {
    "instagram": dict(width=1080, height=1080, folder="instagram-1080x1080", prefix="ig",
                       badge_top=60, cat_font=20, title_font=64, num_font=26, item_font=30,
                       item_gap=68, content_top=290, cta_title_font=46, check_size=64),
    "linkedin": dict(width=1080, height=1350, folder="linkedin-1080x1350", prefix="li",
                      badge_top=70, cat_font=21, title_font=68, num_font=27, item_font=32,
                      item_gap=78, content_top=370, cta_title_font=50, check_size=68),
    "whatsapp": dict(width=1080, height=1920, folder="whatsapp-1080x1920", prefix="wa",
                      badge_top=80, cat_font=24, title_font=80, num_font=32, item_font=36,
                      item_gap=96, content_top=580, cta_title_font=58, check_size=76),
}


def build_category_html(fmt, slide, items):
    width, height = fmt["width"], fmt["height"]
    rows_html = "".join(f"""
        <div class="row">
            <div class="num">{n}</div>
            <div class="q">{q}</div>
        </div>
        <div class="sep"></div>""" for n, q in items)

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {width}px; height: {height}px; overflow: hidden; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }}
.canvas {{ width: {width}px; height: {height}px; position: relative; background: {GLOW}; }}
.badge {{ position: absolute; top: {fmt['badge_top']}px; left: 60px; border: 1px solid rgba(201,187,165,0.4); color: {MUTED}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ position: absolute; top: {fmt['content_top']}px; left: 60px; right: 60px; }}
.cat {{ font-size: {fmt['cat_font']}px; color: {TERRACOTTA}; font-weight: 600; letter-spacing: 0.15em; margin-bottom: 14px; }}
.title {{ font-family: 'Fraunces', serif; font-size: {fmt['title_font']}px; font-weight: 700; color: {CREME}; letter-spacing: -0.02em; margin-bottom: 36px; }}
.sep {{ height: 1px; background: rgba(201,187,165,0.25); }}
.row {{ display: flex; align-items: flex-start; gap: 32px; padding: {fmt['item_gap']//2}px 0; }}
.num {{ font-family: 'Fraunces', serif; font-size: {fmt['num_font']}px; color: {TERRACOTTA}; flex-shrink: 0; width: 50px; }}
.q {{ font-size: {fmt['item_font']}px; color: {CREME}; line-height: 1.35; font-weight: 500; }}
.brand {{ position: absolute; bottom: {fmt['badge_top']}px; right: 60px; font-family: 'Fraunces', serif; font-size: 18px; font-style: italic; color: {CREME}; }}
</style></head>
<body><div class="canvas">
    <div class="badge">{BADGE_DATE}</div>
    <div class="content">
        <div class="cat">{slide['cat']}</div>
        <div class="title">{slide['title']}</div>
        <div class="sep"></div>
        {rows_html}
    </div>
    <div class="brand">{BRAND}</div>
</div></body></html>"""


def build_cta_html(fmt, line1, line2):
    width, height = fmt["width"], fmt["height"]
    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {width}px; height: {height}px; overflow: hidden; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }}
.canvas {{ width: {width}px; height: {height}px; position: relative; background: {GLOW}; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 60px; }}
.badge {{ position: absolute; top: {fmt['badge_top']}px; left: 60px; border: 1px solid rgba(201,187,165,0.4); color: {MUTED}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ text-align: center; max-width: 900px; display: flex; flex-direction: column; align-items: center; gap: 40px; }}
.check {{ width: {fmt['check_size']}px; height: {fmt['check_size']}px; border: 2px solid {TERRACOTTA}; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
.headline {{ font-family: 'Fraunces', serif; font-size: {fmt['cta_title_font']}px; font-weight: 700; line-height: 1.3; letter-spacing: -0.02em; }}
.headline .l1 {{ color: {CREME}; }}
.headline .l2 {{ color: {ACCENT_SOFT}; }}
.btn {{ border: 1px solid rgba(194,65,12,0.5); border-radius: 40px; padding: 20px 40px; font-size: 22px; color: {CREME}; }}
.btn a {{ color: {ACCENT_SOFT}; }}
.brand {{ position: absolute; bottom: {fmt['badge_top']}px; right: 60px; font-family: 'Fraunces', serif; font-size: 18px; font-style: italic; color: {CREME}; }}
</style></head>
<body><div class="canvas">
    <div class="badge">{BADGE_DATE}</div>
    <div class="content">
        <div class="check">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{TERRACOTTA}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <div class="headline"><span class="l1">{line1}<br></span><span class="l2">{line2}</span></div>
        <div class="btn">Lire l'article complet → saibodanfakha.com</div>
    </div>
    <div class="brand">{BRAND}</div>
</div></body></html>"""


async def render(browser, html, width, height, out_path):
    html_path = out_path + ".tmp.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    page = await browser.new_page(viewport={"width": width, "height": height})
    await page.goto(f"file:///{html_path.replace(chr(92), '/')}")
    await page.evaluate("document.fonts.ready")
    await page.wait_for_timeout(150)
    await page.screenshot(path=out_path)
    await page.close()
    os.remove(html_path)
    print(f"[OK] {out_path}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--disable-lcd-text", "--font-render-hinting=none", "--force-color-profile=srgb"])

        for fmt_name, fmt in FORMATS.items():
            folder = os.path.join(OUT_DIR, fmt["folder"])

            for idx, slide in enumerate(CATEGORY_SLIDES, start=2):
                items = slide["items_linkedin"] if fmt_name == "linkedin" else slide["items_default"]
                html = build_category_html(fmt, slide, items)
                slug = slide["title"].lower().replace("è", "e").replace("é", "e")
                filename = f"{idx:02d}-{fmt['prefix']}-{idx}-{slug}-{fmt['width']}x{fmt['height']}.png"
                await render(browser, html, fmt["width"], fmt["height"], os.path.join(folder, filename))

            line1, line2 = CTA_LINKEDIN if fmt_name == "linkedin" else CTA_DEFAULT
            html = build_cta_html(fmt, line1, line2)
            filename = f"06-{fmt['prefix']}-6-cta-{fmt['width']}x{fmt['height']}.png"
            await render(browser, html, fmt["width"], fmt["height"], os.path.join(folder, filename))

        await browser.close()
        print("\n[SUCCESS] Slides 2 a 6 regeneres pour Instagram, LinkedIn, WhatsApp")

if __name__ == "__main__":
    asyncio.run(main())
