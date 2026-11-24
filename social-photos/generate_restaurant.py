"""Carrousel de l'article « Site web pour restaurant à Dakar » (17/11/2026) — NOUVELLE DIRECTION (charte du 16/11).
Schibsted Grotesk seule, pas d'étiquette en capitales, pas d'italique coloré, palette PROVISOIRE de la maquette.
Textes : SEO/posts/2026-11-17.md, Post 2. Aucun prix inventé : les prix du menu dessiné sont des barres grises.
Usage : python generate_restaurant.py essais   →  visuels-restaurant-png/"""
import base64
import os
import sys

from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "visuels-restaurant-png")
PHOTO = os.path.join(BASE, "..", "public", "blog", "restaurant-dakar.jpg")

PAPER, INK, SOFT, RULE, GREEN = "#FBFBF9", "#151715", "#4C524D", "#D6D9D4", "#1C5A3E"


def photo_uri():
    with open(PHOTO, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def page(body, w=1080, h=1350, bg=PAPER, fg=INK):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;600;800&display=swap" rel="stylesheet">
<style>*{{box-sizing:border-box;margin:0}}body{{width:{w}px;height:{h}px;overflow:hidden;background:{bg};color:{fg};
font-family:'Schibsted Grotesk',sans-serif;position:relative}}
h1{{font-weight:800;letter-spacing:-.025em;line-height:1.02}}
.foot{{position:absolute;left:80px;right:80px;bottom:56px;display:flex;justify-content:space-between;font-size:24px}}
.foot b{{font-weight:600}}</style></head><body>{body}</body></html>"""


def foot(n, color=SOFT, name=INK):
    return f'<div class="foot" style="color:{color}"><b style="color:{name}">Saïbo Danfakha</b><span>{n} / 7</span></div>'


def phone(left, top, scale=1.0):
    """Téléphone dessiné : la page d'un restaurant qui montre tout de suite les 4 réponses."""
    bar = lambda w: f'<i style="display:inline-block;width:{w}px;height:14px;border-radius:7px;background:{RULE}"></i>'
    plat = lambda nom: (f'<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;'
                        f'border-bottom:1px solid {RULE};font-size:22px">{nom}{bar(70)}</div>')
    return f"""<div style="position:absolute;left:{left}px;top:{top}px;width:420px;height:900px;transform:scale({scale});
transform-origin:top left;border:12px solid {INK};border-radius:56px;background:#fff;overflow:hidden">
<div style="padding:44px 30px 0">
<div style="font-size:30px;font-weight:800;letter-spacing:-.02em">Votre restaurant</div>
<div style="font-size:19px;color:{GREEN};font-weight:600;margin-top:6px">Ouvert · 12 h – 23 h</div>
<div style="font-size:18px;color:{SOFT};margin-top:4px">Plateau, Dakar · Itinéraire →</div>
<div style="display:flex;gap:10px;margin-top:22px">
<span style="flex:1;text-align:center;padding:14px 0;border-radius:10px;background:{INK};color:#fff;font-size:19px;font-weight:600">Appeler</span>
<span style="flex:1;text-align:center;padding:14px 0;border-radius:10px;border:2px solid {INK};font-size:19px;font-weight:600">WhatsApp</span></div>
<div style="font-size:21px;font-weight:800;margin-top:30px">Menu</div>
{plat("Thiéboudienne")}{plat("Yassa poulet")}{plat("Mafé")}{plat("Bissap, gingembre")}
</div></div>"""


TITRE = "Ton restaurant a un site.<br>Ton client y trouve-t-il ce qu'il&nbsp;cherche&nbsp;?"
SOUS = "Ce qu'un site de restaurant à Dakar doit contenir"


def essai_a():
    """Photo en grand en haut, titre dessous : le lieu d'abord."""
    return page(f"""<div style="position:absolute;left:0;top:0;width:1080px;height:640px;
background:url({photo_uri()}) center/cover"></div>
<div style="position:absolute;left:80px;right:80px;top:700px">
<h1 style="font-size:78px">{TITRE}</h1>
<p style="font-size:30px;color:{SOFT};margin-top:28px;line-height:1.35">{SOUS}</p></div>{foot(1)}""")


def essai_b():
    """Le téléphone dessiné : la réponse visible, titre à gauche."""
    return page(f"""<div style="position:absolute;left:80px;top:96px;width:920px">
<h1 style="font-size:76px">{TITRE}</h1>
<p style="font-size:30px;color:{SOFT};margin-top:24px">{SOUS}</p></div>
<div style="position:absolute;left:0;right:0;top:560px;height:1px;background:{RULE}"></div>
{phone(330, 600, 1.0)}{foot(1)}""")


def essai_c():
    """Fond encre, photo en bande, titre blanc : le plus contrasté."""
    return page(f"""<div style="position:absolute;left:80px;right:80px;top:96px">
<h1 style="font-size:78px;color:#fff">{TITRE}</h1>
<p style="font-size:30px;color:#B9BEB9;margin-top:28px">{SOUS}</p></div>
<div style="position:absolute;left:80px;right:80px;top:640px;height:520px;border-radius:6px;
background:url({photo_uri()}) center/cover"></div>{foot(1, '#B9BEB9', '#fff')}""", bg=INK, fg="#fff")


def render(items):
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, html, w, h in items:
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.set_content(html, wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.screenshot(path=os.path.join(OUT, name + ".png"))
            pg.close()
            print("ok", name)
        b.close()


if __name__ == "__main__":
    if sys.argv[1:] == ["essais"]:
        render([("essai-A", essai_a(), 1080, 1350), ("essai-B", essai_b(), 1080, 1350), ("essai-C", essai_c(), 1080, 1350)])
