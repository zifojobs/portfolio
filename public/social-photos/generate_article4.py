"""Genere les 5 slides Instagram + 5 slides WhatsApp pour l'article 4."""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Palette
CREME = "#FEF3E2"
CREME_SOFT = "#FAF6EE"
TERRACOTTA = "#C2410C"
VERT_OLIVE = "#65733A"
NOIR_CAFE = "#2A1810"
NOIR_CAFE_DARK = "#3D2520"
SABLE_TEXT = "#7A6F5A"
CREME_TEXT = "#E8DFCB"

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'

# Contenu des 5 slides — one-page vs multi-pages
SLIDES = [
    {
        "type": "hero",
        "number": "04",
        "title": "Site one-page ou multi-pages ?",
        "subtitle_main": "Lequel choisir pour votre entreprise",
        "subtitle_note": "Un guide par Saïbo Danfakha",
    },
    {
        "type": "comparison",
        "title": "ONE-PAGE",
        "icon_type": "one",
        "points": [
            "Tout en un seul scroll",
            "Développement rapide",
            "Impact visuel immédiat",
        ],
        "accent": TERRACOTTA,
        "cta": "Parfait pour : freelancer, landing",
    },
    {
        "type": "comparison",
        "title": "MULTI-PAGES",
        "icon_type": "multi",
        "points": [
            "Contenu en profondeur",
            "SEO puissant (Google t'aime)",
            "Facile à grandir",
        ],
        "accent": VERT_OLIVE,
        "cta": "Parfait pour : PME, blog, croissance",
    },
    {
        "type": "pricing",
        "headline": "Impact sur le budget",
        "price1": "One-page : 300k-1.2M FCFA",
        "price2": "Multi-pages : 1M-4M FCFA+",
        "note": "Délai : +1-2 semaines pour multi",
        "accent": TERRACOTTA,
    },
    {
        "type": "cta",
        "headline": "L'article complet,",
        "subhead": "rendez-vous sur",
        "url": "saibodanfakha.com/blog",
    },
]


def build_instagram_slide(slide, idx, total):
    """1080x1080 - fond creme."""
    bg = f"linear-gradient(135deg, {CREME} 0%, {CREME_SOFT} 100%)"

    if slide["type"] == "hero":
        body_html = f"""
        <div class="badge">Blog · 04/12</div>
        <div class="content">
            <div class="number">{slide['number']}</div>
            <div class="title">{slide['title']}</div>
            <div class="subtitle-main">{slide['subtitle_main']}</div>
            <div class="subtitle-note">{slide['subtitle_note']}</div>
        </div>
        <div class="swipe">Swipe →</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    elif slide["type"] == "comparison":
        accent = slide["accent"]
        points_html = "".join([f"""
            <div class="point">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>{p}</span>
            </div>""" for p in slide["points"]])
        body_html = f"""
        <div class="badge" style="background: {accent};">{slide['title']}</div>
        <div class="content content-comparison">
            <div class="points">{points_html}</div>
            <div class="cta-box">{slide['cta']}</div>
        </div>
        <div class="pagination">{idx + 1} / {total}</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    elif slide["type"] == "pricing":
        accent = slide["accent"]
        body_html = f"""
        <div class="badge" style="background: {accent};">Pricing</div>
        <div class="content content-pricing">
            <div class="headline">{slide['headline']}</div>
            <div class="price-row">
                <div class="price-item">{slide['price1']}</div>
                <div class="price-sep">vs</div>
                <div class="price-item">{slide['price2']}</div>
            </div>
            <div class="note">{slide['note']}</div>
        </div>
        <div class="pagination">{idx + 1} / {total}</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    else:  # cta
        body_html = f"""
        <div class="badge">Article 04</div>
        <div class="content content-cta">
            <div class="cta-headline">{slide['headline']}</div>
            <div class="cta-subhead">{slide['subhead']}</div>
            <div class="cta-url">{slide['url']}</div>
            <svg class="arrow-icon" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="{TERRACOTTA}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
        </div>
        <div class="brand">Saïbo Danfakha</div>
        """

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1080px; overflow: hidden; font-family: 'Inter', sans-serif; }}
.canvas {{ width: 1080px; height: 1080px; position: relative; background: {bg}; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 80px; }}
.badge {{ position: absolute; top: 60px; left: 60px; background: {TERRACOTTA}; color: {CREME}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ text-align: center; max-width: 900px; }}
.number {{ font-family: 'Fraunces', serif; font-size: 160px; font-weight: 600; color: {TERRACOTTA}; line-height: 1; margin-bottom: 20px; }}
.title {{ font-family: 'Fraunces', serif; font-size: 52px; font-weight: 600; color: {NOIR_CAFE}; line-height: 1.15; margin-bottom: 20px; letter-spacing: -0.02em; }}
.subtitle-main {{ font-size: 28px; color: {SABLE_TEXT}; margin-bottom: 16px; font-weight: 500; }}
.subtitle-note {{ font-size: 16px; color: {SABLE_TEXT}; font-style: italic; }}
.content-comparison {{ display: flex; flex-direction: column; align-items: center; gap: 24px; }}
.points {{ display: flex; flex-direction: column; gap: 18px; align-items: center; }}
.point {{ display: flex; align-items: center; gap: 14px; text-align: center; max-width: 700px; }}
.point span {{ font-size: 22px; color: {NOIR_CAFE}; line-height: 1.3; font-weight: 500; }}
.point svg {{ flex-shrink: 0; }}
.cta-box {{ background: rgba(194, 65, 12, 0.1); border-left: 4px solid {TERRACOTTA}; padding: 16px 24px; border-radius: 8px; font-size: 18px; color: {SABLE_TEXT}; font-weight: 600; }}
.content-pricing {{ display: flex; flex-direction: column; align-items: center; gap: 20px; }}
.headline {{ font-family: 'Fraunces', serif; font-size: 40px; font-weight: 600; color: {NOIR_CAFE}; margin-bottom: 16px; }}
.price-row {{ display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 16px; }}
.price-item {{ font-family: 'Fraunces', serif; font-size: 28px; font-weight: 700; color: {TERRACOTTA}; letter-spacing: -0.01em; }}
.price-sep {{ font-size: 24px; color: {SABLE_TEXT}; font-weight: 600; }}
.note {{ font-size: 18px; color: {SABLE_TEXT}; font-style: italic; }}
.content-cta {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
.cta-headline {{ font-family: 'Fraunces', serif; font-size: 48px; font-weight: 600; color: {NOIR_CAFE}; letter-spacing: -0.02em; }}
.cta-subhead {{ font-size: 28px; color: {SABLE_TEXT}; }}
.cta-url {{ font-family: 'Fraunces', serif; font-size: 56px; font-weight: 700; color: {TERRACOTTA}; letter-spacing: -0.02em; margin-bottom: 20px; }}
.arrow-icon {{ margin-top: 10px; }}
.swipe {{ position: absolute; bottom: 60px; left: 60px; font-size: 16px; color: {SABLE_TEXT}; font-weight: 600; letter-spacing: 0.05em; }}
.pagination {{ position: absolute; bottom: 60px; left: 60px; font-size: 16px; color: {SABLE_TEXT}; font-weight: 600; letter-spacing: 0.05em; }}
.brand {{ position: absolute; bottom: 60px; right: 60px; font-family: 'Fraunces', serif; font-size: 20px; font-weight: 600; color: {NOIR_CAFE}; letter-spacing: -0.02em; }}
</style></head>
<body><div class="canvas">{body_html}</div></body></html>"""


def build_whatsapp_slide(slide, idx, total):
    """1080x1920 - fond noir cafe."""
    bg = f"linear-gradient(180deg, {NOIR_CAFE} 0%, {NOIR_CAFE_DARK} 100%)"

    if slide["type"] == "hero":
        body_html = f"""
        <div class="badge">Blog · 04/12</div>
        <div class="content">
            <div class="number">{slide['number']}</div>
            <div class="title">{slide['title']}</div>
            <div class="subtitle-main">{slide['subtitle_main']}</div>
            <div class="subtitle-note">{slide['subtitle_note']}</div>
        </div>
        <div class="swipe">Swipe →</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    elif slide["type"] == "comparison":
        accent = slide["accent"]
        points_html = "".join([f"""
            <div class="point">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>{p}</span>
            </div>""" for p in slide["points"]])
        body_html = f"""
        <div class="badge" style="background: {accent};">{slide['title']}</div>
        <div class="content content-comparison">
            <div class="points">{points_html}</div>
            <div class="cta-box">{slide['cta']}</div>
        </div>
        <div class="pagination">{idx + 1} / {total}</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    elif slide["type"] == "pricing":
        accent = slide["accent"]
        body_html = f"""
        <div class="badge" style="background: {accent};">Pricing</div>
        <div class="content content-pricing">
            <div class="headline">{slide['headline']}</div>
            <div class="price-row">
                <div class="price-item">{slide['price1']}</div>
            </div>
            <div class="price-sep">vs</div>
            <div class="price-row">
                <div class="price-item">{slide['price2']}</div>
            </div>
            <div class="note">{slide['note']}</div>
        </div>
        <div class="pagination">{idx + 1} / {total}</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    else:
        body_html = f"""
        <div class="badge">Article 04</div>
        <div class="content content-cta">
            <div class="cta-headline">{slide['headline']}</div>
            <div class="cta-subhead">{slide['subhead']}</div>
            <div class="cta-url">{slide['url']}</div>
            <svg class="arrow-icon" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="{TERRACOTTA}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
        </div>
        <div class="brand">Saïbo Danfakha</div>
        """

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; font-family: 'Inter', sans-serif; }}
.canvas {{ width: 1080px; height: 1920px; position: relative; background: {bg}; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 100px; }}
.badge {{ position: absolute; top: 100px; background: {TERRACOTTA}; color: {CREME}; padding: 14px 28px; border-radius: 30px; font-size: 16px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ text-align: center; max-width: 900px; }}
.number {{ font-family: 'Fraunces', serif; font-size: 220px; font-weight: 600; color: {TERRACOTTA}; line-height: 1; margin-bottom: 30px; }}
.title {{ font-family: 'Fraunces', serif; font-size: 64px; font-weight: 600; color: {CREME}; line-height: 1.15; margin-bottom: 30px; letter-spacing: -0.02em; }}
.subtitle-main {{ font-size: 36px; color: {CREME_TEXT}; margin-bottom: 20px; font-weight: 500; }}
.subtitle-note {{ font-size: 24px; color: {CREME_TEXT}; font-style: italic; }}
.content-comparison {{ display: flex; flex-direction: column; align-items: center; gap: 40px; }}
.points {{ display: flex; flex-direction: column; gap: 28px; align-items: center; }}
.point {{ display: flex; align-items: flex-start; gap: 18px; text-align: center; max-width: 800px; }}
.point span {{ font-size: 28px; color: {CREME}; line-height: 1.4; font-weight: 500; }}
.point svg {{ flex-shrink: 0; margin-top: 2px; }}
.cta-box {{ background: rgba(194, 65, 12, 0.2); border-left: 6px solid {TERRACOTTA}; padding: 24px 32px; border-radius: 8px; font-size: 24px; color: {CREME_TEXT}; font-weight: 600; }}
.content-pricing {{ display: flex; flex-direction: column; align-items: center; gap: 32px; }}
.headline {{ font-family: 'Fraunces', serif; font-size: 52px; font-weight: 600; color: {CREME}; margin-bottom: 24px; }}
.price-row {{ display: flex; align-items: center; justify-content: center; gap: 16px; }}
.price-item {{ font-family: 'Fraunces', serif; font-size: 44px; font-weight: 700; color: {TERRACOTTA}; letter-spacing: -0.01em; }}
.price-sep {{ font-size: 32px; color: {CREME_TEXT}; font-weight: 600; margin: 16px 0; }}
.note {{ font-size: 26px; color: {CREME_TEXT}; font-style: italic; }}
.content-cta {{ display: flex; flex-direction: column; align-items: center; gap: 20px; }}
.cta-headline {{ font-family: 'Fraunces', serif; font-size: 60px; font-weight: 600; color: {CREME}; letter-spacing: -0.02em; }}
.cta-subhead {{ font-size: 36px; color: {CREME_TEXT}; }}
.cta-url {{ font-family: 'Fraunces', serif; font-size: 72px; font-weight: 700; color: {TERRACOTTA}; letter-spacing: -0.02em; margin-bottom: 30px; }}
.arrow-icon {{ margin-top: 20px; }}
.swipe {{ position: absolute; bottom: 100px; left: 100px; font-size: 20px; color: {CREME_TEXT}; font-weight: 600; letter-spacing: 0.05em; }}
.pagination {{ position: absolute; bottom: 100px; left: 100px; font-size: 20px; color: {CREME_TEXT}; font-weight: 600; letter-spacing: 0.05em; }}
.brand {{ position: absolute; bottom: 100px; right: 100px; font-family: 'Fraunces', serif; font-size: 24px; font-weight: 600; color: {CREME}; letter-spacing: -0.02em; }}
</style></head>
<body><div class="canvas">{body_html}</div></body></html>"""


async def screenshot_html(html_content, output_path, width, height):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=2)
        page = await context.new_page()
        await page.set_content(html_content, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=output_path, full_page=False, omit_background=False, clip={"x": 0, "y": 0, "width": width, "height": height})
        await browser.close()
        print(f"OK: {os.path.basename(output_path)}")


async def main():
    total = len(SLIDES)
    for i, slide in enumerate(SLIDES):
        html_ig = build_instagram_slide(slide, i, total)
        html_path_ig = os.path.join(BASE_DIR, f"article4-instagram-{i+1:02d}.html")
        png_path_ig = os.path.join(BASE_DIR, f"Instagram 04-{i+1:02d}.png")
        with open(html_path_ig, "w", encoding="utf-8") as f:
            f.write(html_ig)
        await screenshot_html(html_ig, png_path_ig, 1080, 1080)

        html_wa = build_whatsapp_slide(slide, i, total)
        html_path_wa = os.path.join(BASE_DIR, f"article4-whatsapp-{i+1:02d}.html")
        png_path_wa = os.path.join(BASE_DIR, f"Whatsapp 04-{i+1:02d}.png")
        with open(html_path_wa, "w", encoding="utf-8") as f:
            f.write(html_wa)
        await screenshot_html(html_wa, png_path_wa, 1080, 1920)


if __name__ == "__main__":
    asyncio.run(main())
