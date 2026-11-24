"""Post 2 de l'article du 20/10/2026 (référencement Google à Dakar).
7 diapos Instagram 1080x1350 + 1 statut WhatsApp 1080x1920.
Univers « Africain Contemporain » (crème, noir café, terracotta, savane, Fraunces + Inter).
Motif = le tréma du « ï » de Saïbo (deux disques) : décor, puces, pagination.
Aucune personne : les visuels sont des écrans dessinés (règle du blog).
Usage : python generate_seo_dakar.py [n ...]  (n = 1..7, 8 = statut WhatsApp)  →  visuels-seo-dakar-png/"""
import asyncio
import base64
import io
import os
import sys
from PIL import Image
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "visuels-seo-dakar-png")
LOGO = os.path.join(BASE_DIR, "..", "design system", "png", "transparent", "Noir Café (1024 x 1024 px).png")

CREME = "#FEF3E2"
SABLE1 = "#FAF6EE"
SABLE3 = "#E8DFCB"
SABLE6 = "#7A6F5A"
CAFE = "#2A1810"
TERRA = "#C2410C"
SAVANE = "#65733A"
TOTAL = 7


def logo_uri():
    im = Image.open(LOGO)
    im = im.crop(im.getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.width / im.height


LOGO_URI, LOGO_RATIO = logo_uri()
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;'
         '1,9..144,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')


def css(w, h):
    return f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;font-family:'Inter',sans-serif;color:{CAFE};background:{CREME}}}
.c{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{CREME}}}
.ribbon{{position:absolute;top:0;left:0;right:0;height:10px;display:flex;z-index:3}}
.ribbon i{{flex:1}}
.disc{{position:absolute;border-radius:50%}}
.tx{{position:absolute;left:80px;top:120px;width:920px;z-index:2}}
.kick{{display:flex;align-items:center;gap:14px;font-size:22px;font-weight:700;letter-spacing:3.5px;text-transform:uppercase;color:{TERRA}}}
.trema{{display:inline-flex;gap:7px}} .trema i{{width:11px;height:11px;border-radius:50%;background:{TERRA}}}
.trema i+i{{background:{SAVANE}}}
h1{{font-family:'Fraunces',serif;font-weight:600;letter-spacing:-0.025em;line-height:1.02;margin-top:26px;color:{CAFE}}}
h1 em{{font-style:italic;font-weight:500;color:{TERRA}}}
.sub{{font-size:28px;line-height:1.45;color:{SABLE6};max-width:820px;margin-top:30px}}
.frame{{position:absolute;z-index:2;background:#fff;border-radius:0 56px 0 56px;overflow:hidden;
  box-shadow:0 30px 70px rgba(42,24,16,.16),0 0 0 1px rgba(42,24,16,.06)}}
.foot{{position:absolute;left:80px;right:80px;bottom:60px;padding-top:30px;border-top:1.5px solid {SABLE3};
  display:flex;justify-content:space-between;align-items:center;z-index:2}}
.foot img{{height:32px;width:calc(32px * {LOGO_RATIO:.3f})}}
.dots{{display:flex;align-items:center;gap:10px}}
.dots i{{width:12px;height:12px;border-radius:50%;background:{SABLE3}}}
.dots i.on{{width:34px;border-radius:6px;background:{TERRA}}}
.cta{{font-size:21px;font-weight:700;letter-spacing:3px;color:{TERRA}}}
/* écrans dessinés */
.gbar{{display:flex;align-items:center;gap:16px;border:1.5px solid #dfe1e5;border-radius:999px;padding:18px 26px;font-size:26px;color:#202124;background:#fff}}
.res .u{{font-size:17px;color:#4d5156}} .res .t{{font-size:25px;color:#1a0dab;margin:4px 0}} .res .d{{font-size:18px;color:#4d5156;line-height:1.4}}
.skel{{height:14px;border-radius:7px;background:#eceae6}}
.row{{display:flex;justify-content:space-between;align-items:center;padding:18px 26px;border-top:1px solid #eee}}
.row .n{{font-size:22px;font-weight:600}} .row .s{{font-size:17px;color:#70757a;margin-top:4px}}
.mark{{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:22px;flex:none}}
.pin{{position:absolute;width:30px;height:30px;background:{TERRA};border-radius:50% 50% 50% 0;transform:rotate(-45deg);box-shadow:0 4px 8px rgba(0,0,0,.2)}}
.pin.o{{background:#b9b3a8}}
"""


SEARCH = ('<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#9aa0a6" stroke-width="2.4" stroke-linecap="round">'
          '<circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>')


def ribbon():
    return f'<div class="ribbon"><i style="background:{CAFE}"></i><i style="background:{TERRA}"></i><i style="background:{SAVANE}"></i></div>'


def trema_decor(x, y, r=170):
    """Les deux points du « ï », en grand, à demi cachés derrière l'écran."""
    return (f'<div class="disc" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{TERRA}"></div>'
            f'<div class="disc" style="left:{x + r + 34}px;top:{y}px;width:{r}px;height:{r}px;background:{SAVANE}"></div>')


def kicker(t):
    return f'<div class="kick"><span class="trema"><i></i><i></i></span>{t}</div>'


def text(kick, title, size, sub):
    return f'<div class="tx">{kicker(kick)}<h1 style="font-size:{size}px">{title}</h1><p class="sub">{sub}</p></div>'


def foot(i, right=None):
    if right is None:
        right = '<div class="dots">' + "".join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(1, TOTAL + 1)) + "</div>"
    else:
        right = f'<div class="cta">{right}</div>'
    return f'<div class="foot"><img src="{LOGO_URI}" alt="Saïbo Danfakha">{right}</div>'


def doc(w, h, body):
    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">{FONTS}<style>{css(w, h)}</style></head>'
            f'<body><div class="c">{ribbon()}{body}</div></body></html>')


def skel_result(w1, w2, w3):
    return (f'<div style="padding:14px 0"><div class="skel" style="width:{w1 * 0.4}%"></div>'
            f'<div class="skel" style="width:{w1}%;height:20px;margin:10px 0;background:#e3e0f0"></div>'
            f'<div class="skel" style="width:{w2}%"></div><div class="skel" style="width:{w3}%;margin-top:8px"></div></div>')


def gscreen(left, top, width, height):
    return (f'<div class="frame" style="left:{left}px;top:{top}px;width:{width}px;height:{height}px;padding:40px 44px">'
            f'<div class="gbar">{SEARCH}<span>traiteur mariage Dakar</span></div>'
            f'<div style="margin-top:18px">{skel_result(72, 94, 58)}{skel_result(64, 90, 66)}</div>'
            f'<div style="position:absolute;right:44px;bottom:34px;font-size:20px;font-weight:600;color:{TERRA}">Et votre site ?</div></div>')


HERO_TITLE = 'Votre site existe.<br><em>Google le <span style="white-space:nowrap">montre-t-il&nbsp;?</span></em>'
HERO_SUB = "Les 7 étapes, dans l'ordre, pour être trouvé par vos clients à Dakar. Sans publicité."


def s1():
    return (trema_decor(560, 640, 200) + text("Guide · 7 étapes", HERO_TITLE, 104, HERO_SUB)
            + gscreen(80, 760, 860, 400) + foot(1))


def s2():
    screen = (f'<div class="frame" style="left:80px;top:690px;width:860px;height:450px;padding:40px 44px">'
              f'<div class="gbar">{SEARCH}<span>site:votresite.com</span></div>'
              f'<div style="margin-top:34px;font-size:24px;line-height:1.5;color:#202124">Aucun document ne correspond aux termes de recherche spécifiés.</div>'
              f'<div style="margin-top:30px;display:flex;align-items:center;gap:16px;padding:20px 24px;background:{SABLE1};border-radius:0 24px 0 24px">'
              f'<div class="mark" style="background:{SAVANE}">✓</div><div style="font-size:22px"><b>Search Console</b> · gratuit : Google vous dit ce qu\'il a retenu.</div></div></div>')
    return (trema_decor(640, 600, 160) + text("Étape 1 sur 7", "Google connaît-il<br><em>votre site ?</em>", 96,
                                              "Tapez cette recherche avec votre adresse. Si rien ne s'affiche, tout le reste attend.")
            + screen + foot(2))


def s3():
    pins = ('<div class="pin" style="left:46%;top:38%"></div><div class="pin o" style="left:22%;top:58%"></div>'
            '<div class="pin o" style="left:72%;top:24%"></div>')
    streets = ('<div style="position:absolute;inset:0;background:'
               'linear-gradient(90deg,transparent 30%,#fff 30%,#fff 32%,transparent 32%),'
               'linear-gradient(0deg,transparent 55%,#fff 55%,#fff 58%,transparent 58%),'
               'linear-gradient(35deg,transparent 62%,#fff 62%,#fff 64%,transparent 64%),'
               'linear-gradient(120deg,transparent 20%,#DDE3CF 20%,#DDE3CF 34%,transparent 34%)"></div>')
    rows = (f'<div class="row" style="background:#FFF7EE"><div><div class="n">Votre pâtisserie</div>'
            f'<div class="s"><span style="color:#E8A33A">★★★★★</span> 4,8 · Mermoz · Ouvert</div></div>'
            f'<div class="mark" style="background:{TERRA}">1</div></div>'
            f'<div class="row"><div style="width:70%"><div class="skel" style="width:60%;height:18px"></div>'
            f'<div class="skel" style="width:85%;margin-top:10px"></div></div><div class="mark" style="background:#c9c4ba">2</div></div>'
            f'<div class="row"><div style="width:70%"><div class="skel" style="width:52%;height:18px"></div>'
            f'<div class="skel" style="width:78%;margin-top:10px"></div></div><div class="mark" style="background:#c9c4ba">3</div></div>')
    screen = (f'<div class="frame" style="left:80px;top:660px;width:780px;height:480px">'
              f'<div style="position:relative;height:210px;background:#EEF0E6;overflow:hidden">{streets}{pins}</div>{rows}</div>')
    return (trema_decor(620, 600, 180) + text("Étape 2 sur 7", "Votre fiche<br><em>Google Business</em>", 96,
                                              "« pâtisserie Mermoz » : Google montre d'abord une carte avec trois adresses. Elles viennent des fiches, pas des sites.")
            + screen + foot(3))


def s4():
    sugg = "".join(f'<div style="display:flex;align-items:center;gap:16px;padding:16px 4px;font-size:24px;color:#202124">{SEARCH}'
                   f'<span>traiteur <b>{s}</b></span></div>' for s in ("mariage dakar", "baptême dakar", "pas cher dakar", "livraison dakar"))
    screen = (f'<div class="frame" style="left:80px;top:690px;width:860px;height:450px;padding:36px 44px">'
              f'<div class="gbar">{SEARCH}<span>traiteur<span style="display:inline-block;width:3px;height:30px;background:{TERRA};margin-left:4px;vertical-align:middle"></span></span></div>'
              f'<div style="margin-top:10px;padding:0 22px">{sugg}</div></div>')
    return (trema_decor(640, 600, 160) + text("Étape 3 sur 7", "Une page<br><em>pour chaque recherche</em>", 96,
                                              "Vos clients tapent un besoin et un lieu. Un service = une page, avec la ville dans le titre.")
            + screen + foot(4))


def s5():
    bad = ('<div style="display:flex;gap:18px;align-items:flex-start;padding:26px 30px;border-bottom:1px solid #eee">'
           '<div class="mark" style="background:#B3261E">✕</div><div class="res">'
           '<div class="u">votresite.com</div><div class="t">Accueil</div>'
           '<div class="d">Bienvenue sur notre site…</div></div></div>')
    good = (f'<div style="display:flex;gap:18px;align-items:flex-start;padding:26px 30px">'
            f'<div class="mark" style="background:{SAVANE}">✓</div><div class="res">'
            '<div class="u">votresite.com › mariages</div><div class="t">Traiteur pour mariages à Dakar — Votre nom</div>'
            '<div class="d">Menus sénégalais et internationaux, de 50 à 500 invités. Devis sur WhatsApp.</div></div></div>')
    screen = f'<div class="frame" style="left:80px;top:680px;width:680px;height:420px">{bad}{good}</div>'
    phone = (f'<div style="position:absolute;z-index:2;right:80px;top:640px;width:230px;height:460px;background:{CAFE};border-radius:42px;padding:14px;'
             f'box-shadow:0 30px 70px rgba(42,24,16,.25)"><div style="background:{SABLE1};height:100%;border-radius:30px;display:flex;'
             f'flex-direction:column;align-items:center;justify-content:center;gap:10px">'
             f'<div style="width:150px;height:150px;border-radius:50%;background:conic-gradient({SAVANE} 0 82%, {SABLE3} 82% 100%);'
             f'display:flex;align-items:center;justify-content:center"><div style="width:118px;height:118px;border-radius:50%;background:{SABLE1};'
             f'display:flex;align-items:center;justify-content:center;font-family:Fraunces,serif;font-size:44px;font-weight:600;color:{SAVANE}">82</div></div>'
             f'<div style="font-size:16px;font-weight:600;color:{SABLE6};letter-spacing:1px">MOBILE</div>'
             f'<div style="font-size:15px;color:{SABLE6};text-align:center;padding:0 16px">PageSpeed Insights</div></div></div>')
    return (text("Étapes 4 et 5 sur 7", "Donnez envie<br><em>de cliquer</em>", 96,
                 "Un titre qui dit le service et la ville, pas « Accueil ». Et un site rapide sur téléphone : testez-le, c'est gratuit.")
            + screen + phone + foot(5))


def s6():
    lines = "".join(f'<div class="row" style="padding:20px 30px"><div><div class="n">{src}</div><div class="s">Votre nom · 77 XXX XX XX · Mermoz</div></div>'
                    f'<div class="mark" style="background:{SAVANE}">✓</div></div>' for src in ("Votre site", "Fiche Google", "Page Facebook"))
    left = f'<div class="frame" style="left:80px;top:680px;width:560px;height:400px;padding-top:10px">{lines}</div>'
    bars = "".join(f'<div style="flex:1;height:{h}%;background:{TERRA if k == 5 else SABLE3};border-radius:8px 8px 0 0"></div>'
                   for k, h in enumerate((22, 30, 38, 46, 60, 82)))
    right = (f'<div class="frame" style="left:670px;top:740px;width:330px;height:340px;padding:30px;border-radius:56px 0 56px 0">'
             f'<div style="font-size:18px;font-weight:600;color:{SABLE6};letter-spacing:1px">IMPRESSIONS / MOIS</div>'
             f'<div style="display:flex;align-items:flex-end;gap:12px;height:220px;margin-top:24px">{bars}</div></div>')
    return (text("Étapes 6 et 7 sur 7", "Soyez constant,<br><em>et mesurez</em>", 96,
                 "Les mêmes coordonnées partout, au caractère près. Un article utile par quinzaine, et trois chiffres à lire chaque mois.")
            + left + right + foot(6))


def s7():
    screen = (f'<div class="frame" style="left:80px;top:700px;width:860px;height:420px">'
              f'<div style="display:flex;align-items:center;gap:10px;padding:18px 24px;background:{SABLE1};border-bottom:1px solid #eee">'
              f'<i style="width:14px;height:14px;border-radius:50%;background:{TERRA}"></i><i style="width:14px;height:14px;border-radius:50%;background:{SAVANE}"></i>'
              f'<div style="margin-left:16px;flex:1;background:#fff;border-radius:999px;padding:10px 22px;font-size:20px;color:{SABLE6}">saibodanfakha.com/blog</div></div>'
              f'<div style="padding:40px 48px"><div style="font-size:18px;font-weight:700;letter-spacing:3px;color:{TERRA}">BLOG · 20 OCTOBRE 2026</div>'
              f'<div style="font-family:Fraunces,serif;font-size:46px;font-weight:600;line-height:1.1;letter-spacing:-0.02em;margin-top:16px">Référencement Google à Dakar : par où commencer en 2026</div>'
              f'<div style="font-size:22px;color:{SABLE6};margin-top:18px">7 étapes · sans publicité</div></div></div>')
    return (trema_decor(620, 620, 180) + text("Le guide complet", "Les 7 étapes en détail,<br><em>sur mon blog</em>", 92,
                                              "Les 4 premières se font en une semaine. Un avis sur votre site ? Écrivez-moi en message.")
            + screen + foot(7, "LIEN EN BIO ↗"))


def statut():
    big = ('<style>.tx{top:200px}.kick{font-size:30px}.trema i{width:15px;height:15px}.sub{font-size:40px;max-width:900px}'
           '.foot img{height:44px;width:calc(44px * ' + f'{LOGO_RATIO:.3f}' + ')}.cta{font-size:28px}</style>')
    return (big + trema_decor(540, 1000, 240) + text("Guide · 7 étapes", HERO_TITLE, 108, HERO_SUB)
            + gscreen(80, 1140, 920, 480) + foot(1, "LIEN CI-DESSOUS ↓"))


SLIDES = {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7}


async def render(b, html, w, h, name):
    path = os.path.join(OUT_DIR, f"_{name}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    pg = await b.new_page(viewport={"width": w, "height": h})
    await pg.goto("file:///" + path.replace("\\", "/"), wait_until="networkidle")
    await pg.evaluate("document.fonts.ready")
    await pg.screenshot(path=os.path.join(OUT_DIR, name + ".png"))
    await pg.close()
    os.remove(path)
    print("[OK]", name)


async def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    wanted = [int(a) for a in sys.argv[1:]] or list(range(1, 9))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for n in wanted:
            if n == 8:
                await render(b, doc(1080, 1920, statut()), 1080, 1920, "Statut-WhatsApp")
            else:
                await render(b, doc(1080, 1350, SLIDES[n]()), 1080, 1350, f"Instagram-{n:02d}")
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
