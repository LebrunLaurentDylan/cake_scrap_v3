# PROJET 3 : Cake scrap v3

## Projet guidé dans le cadre d'un cours sur le web-scraping :

Description du projet en trois parties : 

*"Vous allez apprendre le scraping, pour extraire des informations à partir de pages web (HTML).*

*Vous n'avez pas besoin de connaitre le langage HTML pour suivre ce projet.*

*Nous allons extraire des recettes de gateaux et donner à notre algorithme la liste des ingrédients que l'on possède chez nous (farine, sucre, oeufs...). Celui ci nous proposera une liste de recette que l'on peut réaliser en fonction des ingrédients.*

*Vous verrez, c'est pratique !*

*Vous apprendrez aussi : à utiliser Requests, Beautifulsoup, et Pandas pour extraire vos données au format Excel."*

Dans cette partie du projet, nous utilisons un site public réel cuisine-libre.org pour récupérer les recettes et les stocker dans un fichier json et éviter de les re-scraper à chaque appel du programme. Puis nous allons nous servir des données des recettes et d'une liste d'ingredient que nous possédons pour faire une comparaison entre eux et demander au programme de nous proposer des recettes en lien avec les ingredients que nous possédons. 

