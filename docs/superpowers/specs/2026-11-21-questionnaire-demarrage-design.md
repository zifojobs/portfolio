# Design : le questionnaire de démarrage (« Démarrer avec Saïbo »)

**Date :** 2026-11-21 (brainstorming du soir, avec Saïbo)
**Projet :** portfolio `saibodanfakha.com` (Astro 6, statique, Vercel) + agent WhatsApp (`agent.saibodanfakha.com`, VPS)
**Premier client :** une société de sécurité privée à Dakar (dossier du client : `<dossier du client>\`, hors dépôt).
**Maquette validée :** `<dossier du client>\.superpowers\brainstorm\…\content\parcours.html` (3 écrans).

> ⚠️ Ce dépôt est **public**. Ce document ne contient aucune donnée de client (nom, numéro, NINEA, budget).

## 1. L'intention

Avant un devis, Saïbo envoie à son client un lien. Le client répond seul, sur son téléphone, aux questions de cadrage.
**Ce n'est pas un formulaire : c'est le premier livrable.** Le client doit vivre une expérience. À la fin, il doit
**sentir le professionnalisme** et se dire : **« je veux travailler avec cette personne »** (Saïbo, 21/11).

- **Objectifs** : récolter les réponses de cadrage complètes · impressionner · servir **pour tous les clients**.
- **Non-objectifs** : pas de devis ni de prix dans le parcours · pas de compte client · pas de maquette de site.
- **Anti-objectifs** (échec même si ça marche) : une réponse perdue sans que Saïbo le sache · des données client dans le
  dépôt public · une promesse faite au client avant le devis · un parcours qui ressemble à un Google Forms.

## 2. Les approches considérées

| | Approche | Bilan |
|---|---|---|
| A | Une conversation avec Saïbo (une question par écran, sa photo, le « pourquoi » sous chaque question) | Sérieux, réutilisable, mais pas d'effet « waouh » |
| B | Le site du client se dessine en direct pendant qu'il répond | Effet le plus fort, mais lourd par client et promet un résultat avant le devis |
| **C ✅** | **A + une carte de projet qui se remplit en direct + un dossier de démarrage à la fin** | **Choisi par Saïbo** : le « waouh » de B sans son poids ni ses promesses |

## 3. Le parcours (validé sur maquette)

1. **Une question par écran** : en haut, la photo et le nom de Saïbo + « question n sur N » + barre d'avancement.
   Sous la question, un encadré **« Pourquoi je vous le demande »** (une phrase, ton de Saïbo, vouvoiement).
   Réponses surtout **à toucher** (choix, puces), peu de texte à taper. **8 minutes maximum.**
2. **La carte de projet** (bas de l'écran) : vide au départ, elle se remplit à chaque réponse : nom de la société,
   logo et couleurs, services, zones. Le dernier ajout est mis en valeur (pastille de la couleur d'accent).
3. **Au clic « Envoyer »**, la carte **s'agrandit et devient le dossier de démarrage** : la page à son nom (date, ce
   qu'il a dit, le chemin en étapes, « je reviens vers vous sous 48 h »). Bouton **« Enregistrer mon dossier »**
   (image PNG, facile à garder et partager sur WhatsApp).
4. **Bonus** : bouton facultatif **« Envoyer aussi à Saïbo sur WhatsApp »** (lien `wa.me` vers le numéro de Saïbo,
   message pré-rempli avec le résumé). Le client appuie lui-même sur Envoyer ; la discussion s'ouvre entre eux.

## 4. Réception des réponses (décidé par Saïbo : WhatsApp + mail en filet)

Le navigateur envoie le dossier (JSON) à **`https://agent.saibodanfakha.com/dossier`** (serveur de Saïbo). L'agent :
1. **écrit une copie sur disque** (un fichier par dossier, hors de tout dépôt) : rien ne se perd, même si les envois ratent ;
2. **prévient Saïbo sur WhatsApp** par un **modèle de message approuvé par Meta** (passe à toute heure, hors fenêtre
   de 24 h) : « Nouveau dossier : {société} · {prénom} » + le résumé ;
3. **envoie le dossier complet par mail** à Saïbo.

Le navigateur n'affiche « Envoyé » qu'après la réponse 200 de l'agent ; sinon, message d'erreur clair et bouton
« Réessayer », la saisie reste en place (sauvegarde locale du brouillon pendant le parcours).

## 5. Réutilisable pour tous les clients

- **Le moteur est unique**, les **jeux de questions sont des données** (un fichier par type de mission ; le premier :
  « visibilité : réseaux + site », variante sécurité privée).
- **Lien personnalisé facultatif** : Saïbo prépare pour un client un lien non devinable qui ouvre le parcours déjà à ses
  couleurs, avec son logo (« Bonjour <prénom> ») et le bon jeu de questions. Sans lien personnalisé, le client choisit
  sa couleur et peut déposer son logo.
- Adresse : `saibodanfakha.com/demarrer/…`, **hors sitemap, `noindex`**.

## 6. Contraintes

- **Données** : jamais dans le dépôt public ni dans les journaux Vercel ; le minimum de champs (loi n° 2008-12) ; la
  configuration d'un lien personnalisé ne contient que prénom, nom de société, logo, couleurs, jeu de questions.
- **Sécurité** (règle du hub : outil à données ⇒ relecture par un agent séparé avant la mise en prod) : l'endpoint
  `/dossier` accepte seulement l'origine `saibodanfakha.com`, limite la taille et la fréquence, valide le JSON contre
  le jeu de questions, et n'exécute rien de ce qu'il reçoit (le résumé WhatsApp est du texte, coupé à la longueur permise).
- **Charte** : nouvelle direction du portfolio (Schibsted Grotesk, `marque\CHARTE.md`) ; les couleurs du client ne
  vivent que dans la carte et le dossier. Couleurs propres au portfolio : encore à décider ⇒ neutres en attendant.
- **Téléphone d'abord** (lien reçu sur WhatsApp), puis ordinateur. Pas de musique, aucun son.
- **Déploiement** : par git uniquement ; l'agent se met à jour sur le VPS selon sa procédure.

## 7. Le premier jeu de questions : « visibilité, sécurité privée »

> 🔄 **Modifié par Saïbo le 22/11 (validation des questions)** : les questions 3 (NINEA/RCCM), 4 (autorisation) et 10
> (parcours à l'étranger) sont retirées. La 12 devient « Avez-vous des photos de votre société à montrer ? » : ce que le
> client a déjà (équipe, agents, locaux, véhicules, formations, rien), sinon comment en avoir (son téléphone, un
> photographe qu'il connaît, des images d'illustration en attendant). Saïbo n'est pas photographe. Il reste 10 questions.

Repris des 11 questions de `<plan de visibilité du client>` §6, réécrites pour qu'il réponde seul. *(pourquoi)* · [format]

1. Votre prénom et votre nom. *(pour vous écrire à votre nom)* [texte, prérempli si lien personnalisé]
2. Le nom officiel de votre société. *(votre domaine sera enregistré à son nom, jamais au mien)* [texte] ⇒ carte
3. Votre NINEA et votre RCCM. *(indispensables pour le domaine et les mentions légales du site)* [texte · « je les envoie plus tard »]
4. Votre autorisation d'exercer : obtenue / en cours / pas encore, et sa référence. *(rien de public ne sort avant
   qu'elle soit obtenue : c'est votre crédibilité)* [choix + texte facultatif]
5. Le numéro que verront vos clients (WhatsApp Business et site). *(il sera partout : il doit être celui de la société)*
   [une ligne dédiée à créer · un numéro existant]
6. Vos services. *(chacun aura sa place sur votre page)* [puces : sécurité privée · télésurveillance · sécurité
   incendie · rondes et gardiennage · autre] ⇒ carte
7. Vos formations, et ce que veut dire « SST » sur vos supports. *(je n'écris rien que vous n'avez pas confirmé)*
   [puces + texte ; durée, public, places, lieu : « je précise » ou « sur demande »]
8. Les zones que vous couvrez. *(pour que Google vous montre aux bonnes personnes)* [puces de villes + autre] ⇒ carte
9. Vos clients prioritaires. *(on parle d'abord à ceux qui vous font vivre)* [puces : entreprises · commerces ·
   événements · banques et hôtels · ONG · particuliers]
10. Votre parcours à l'étranger : avez-vous des justificatifs à montrer ? *(c'est votre meilleure preuve ; on ne la
    publie qu'avec eux)* [oui · certains · pas encore]
11. Qui répondra aux messages, et sous quel délai ? *(un client qui attend part chez le concurrent)* [choix]
12. La séance photo : quel jour, et qui est d'accord pour apparaître ? *(de vraies photos, avec l'accord écrit de
    chacun)* [choix de jours + texte]
13. Votre budget de départ et votre budget par mois. *(pour vous proposer ce qui vous sert, sans rien de superflu)*
    [tranches à toucher · « je préfère en parler »] — **toujours la dernière question**

## 8. Ce qui reste au constructeur

L'enchaînement exact des animations (carte → dossier) · les tranches de budget (à faire valider par Saïbo, cohérentes
avec la grille publique) · le texte du modèle WhatsApp à soumettre à Meta · le moyen d'envoi du mail depuis le VPS ·
la forme du lien personnalisé · le format de la copie sur disque.

## 9. Calls de Claude (à vérifier par Saïbo)

Questionnaire de 13 questions (11 du plan + prénom + numéro public séparé) · budget en dernier · PNG plutôt que PDF pour
le dossier · lien personnalisé facultatif · l'endpoint sur l'agent (VPS) plutôt qu'une fonction Vercel (le portfolio
reste statique, les données restent chez Saïbo) · `noindex` · brouillon sauvegardé dans le navigateur pendant le parcours.
