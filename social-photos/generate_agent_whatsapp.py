"""Genere 1 visuel de presentation de l'Agent WhatsApp perso de Saibo (1080x1080)."""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Palette (identique aux articles precedents)
CREME = "#FEF3E2"
TERRACOTTA = "#C2410C"
DARK_BASE = "#1A1410"
ACCENT_SOFT = "#E8915F"
MUTED = "#C9BBA5"

GLOW = ("radial-gradient(820px 620px at 90% -8%, rgba(194,65,12,0.30), transparent 60%), "
        "radial-gradient(700px 560px at -8% 112%, rgba(101,115,58,0.20), transparent 60%), "
        + DARK_BASE)

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'

CONTENT = {
    "fr": {
        "lang": "fr",
        "badge": "Coté atelier",
        "title": "Mon assistant WhatsApp",
        "subtitle": "Construit par moi, pour moi — 100% perso",
        "points": [
            "Répond à ma place quand je suis absent (rien ne part sans ma validation)",
            "Se souvient de nos derniers échanges",
            "Me propose des idées : statuts, rappels, stratégie",
            "Hébergé et codé par moi, de A à Z",
        ],
        "cta": "Envie du même niveau d'automatisation pour votre business ?<br>Parlons-en : "
               '<span class="cta-number">+221 77 527 71 64</span> · saibodanfakha.com',
    },
    "en": {
        "lang": "en",
        "badge": "Behind the scenes",
        "title": "My WhatsApp Assistant",
        "subtitle": "Built by me, for me — 100% personal",
        "points": [
            "Replies for me when I'm away (nothing sent without my approval)",
            "Remembers our recent conversation",
            "Suggests ideas: posts, reminders, strategy",
            "Hosted and coded by me, end to end",
        ],
        "cta": "Want this level of automation for your business?<br>Let's talk: "
               '<span class="cta-number">+221 77 527 71 64</span> · saibodanfakha.com',
    },
}


def build_slide(lang):
    c = CONTENT[lang]
    points_html = "".join([f"""
        <div class="point">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{TERRACOTTA}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>{p}</span>
        </div>""" for p in c["points"]])

    body_html = f"""
    <div class="badge">{c['badge']}</div>
    <div class="content">
        <div class="icon">🤖</div>
        <div class="title">{c['title']}</div>
        <div class="subtitle">{c['subtitle']}</div>
        <div class="agent-number">📱 +221 76 185 73 73</div>
        <div class="points">{points_html}</div>
        <div class="cta">{c['cta']}</div>
    </div>
    <div class="brand">Saïbo Danfakha</div>
    """

    html = f"""<!DOCTYPE html>
<html lang="{c['lang']}"><head><meta charset="UTF-8">{FONT_LINK}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1080px; overflow: hidden; font-family: 'Inter', sans-serif; }}
.canvas {{ width: 1080px; height: 1080px; position: relative; background: {GLOW}; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 70px; }}
.badge {{ position: absolute; top: 60px; left: 60px; background: {TERRACOTTA}; color: {CREME}; padding: 12px 24px; border-radius: 30px; font-size: 14px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
.content {{ text-align: center; max-width: 880px; display: flex; flex-direction: column; align-items: center; }}
.icon {{ font-size: 64px; margin-bottom: 16px; }}
.title {{ font-family: 'Fraunces', serif; font-size: 52px; font-weight: 600; color: {CREME}; line-height: 1.2; margin-bottom: 14px; letter-spacing: -0.02em; }}
.subtitle {{ font-size: 20px; color: {ACCENT_SOFT}; margin-bottom: 20px; font-weight: 500; }}
.agent-number {{ font-size: 20px; color: {CREME}; margin-bottom: 36px; font-weight: 700; letter-spacing: 0.02em; }}
.points {{ display: flex; flex-direction: column; gap: 18px; align-items: flex-start; width: 760px; }}
.point {{ display: flex; align-items: flex-start; gap: 14px; text-align: left; width: 100%; }}
.point span {{ font-size: 18px; color: {CREME}; line-height: 1.4; font-weight: 500; }}
.point svg {{ flex-shrink: 0; margin-top: 2px; }}
.cta {{ margin-top: 36px; padding-top: 28px; border-top: 1px solid rgba(254,243,226,0.15); font-size: 16px; color: {MUTED}; line-height: 1.6; text-align: center; }}
.cta-number {{ color: {ACCENT_SOFT}; font-weight: 700; }}
.brand {{ position: absolute; bottom: 60px; right: 60px; font-family: 'Fraunces', serif; font-size: 18px; font-weight: 600; color: {CREME}; letter-spacing: -0.02em; }}
</style></head>
<body><div class="canvas">{body_html}</div></body></html>"""
    return html


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for lang, suffix in [("fr", ""), ("en", " (EN)")]:
            html = build_slide(lang)
            html_path = os.path.join(BASE_DIR, f"agent-whatsapp-presentation-{lang}.html")
            png_path = os.path.join(BASE_DIR, f"Agent WhatsApp - presentation{suffix}.png")

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

            page = await browser.new_page(viewport={"width": 1080, "height": 1080})
            await page.goto(f"file:///{html_path.replace(chr(92), '/')}")
            await page.screenshot(path=png_path)
            await page.close()
            print(f"[SUCCESS] {png_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
