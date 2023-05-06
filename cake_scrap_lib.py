import os.path
import json

JSON_FILENAME = "recettes.json"

MES_INGREDIENTS = ["beurre", "beurre doux", "beurre doux mou", "beurre fondu", "beurre fondu)", "beurre mou",
                   "cannelle en poudre", "cannelle", "chocolat noir", "compote de pommes", "curcuma en poudre",
                   "eau", "farine", "farine blanche", "farine de blé", "farine de blé t65", "farine t55",
                   "flocons d’avoine", "fécule", "gingembre en poudre", "gros œufs", "huile", "huile neutre", "levure",
                   "levure boulanger", "levure chimique", "levure de boulanger", "levure de boulanger déshydratée",
                   "levure sèche", "maïzena", "miel", "miel d’acacia", "muscade", "noix de muscade", "poudre de cacao",
                   "poudre de cacao, non sucrée", "poudre à lever", "rhum", "rhum ambré", "sel", "sel fin", "sucre",
                   "sucre blanc", "sucre fin", "sésame", "tasse de sucre", "vanille", "vinaigre blanc", "œuf",
                   "œuf battu", "œuf bien battu", "œuf entier", "œuf pour dorer", "œuf+ 2 jaunes", "œufs",
                   "œufs + 1 jaune pour la pâte", "œufs + 1 œuf battu", "œufs battus", "œufs bien battus",
                   "œufs entiers", "sucre glace", "beurre ramolli", "chocolat noir à dessert", "cacao en poudre",
                   "sucre en poudre", "sucre vanillé"]


def charger_fichier_json(filename):
    if os.path.exists(filename):
        f = open(filename, "r")
        json_data = f.read()
        f.close()
        return json.loads(json_data)
    return None


def filtrer_nom_ingredient(nom_ingredient):
    filtre_gauche = False
    # 100g farine a nettoyer
    # 2 ou 3 oeufs

    index_de = nom_ingredient.find(" de ")
    if index_de != -1:
        nom_ingredient = nom_ingredient[index_de + 4:]
        filtre_gauche = True

    if not filtre_gauche:
        index_d = nom_ingredient.find(" d'")
        if index_d == -1:
            index_d = nom_ingredient.find(" d’")
        if index_d != -1:
            nom_ingredient = nom_ingredient[index_d + 3:]
            filtre_gauche = True

    if not filtre_gauche:
        nom_split = nom_ingredient.split(" ")
        if nom_split[0].isdigit() and nom_split[1] == "ou" and nom_split[2].isdigit():
            nom_ingredient = " ".join(nom_split[3:])
            filtre_gauche = True

    if not filtre_gauche:
        nom_split = nom_ingredient.split(" ")
        if nom_split[0].isdigit() and nom_split[1] == "à" and nom_split[2].isdigit():
            nom_ingredient = " ".join(nom_split[3:])
            filtre_gauche = True

    if not filtre_gauche:
        nom_split = nom_ingredient.split(" ")
        if nom_split[0].isdigit() and nom_split[1] == "g":
            nom_ingredient = " ".join(nom_split[2:])
            filtre_gauche = True

    if not filtre_gauche:
        nom_split = nom_ingredient.split(" ")
        if nom_split[0].isdigit():
            nom_ingredient = " ".join(nom_split[1:])
            filtre_gauche = True

    if not filtre_gauche:
        if nom_ingredient.startswith("du "):
            nom_ingredient = nom_ingredient[3:]
            filtre_gauche = True

    if not filtre_gauche:
        if nom_ingredient.startswith("des "):
            nom_ingredient = nom_ingredient[4:]
            filtre_gauche = True
    # filtre à droite
    index_parenthese = nom_ingredient.find("(")
    if index_parenthese != -1:
        return nom_ingredient[:index_parenthese]

    index_tiret = nom_ingredient.find(" - ")
    if index_tiret != -1:
        return nom_ingredient[:index_tiret]

    index_crochet = nom_ingredient.find(" [")
    if index_crochet != -1:
        return nom_ingredient[:index_crochet]

    return nom_ingredient


def trier_recettes_par_liste_ingredients(liste_recettes, liste_ingredients):
    # liste_recettes_sauvgardees
    # "nom_ingredients" = []
    for recette in liste_recettes:
        recette["nom_ingredients"] = [filtrer_nom_ingredient(i).lower().strip() for i in recette['recettes']['ingredients']]
        recette["ingredients_correspondants"] = [ingredient for ingredient in recette["nom_ingredients"] if ingredient in liste_ingredients]
        recette["ingredients_manquants"] = [ingredient for ingredient in recette["nom_ingredients"] if ingredient not in liste_ingredients]
        recette["score_match_ingredients"] = len(recette["ingredients_correspondants"])-(4*len(recette["ingredients_manquants"]))
        if len(recette["ingredients_correspondants"])==0:
            recette["score_match_ingredients"] -= 40
        if len(recette["ingredients_manquants"])==0:
            recette["score_match_ingredients"] += 40

    liste_recettes.sort(key=lambda x: x["score_match_ingredients"], reverse=True)
    return liste_recettes

