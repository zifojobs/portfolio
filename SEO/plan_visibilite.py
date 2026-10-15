"""Génère SEO/PLAN-VISIBILITE-2026-2027.xlsx (méthode équipe SEO de Platinum, transposée)."""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SITE = Path(sys.argv[1])
OUT = SITE / "SEO" / "PLAN-VISIBILITE-2026-2027.xlsx"

NOIR, TERRA, SABLE = "2B1D14", "B5532F", "F3EDE4"
H_FONT = Font(bold=True, color="FFFFFF")
H_FILL = PatternFill("solid", fgColor=NOIR)
WRAP = Alignment(wrap_text=True, vertical="top")


def sheet(wb, titre, sous_titre, entetes, largeurs, lignes):
    ws = wb.create_sheet(titre)
    ws["A1"] = titre
    ws["A1"].font = Font(bold=True, size=16, color=TERRA)
    ws["A2"] = sous_titre
    ws["A2"].font = Font(italic=True, color="6B5B4E")
    for i, (h, w) in enumerate(zip(entetes, largeurs), start=1):
        c = ws.cell(4, i, h)
        c.font, c.fill, c.alignment = H_FONT, H_FILL, WRAP
        ws.column_dimensions[get_column_letter(i)].width = w
    for r, ligne in enumerate(lignes, start=5):
        for i, v in enumerate(ligne, start=1):
            c = ws.cell(r, i, v)
            c.alignment = WRAP
            if r % 2:
                c.fill = PatternFill("solid", fgColor=SABLE)
    ws.freeze_panes = "B5"
    return ws


wb = Workbook()
wb.remove(wb.active)

# 0. À lire d'abord
ws = wb.create_sheet("À lire d'abord")
ws.column_dimensions["A"].width = 110
texte = [
    ("Plan de visibilité saibodanfakha.com — 16/10/2026 → 15/04/2027", Font(bold=True, size=16, color=TERRA)),
    ("Préparé le 15/10/2026. C'est à la fois le plan et le rapport : ce qui est prévu est écrit avant, ce qui est fait est noté après.", None),
    ("", None),
    ("LA MÉTHODE (copiée sur l'équipe SEO de Platinum)", Font(bold=True)),
    ("1. Un mot-clé principal pour le site + des secondaires répartis page par page (onglet 1).", None),
    ("2. Une feuille de meta : title, description, longueur, conformité (onglet 2).", None),
    ("3. Un article par semaine « besoin + ville/public », publié le mardi à 9 h (onglet 3).", None),
    ("4. Chaque article décliné en 3 posts : mardi LinkedIn + X, jeudi matin carrousel Instagram + Statut WhatsApp, samedi vidéo TikTok/Reels.", None),
    ("5. Annuaires et avis en parallèle, 1 h par semaine (onglet 5).", None),
    ("6. Un rapport chaque mois, 1re semaine (onglet 6).", None),
    ("", None),
    ("CE QUI EST AUTOMATIQUE", Font(bold=True)),
    ("• Jeudi : une routine cloud rédige l'article du mardi suivant sur une branche + les textes des 3 posts (SEO/posts/).", None),
    ("• Mardi 9 h : une routine cloud publie l'article, sauf si le fichier NE-PAS-PUBLIER existe sur la branche.", None),
    ("• Reste à Saïbo : relire entre jeudi et lundi, publier les 3 posts sur ses comptes, cocher l'onglet 4, inscriptions annuaires, relevé Search Console.", None),
    ("", None),
    ("LES 3 VAGUES", Font(bold=True)),
    ("Vague 1 (20/10 → 29/12) : Dakar + diaspora, sites + référencement.", None),
    ("Vague 2 (05/01 → 23/02) : ONG et associations, outils sur mesure.", None),
    ("Vague 3 (02/03 → 13/04) : Canada en anglais — SEULEMENT si ≥ 80 % des publications des vagues 1-2 sont faites.", None),
    ("", None),
    ("CIBLES AU 15/04/2027 (à mesurer, pas promises)", Font(bold=True)),
    ("Impressions sur 3 mois : 96 → 1 500 · 5 requêtes non-marque en top 10 · ≥ 2 demandes entrantes par mois · ≥ 80 % des publications faites.", None),
    ("Point d'arrêt au 15/01 : si moins de 50 % des publications sont faites, on passe à 2 articles par mois.", None),
    ("", None),
    ("GARDE-FOUS", Font(bold=True)),
    ("Aucun prix de Saïbo · aucun client nommé sans accord · aucune musique · pas de personnes dans les images du blog · rien publié le jeudi soir → vendredi maghrib.", None),
]
for i, (t, f) in enumerate(texte, start=1):
    c = ws.cell(i, 1, t)
    c.alignment = WRAP
    if f:
        c.font = f

# 1. Mots-clés par page
MOTS = [
    ("/", "création site web Sénégal", "développeur web freelance Sénégal · agence web Dakar", "Commerciale"),
    ("/referencement-site-web-senegal/", "référencement site web Sénégal", "référencement Dakar · SEO Dakar · optimisation seo site web sénégal · référencement local Sénégal", "Commerciale"),
    ("/application-web-sur-mesure/", "application web sur mesure Sénégal", "logiciel suivi-évaluation ONG · application gestion association · outil rapport bailleur", "Commerciale"),
    ("/site-web-diaspora/", "site web diaspora sénégalaise", "créer site web Sénégal depuis la France · site web entrepreneur diaspora", "Commerciale"),
    ("/site-web-association-diaspora/", "site web association diaspora", "site web association ressortissants · gestion cotisations association", "Commerciale"),
    ("/freelance-web-kaolack/", "développeur web Kaolack", "création site web Kaolack · freelance web Kaolack", "Géo-locale"),
    ("/blog/combien-coute-un-site-professionnel/", "prix création site web Dakar", "prix site wordpress dakar · prix site web Sénégal 2026", "Info. + transactionnelle"),
    ("/blog/seo-local-senegal/", "référencement local Sénégal", "fiche Google Business Sénégal — ⚠️ renvoie vers /referencement-site-web-senegal/ (éviter la cannibalisation)", "Informationnelle"),
    ("/blog/comment-choisir-son-developpeur-web-freelance/", "choisir développeur web freelance Sénégal", "freelance web Sénégal", "Info. + commerciale"),
    ("/blog/creer-boutique-en-ligne-senegal/", "créer boutique en ligne Sénégal", "site e-commerce Sénégal · paiement Wave site", "Info. + transactionnelle"),
    ("/blog/diaspora-site-bilingue/", "site web bilingue diaspora sénégalaise", "", "Informationnelle"),
    ("/blog/wordpress-astro-webflow/", "WordPress ou Webflow", "meilleur outil site vitrine", "Informationnelle"),
]
sheet(wb, "1. Mots-clés par page",
      "Mot-clé principal du site : « création site web Sénégal ». Une requête principale par page, jamais deux pages sur la même.",
      ["Page", "Mot-clé principal", "Secondaires", "Intention", "Position au dernier relevé", "Statut"],
      [42, 34, 60, 20, 16, 14],
      [(p, k, s, i, "", "en place") for p, k, s, i in MOTS])

# 2. Feuille meta (extraite des sources)
meta = []
for f in sorted((SITE / "src" / "pages").rglob("*.astro")):
    src = f.read_text(encoding="utf-8")
    t = re.search(r'\btitle="([^"]+)"', src)
    d = re.search(r'\bdescription="([^"]+)"', src)
    at = re.search(r'\btitre:\s*"([^"]+)"', src)
    ae = re.search(r'\bextrait:\s*"([^"]+)"', src)
    if at and "article.titre" in src:  # article de blog : title calculé dans Layout
        tt, dd = f"{at.group(1)} — Blog — Saïbo Danfakha", ae.group(1) if ae else ""
    elif t:
        tt, dd = t.group(1), d.group(1) if d else ""
    else:
        continue
    rel = f.relative_to(SITE / "src" / "pages").as_posix().removesuffix(".astro")
    url = "/" if rel == "index" else "/" + rel.removesuffix("/index").removesuffix("index") + "/"
    url = url.replace("//", "/")
    ok = "oui" if len(tt) <= 70 and 120 <= len(dd) <= 165 else "à revoir"
    meta.append((url, tt, len(tt), dd, len(dd), ok))
sheet(wb, "2. Feuille meta",
      "Relevée dans le code le 15/10. Cible : title ≤ 70 caractères, description 120-165. « à revoir » = hors cible, pas forcément faux.",
      ["URL", "Title", "Long.", "Description", "Long.", "Conforme"],
      [44, 60, 7, 80, 7, 11], meta)

# 3. Calendrier
ARTICLES = [
    ("1", "Référencement Google à Dakar : par où commencer en 2026", "référencement site web Dakar"),
    ("1", "Combien coûte le référencement d'un site au Sénégal", "prix référencement Sénégal"),
    ("1", "Fiche Google Business : le guide pour une PME à Dakar", "fiche Google Business Dakar"),
    ("1", "Site WordPress à Dakar : prix, pièges et alternatives", "création site wordpress Dakar"),
    ("1", "Site web pour restaurant à Dakar : ce qu'il doit contenir", "site web restaurant Dakar"),
    ("1", "Faire créer son site au Sénégal depuis la France", "création site web Sénégal depuis la France"),
    ("1", "Site web pour cabinet médical au Sénégal", "site web cabinet médical Sénégal"),
    ("1", "Faire créer son site au Sénégal depuis l'Italie", "site web Sénégal diaspora Italie"),
    ("1", "Site web pour association de ressortissants : le guide", "site web association ressortissants"),
    ("1", "Site web pour auto-école au Sénégal", "site web auto-école Sénégal"),
    ("1", "Faire créer son site au Sénégal depuis les États-Unis ou le Canada", "site web Sénégal diaspora Amérique"),
    ("2", "Suivi-évaluation d'un projet d'ONG sans Excel", "logiciel suivi-évaluation ONG"),
    ("2", "Rapport bailleur : le produire en un clic", "rapport bailleur ONG automatique"),
    ("2", "Gérer les groupes d'épargne (AVEC) avec une application", "application gestion AVEC"),
    ("2", "Application de cotisations pour association", "application cotisations association"),
    ("2", "Outil sur mesure ou logiciel tout fait : comment choisir", "application sur mesure ou logiciel"),
    ("2", "Données des bénéficiaires : ce que demande la CDP au Sénégal", "CDP données personnelles ONG"),
    ("2", "Application de gestion pour école au Sénégal", "logiciel gestion scolaire Sénégal"),
    ("2", "Étude de cas : de dix classeurs à un outil de suivi", "outil suivi-évaluation étude de cas"),
] + [("3", "À décider — vague 3 en anglais (Canada), conditionnelle", "")] * 7
cal = []
mardi = date(2026, 10, 20)
for i, (vague, titre, kw) in enumerate(ARTICLES, start=1):
    jeudi, samedi = mardi + timedelta(days=2), mardi + timedelta(days=4)
    note = "Semaine des Awards Dëkkandoo (17/12)" if mardi == date(2026, 12, 15) else ""
    cal.append((i, vague, mardi.strftime("%d/%m/%Y"), titre, kw,
                "LinkedIn + X : l'idée de l'article en 5 lignes + lien",
                f"{jeudi:%d/%m} matin : carrousel Instagram (7 slides) + Statut WhatsApp",
                f"{samedi:%d/%m} : vidéo 9:16 TikTok + Reels (design sonore seul)", note))
    mardi += timedelta(days=7)
sheet(wb, "3. Calendrier",
      "Une ligne par semaine. Les titres se revoient chaque mois d'après le relevé Search Console.",
      ["Sem.", "Vague", "Mardi 9 h", "Article", "Mot-clé visé", "Post 1 (mardi)", "Post 2 (jeudi)", "Post 3 (samedi)", "Note"],
      [6, 7, 12, 52, 34, 34, 40, 40, 26], cal)

# 4. Suivi des publications
ws4 = sheet(wb, "4. Suivi des publications",
            "Une ligne par publication réellement faite. Ce qui n'est pas ici n'existe pas pour le bilan. La colonne « Messages reçus » est la seule qui compte.",
            ["Date", "Réseau", "Type", "Sujet / article", "Lien", "Vues (facultatif)", "Messages reçus", "Notes"],
            [12, 14, 14, 44, 40, 14, 14, 40], [("", "", "", "", "", "", "", "")] * 120)
dv = DataValidation(type="list", formula1='"Site,LinkedIn,X,Instagram,TikTok,WhatsApp Statut,WhatsApp chaîne"', allow_blank=True)
dv2 = DataValidation(type="list", formula1='"Article,Texte,Carrousel,Vidéo,Statut"', allow_blank=True)
ws4.add_data_validation(dv)
ws4.add_data_validation(dv2)
dv.add("B5:B124")
dv2.add("C5:C124")

# 5. Annuaires
ANN = [
    ("1", "Google Business Profile", "Retirer les prix de la description · vérification · 3 avis", "en cours"),
    ("1", "Bing Places", "Importer la fiche Google", "à faire"),
    ("1", "Apple Business Connect", "Accepte les entreprises sans local", "à faire"),
    ("1", "Page LinkedIn entreprise", "Site dans « Coordonnées »", "à faire"),
    ("1", "Page Facebook", "Même NAP, bouton WhatsApp", "à faire"),
    ("2", "SenPages", "Plan gratuit", "à faire"),
    ("2", "Go Africa Online", "Ne pas prendre de pack payant", "à faire"),
    ("2", "Pages Jaunes du Sénégal", "Conditions à vérifier", "à faire"),
    ("2", "Annuaire-Senegal.com", "Gratuit annoncé", "à faire"),
    ("2", "Yelu", "Offre gratuite", "à faire"),
    ("2", "Open Biz Dev", "Gratuit annoncé", "à faire"),
    ("2", "Afrikta", "Conditions à vérifier", "à faire"),
    ("2", "CCI de Kaolack", "Répertoire des adhérents ?", "à faire"),
    ("3", "AfricaShore", "Fiche freelance", "à faire"),
    ("3", "IWORKS", "Pas de prix fixes", "à faire"),
    ("3", "Malt", "Diaspora France", "à faire"),
    ("3", "Codeur.com / ComeUp", "Lien profil → portfolio", "à faire"),
    ("Lien", "Crédits en pied de page (RTZW, Dëkkandoo, Jàng, S5L…)", "Accord écrit du client", "à faire"),
    ("Avis", "Avis Google : Bangaly (Nafadji), Shabeeb, Khaly", "+ « qui d'autre autour de vous ? »", "à faire"),
]
sheet(wb, "5. Annuaires et avis",
      "Repris de SEO/CITATIONS-BACKLINKS.md (NAP à copier à l'identique). 3 inscriptions par semaine. Jamais d'option payante.",
      ["Priorité", "Plateforme", "Remarque", "Statut", "Date", "Lien de la fiche"],
      [9, 46, 46, 12, 12, 40], [(p, n, r, s, "", "") for p, n, r, s in ANN])

# 6. Rapport mensuel
mois = ["oct. 2026 (départ)", "nov. 2026", "déc. 2026", "janv. 2027", "févr. 2027", "mars 2027", "avr. 2027"]
sheet(wb, "6. Rapport mensuel",
      "1re semaine du mois. Source : Google Search Console, fenêtre 3 mois. Dernier relevé connu : 27/07/2026 = 2 clics · 96 impressions · position 20,7.",
      ["Mois", "Clics", "Impressions", "Position moy.", "Requêtes en top 10", "Articles prévus / faits", "Posts prévus / faits", "Messages entrants", "Sites référents", "Lecture"],
      [20, 8, 12, 12, 14, 16, 16, 14, 12, 50],
      [("oct. 2026 (départ)", 1, 285, 19.8, "à compter", "—", "—", "", "",
        "Relevé du 15/10 : impressions ×3 depuis juillet, page 2. 1re requête : « rédacteur web senegal » (27). 4 pages en 404 redirigées.")]
      + [(m, "", "", "", "", "", "", "", "", "") for m in mois[1:]])

OUT.parent.mkdir(exist_ok=True)
wb.save(OUT)

# Miroir texte pour les routines cloud (elles lisent le calendrier sans Excel).
md = ["# Calendrier éditorial — miroir de PLAN-VISIBILITE-2026-2027.xlsx",
      "", "Généré par `SEO/plan_visibilite.py`. Ne pas éditer à la main : modifier le script et relancer.",
      "", "## Articles (mardi 9 h)", "",
      "| Sem. | Vague | Mardi | Article | Mot-clé visé | Note |", "|---|---|---|---|---|---|"]
md += [f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} | {c[4]} | {c[8]} |" for c in cal]
md += ["", "## Mots-clés déjà pris par une page (ne pas concurrencer : y renvoyer)", "",
       "| Page | Mot-clé principal |", "|---|---|"]
md += [f"| `{p}` | {k} |" for p, k, _, _ in MOTS]
(SITE / "SEO" / "CALENDRIER.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(OUT, len(meta), "pages meta", len(cal), "semaines")
