"""Genere les 5 slides Instagram + 5 slides WhatsApp pour l'article 3."""
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

# Contenu des 5 slides — prix marche senegalais
SLIDES = [
    {
        "type": "hero",
        "number": "03",
        "title": "Combien coûte un site web pro au Sénégal en 2026 ?",
        "subtitle_fcfa": "De 100 000 à 20 000 000 FCFA",
        "subtitle_eur": "150€ à 30 000€",
        "subtitle_note": "4 tranches de prix décodées",
    },
    {
        "type": "tranche",
        "tag": "Tranche 1",
        "price_fcfa": "100k à 300k FCFA",
        "price_eur": "150 à 450€",
        "label": "Le DIY",
        "warning": "Templates Wix, Squarespace, WordPress",
        "points": [
            "Design générique vu mille fois",
            "Aucun support quand ça casse",
            "Pas pour vendre votre crédibilité",
        ],
        "accent": TERRACOTTA,
    },
    {
        "type": "tranche",
        "tag": "Tranche 2",
        "price_fcfa": "300k à 1M FCFA",
        "price_eur": "450 à 1 500€",
        "label": "Freelance junior",
        "warning": "Vous payez son apprentissage",
        "points": [
            "Site basé sur un thème adapté",
            "Design correct, pas différenciant",
            "Délais et support souvent flous",
        ],
        "accent": TERRACOTTA,
    },
    {
        "type": "tranche",
        "tag": "Tranche 3 ⭐",
        "price_fcfa": "1M à 5M FCFA",
        "price_eur": "1 500 à 7 500€",
        "label": "LE SWEET SPOT",
        "warning": "Freelance expérimenté",
        "points": [
            "Site sur-mesure qui reflète votre identité",
            "Code propre, performant, optimisé SEO",
            "Communication claire, délais respectés",
        ],
        "accent": VERT_OLIVE,
        "highlight": True,
    },
    {
        "type": "cta",
        "headline": "Pour lire l'article complet,",
        "subhead": "rendez-vous sur",
        "url": "saibodanfakha.com/blog",
    },
]


def build_instagram_slide(slide, idx, total):
    """1080x1080 - fond creme."""
    bg = f"linear-gradient(135deg, {CREME} 0%, {CREME_SOFT} 100%)"

    if slide["type"] == "hero":
        body_html = f"""
        <div class="badge">Blog · 03/12</div>
        <div class="content">
            <div class="number">{slide['number']}</div>
            <div class="title">{slide['title']}</div>
            <div class="subtitle-row">
                <div class="subtitle-price">{slide['subtitle_fcfa']}</div>
                <div class="subtitle-sep">·</div>
                <div class="subtitle-price">{slide['subtitle_eur']}</div>
            </div>
            <div class="subtitle-note">{slide['subtitle_note']}</div>
        </div>
        <div class="swipe">Swipe →</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    elif slide["type"] == "tranche":
        accent = slide["accent"]
        highlight = slide.get("highlight", False)
        star_class = "highlight" if highlight else ""
        points_html = "".join([f"""
            <div class="point">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>{p}</span>
            </div>""" for p in slide["points"]])
        body_html = f"""
        <div class="badge" style="background: {accent};">{slide['tag']}</div>
        <div class="content content-tranche">
            <div class="prices">
                <div class="price-fcfa {star_class}" style="color: {accent};">{slide['price_fcfa']}</div>
                <div class="price-eur {star_class}" style="color: {accent};">{slide['price_eur']}</div>
            </div>
            <div class="label">{slide['label']}</div>
            <div class="warning">{slide['warning']}</div>
            <div class="points">{points_html}</div>
        </div>
        <div class="pagination">{idx + 1} / {total}</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    else:  # cta
        body_html = f"""
        <div class="badge">Article 03</div>
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
.content {{ text-align: center; max-width: 880px; }}
.number {{ font-family: 'Fraunces', serif; font-size: 160px; font-weight: 600; color: {TERRACOTTA}; line-height: 1; margin-bottom: 20px; }}
.title {{ font-family: 'Fraunces', serif; font-size: 44px; font-weight: 600; color: {NOIR_CAFE}; line-height: 1.2; margin-bottom: 24px; letter-spacing: -0.02em; }}
.subtitle-row {{ display: flex; align-items: center; justify-content: center; gap: 18px; margin-bottom: 14px; }}
.subtitle-price {{ font-family: 'Fraunces', serif; font-size: 32px; font-weight: 600; color: {TERRACOTTA}; letter-spacing: -0.01em; }}
.subtitle-sep {{ font-size: 32px; color: {SABLE_TEXT}; }}
.subtitle-note {{ font-size: 18px; color: {SABLE_TEXT}; }}
.content-tranche {{ display: flex; flex-direction: column; align-items: center; gap: 6px; }}
.prices {{ display: flex; flex-direction: column; align-items: center; gap: 4px; margin-bottom: 12px; }}
.price-fcfa, .price-eur {{ font-family: 'Fraunces', serif; font-size: 72px; font-weight: 700; line-height: 1.05; letter-spacing: -0.02em; white-space: nowrap; }}
.price-fcfa.highlight, .price-eur.highlight {{ font-size: 82px; }}
.label {{ font-family: 'Fraunces', serif; font-size: 40px; font-weight: 600; color: {NOIR_CAFE}; margin-bottom: 6px; margin-top: 12px; }}
.warning {{ font-size: 20px; color: {SABLE_TEXT}; margin-bottom: 36px; font-style: italic; }}
.points {{ display: flex; flex-direction: column; gap: 14px; align-items: flex-start; max-width: 700px; margin: 0 auto; }}
.point {{ display: flex; align-items: flex-start; gap: 16px; text-align: left; }}
.point span {{ font-size: 22px; color: {NOIR_CAFE}; line-height: 1.4; font-weight: 500; }}
.point svg {{ flex-shrink: 0; margin-top: 4px; }}
.content-cta {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
.cta-headline {{ font-family: 'Fraunces', serif; font-size: 48px; font-weight: 600; color: {NOIR_CAFE}; letter-spacing: -0.02em; }}
.cta-subhead {{ font-size: 28px; color: {SABLE_TEXT}; margin-bottom: 16px; }}
.cta-url {{ font-family: 'Fraunces', serif; font-size: 56px; font-weight: 700; color: {TERRACOTTA}; letter-spacing: -0.02em; margin-bottom: 30px; }}
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
        <div class="badge">Blog · 03/12</div>
        <div class="content">
            <div class="number">{slide['number']}</div>
            <div class="title">{slide['title']}</div>
            <div class="subtitle-row">
                <div class="subtitle-price">{slide['subtitle_fcfa']}</div>
            </div>
            <div class="subtitle-row">
                <div class="subtitle-price">{slide['subtitle_eur']}</div>
            </div>
            <div class="subtitle-note">{slide['subtitle_note']}</div>
        </div>
        <div class="swipe">Swipe →</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    elif slide["type"] == "tranche":
        accent = slide["accent"]
        highlight = slide.get("highlight", False)
        star_class = "highlight" if highlight else ""
        points_html = "".join([f"""
            <div class="point">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>{p}</span>
            </div>""" for p in slide["points"]])
        body_html = f"""
        <div class="badge" style="background: {accent};">{slide['tag']}</div>
        <div class="content content-tranche">
            <div class="prices">
                <div class="price-fcfa {star_class}" style="color: {accent};">{slide['price_fcfa']}</div>
                <div class="price-eur {star_class}" style="color: {accent};">{slide['price_eur']}</div>
            </div>
            <div class="label">{slide['label']}</div>
            <div class="warning">{slide['warning']}</div>
            <div class="points">{points_html}</div>
        </div>
        <div class="pagination">{idx + 1} / {total}</div>
        <div class="brand">Saïbo Danfakha</div>
        """
    else:
        body_html = f"""
        <div class="badge">Article 03</div>
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
.title {{ font-family: 'Fraunces', serif; font-size: 56px; font-weight: 600; color: {CREME}; line-height: 1.2; margin-bottom: 30px; letter-spacing: -0.02em; }}
.subtitle-row {{ display: flex; align-items: center; justify-content: center; margin-bottom: 8px; }}
.subtitle-price {{ font-family: 'Fraunces', serif; font-size: 44px; font-weight: 600; color: {TERRACOTTA}; letter-spacing: -0.01em; }}
.subtitle-note {{ font-size: 24px; color: {CREME_TEXT}; margin-top: 20px; }}
.content-tranche {{ display: flex; flex-direction: column; align-items: center; gap: 8px; }}
.prices {{ display: flex; flex-direction: column; align-items: center; gap: 4px; margin-bottom: 20px; }}
.price-fcfa, .price-eur {{ font-family: 'Fraunces', serif; font-size: 86px; font-weight: 700; line-height: 1.05; letter-spacing: -0.02em; white-space: nowrap; }}
.price-fcfa.highlight, .price-eur.highlight {{ font-size: 100px; }}
.label {{ font-family: 'Fraunces', serif; font-size: 50px; font-weight: 600; color: {CREME}; margin-bottom: 8px; margin-top: 16px; }}
.warning {{ font-size: 26px; color: {CREME_TEXT}; margin-bottom: 50px; font-style: italic; }}
.points {{ display: flex; flex-direction: column; gap: 22px; align-items: flex-start; max-width: 800px; margin: 0 auto; }}
.point {{ display: flex; align-items: flex-start; gap: 18px; text-align: left; }}
.point span {{ font-size: 26px; color: {CREME}; line-height: 1.4; font-weight: 500; }}
.point svg {{ flex-shrink: 0; margin-top: 6px; }}
.content-cta {{ display: flex; flex-direction: column; align-items: center; gap: 20px; }}
.cta-headline {{ font-family: 'Fraunces', serif; font-size: 60px; font-weight: 600; color: {CREME}; letter-spacing: -0.02em; }}
.cta-subhead {{ font-size: 36px; color: {CREME_TEXT}; margin-bottom: 24px; }}
.cta-url {{ font-family: 'Fraunces', serif; font-size: 72px; font-weight: 700; color: {TERRACOTTA}; letter-spacing: -0.02em; margin-bottom: 40px; }}
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
        html_path_ig = os.path.join(BASE_DIR, f"article3-instagram-{i+1:02d}.html")
        png_path_ig = os.path.join(BASE_DIR, f"Instagram 03-{i+1:02d}.png")
        with open(html_path_ig, "w", encoding="utf-8") as f:
            f.write(html_ig)
        await screenshot_html(html_ig, png_path_ig, 1080, 1080)

        html_wa = build_whatsapp_slide(slide, i, total)
        html_path_wa = os.path.join(BASE_DIR, f"article3-whatsapp-{i+1:02d}.html")
        png_path_wa = os.path.join(BASE_DIR, f"Whatsapp 03-{i+1:02d}.png")
        with open(html_path_wa, "w", encoding="utf-8") as f:
            f.write(html_wa)
        await screenshot_html(html_wa, png_path_wa, 1080, 1920)


if __name__ == "__main__":
    asyncio.run(main())
