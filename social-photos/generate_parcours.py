"""Genere les visuels sociaux de l'article parcours-autodidacte-freelance (14/07) :
Instagram (1080x1080), LinkedIn (1080x1350), WhatsApp (1080x1920).
7 slides par format : hero, 5 chapitres du recit, CTA.
Style valide (article 7) : dark warm + halos colores, Fraunces/Inter."""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "visuels-parcours-png")

CREME = "#FEF3E2"
TERRACOTTA = "#C2410C"
ACCENT_SOFT = "#E8915F"
MUTED = "#C9BBA5"
DARK_BASE = "#1A1410"

GLOW = ("radial-gradient(820px 620px at 90% -8%, rgba(194,65,12,0.30), transparent 60%), "
        "radial-gradient(700px 560px at -8% 112%, rgba(101,115,58,0.20), transparent 60%), "
        + DARK_BASE)

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
BADGE_DATE = "Blog · 14/07"
BRAND = "Saïbo Danfakha"

HERO = {
    "kicker": "RÉCIT · PARCOURS",
    "title_l1": "Un chemin en zigzag",
    "title_l2": "jusqu'au code",
    "subtitle": "Ce qu'un parcours en zigzag apprend qu'aucune ligne droite n'enseigne.",
}

# 6 chapitres, calques sur les sections de l'article publie
STORY_SLIDES = [
    {
        "num": "01", "cat": "CHAPITRE 1 / 6",
        "title": "Le code d'abord",
        "text": "Étudiant en développement web jusqu'à la licence. Puis, pendant un temps, d'autres chemins et d'autres rêves ont pris toute la place, loin du code.",
    },
    {
        "num": "02", "cat": "CHAPITRE 2 / 6",
        "title": "Une page qui se tourne",
        "text": "Un chapitre s'est refermé. Plutôt que de m'accrocher à ce qui n'était plus, j'ai tourné la page — et appris à accepter ce que je ne pouvais pas changer.",
    },
    {
        "num": "03", "cat": "CHAPITRE 3 / 6",
        "title": "Le retour, par une porte inattendue",
        "text": "Une opportunité dans le digital m'a remis devant l'écran : contenus, montage, traduction pour un public de plusieurs pays. Sans m'en rendre compte, le web m'avait repris.",
    },
    {
        "num": "04", "cat": "CHAPITRE 4 / 6",
        "title": "Apprendre par soi-même",
        "text": "Tout réapprendre en autodidacte : les frameworks modernes, le design, le SEO. Choisir ce qu'on apprend parce qu'un projet en a besoin — tous les jours.",
    },
    {
        "num": "05", "cat": "CHAPITRE 5 / 6",
        "title": "Construire avec l'IA",
        "text": "Ce réflexe d'autodidacte m'a mené à l'IA. Je code avec elle sur chaque projet : plus vite, plus ambitieux. Mais le jugement et la qualité restent humains.",
    },
    {
        "num": "06", "cat": "CHAPITRE 6 / 6",
        "title": "International, depuis Kaolack",
        "text": "Aujourd'hui : des clients au Sénégal, au Canada, dans la diaspora. Des sites livrés, des applications en production. Sans quitter Kaolack.",
    },
]

CTA = ("Un parcours en zigzag,", "c'est un atout.")

# format: dimensions + tailles typo par reseau
FORMATS = {
    "instagram": dict(width=1080, height=1080, folder="instagram-1080x1080", prefix="ig",
                      pad=60, kicker_font=20, hero_font=72, sub_font=30,
                      num_font=120, cat_font=20, title_font=58, text_font=32,
                      cta_title_font=52, check_size=64, content_top=300),
    "linkedin": dict(width=1080, height=1350, folder="linkedin-1080x1350", prefix="li",
                     pad=70, kicker_font=21, hero_font=78, sub_font=32,
                     num_font=140, cat_font=21, title_font=62, text_font=34,
                     cta_title_font=56, check_size=68, content_top=400),
    "whatsapp": dict(width=1080, height=1920, folder="whatsapp-1080x1920", prefix="wa",
                     pad=80, kicker_font=24, hero_font=88, sub_font=38,
                     num_font=170, cat_font=24, title_font=72, text_font=40,
                     cta_title_font=64, check_size=76, content_top=640),
}

BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { overflow: hidden; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
"""


def frame(fmt, inner):
    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
{BASE_CSS}
html, body {{ width: {fmt['width']}px; height: {fmt['height']}px; }}
.canvas {{ width: {fmt['width']}px; height: {fmt['height']}px; position: relative; background: {GLOW}; }}
.badge {{ position: absolute; top: {fmt['pad']}px; left: {fmt['pad']}px; border: 1px solid rgba(201,187,165,0.4); color: {MUTED}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.brand {{ position: absolute; bottom: {fmt['pad']}px; right: {fmt['pad']}px; font-family: 'Fraunces', serif; font-size: 18px; font-style: italic; color: {CREME}; }}
</style></head>
<body><div class="canvas">
    <div class="badge">{BADGE_DATE}</div>
    {inner}
    <div class="brand">{BRAND}</div>
</div></body></html>"""


def build_hero_html(fmt):
    inner = f"""
    <style>
    .content {{ position: absolute; top: 50%; left: {fmt['pad']}px; right: {fmt['pad']}px; transform: translateY(-50%); }}
    .kicker {{ font-size: {fmt['kicker_font']}px; color: {TERRACOTTA}; font-weight: 600; letter-spacing: 0.18em; margin-bottom: 28px; }}
    .title {{ font-family: 'Fraunces', serif; font-size: {fmt['hero_font']}px; font-weight: 700; color: {CREME}; line-height: 1.12; letter-spacing: -0.02em; }}
    .title .l2 {{ color: {ACCENT_SOFT}; }}
    .subtitle {{ margin-top: 36px; font-size: {fmt['sub_font']}px; color: {MUTED}; line-height: 1.45; max-width: 20ch; font-weight: 500; }}
    </style>
    <div class="content">
        <div class="kicker">{HERO['kicker']}</div>
        <div class="title">{HERO['title_l1']}<br><span class="l2">{HERO['title_l2']}</span></div>
        <div class="subtitle">{HERO['subtitle']}</div>
    </div>"""
    return frame(fmt, inner)


def build_story_html(fmt, slide):
    inner = f"""
    <style>
    .content {{ position: absolute; top: {fmt['content_top']}px; left: {fmt['pad']}px; right: {fmt['pad']}px; }}
    .bignum {{ font-family: 'Fraunces', serif; font-size: {fmt['num_font']}px; font-weight: 600; color: rgba(232,145,95,0.28); line-height: 1; margin-bottom: 8px; }}
    .cat {{ font-size: {fmt['cat_font']}px; color: {TERRACOTTA}; font-weight: 600; letter-spacing: 0.15em; margin-bottom: 16px; }}
    .title {{ font-family: 'Fraunces', serif; font-size: {fmt['title_font']}px; font-weight: 700; color: {CREME}; letter-spacing: -0.02em; line-height: 1.15; margin-bottom: 32px; }}
    .sep {{ height: 1px; background: rgba(201,187,165,0.25); margin-bottom: 32px; width: 120px; }}
    .text {{ font-size: {fmt['text_font']}px; color: {CREME}; line-height: 1.5; font-weight: 500; max-width: 26ch; }}
    </style>
    <div class="content">
        <div class="bignum">{slide['num']}</div>
        <div class="cat">{slide['cat']}</div>
        <div class="title">{slide['title']}</div>
        <div class="sep"></div>
        <div class="text">{slide['text']}</div>
    </div>"""
    return frame(fmt, inner)


def build_cta_html(fmt):
    inner = f"""
    <style>
    .content {{ position: absolute; top: 50%; left: {fmt['pad']}px; right: {fmt['pad']}px; transform: translateY(-50%); text-align: center; display: flex; flex-direction: column; align-items: center; gap: 40px; }}
    .check {{ width: {fmt['check_size']}px; height: {fmt['check_size']}px; border: 2px solid {TERRACOTTA}; border-radius: 50%; display: flex; align-items: center; justify-content: center; }}
    .headline {{ font-family: 'Fraunces', serif; font-size: {fmt['cta_title_font']}px; font-weight: 700; line-height: 1.3; letter-spacing: -0.02em; }}
    .headline .l1 {{ color: {CREME}; }}
    .headline .l2 {{ color: {ACCENT_SOFT}; }}
    .btn {{ border: 1px solid rgba(194,65,12,0.5); border-radius: 40px; padding: 20px 40px; font-size: 22px; color: {CREME}; }}
    </style>
    <div class="content">
        <div class="check">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{TERRACOTTA}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <div class="headline"><span class="l1">{CTA[0]}<br></span><span class="l2">{CTA[1]}</span></div>
        <div class="btn">Lire le récit complet → saibodanfakha.com</div>
    </div>"""
    return frame(fmt, inner)


async def render(browser, html, width, height, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
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

        for fmt in FORMATS.values():
            folder = os.path.join(OUT_DIR, fmt["folder"])
            size = f"{fmt['width']}x{fmt['height']}"

            await render(browser, build_hero_html(fmt), fmt["width"], fmt["height"],
                         os.path.join(folder, f"01-{fmt['prefix']}-hero-{size}.png"))

            for idx, slide in enumerate(STORY_SLIDES, start=2):
                slug = (slide["title"].lower().replace("'", "").replace(",", "")
                        .replace("é", "e").replace("è", "e").replace("ê", "e").replace(" ", "-"))
                await render(browser, build_story_html(fmt, slide), fmt["width"], fmt["height"],
                             os.path.join(folder, f"{idx:02d}-{fmt['prefix']}-{slug}-{size}.png"))

            cta_num = len(STORY_SLIDES) + 2  # hero (01) + chapitres + CTA en dernier
            await render(browser, build_cta_html(fmt), fmt["width"], fmt["height"],
                         os.path.join(folder, f"{cta_num:02d}-{fmt['prefix']}-cta-{size}.png"))

        await browser.close()
        total = (len(STORY_SLIDES) + 2) * len(FORMATS)
        print(f"\n[SUCCESS] {total} visuels generes ({len(STORY_SLIDES) + 2} x Instagram, LinkedIn, WhatsApp) dans visuels-parcours-png/")

if __name__ == "__main__":
    asyncio.run(main())
