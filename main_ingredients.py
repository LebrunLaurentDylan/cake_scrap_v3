from cake_scrap_lib import *

liste_recettes_sauvegardees = charger_fichier_json(JSON_FILENAME)
if not liste_recettes_sauvegardees:
    print("erreur, aucune donnée")
    exit(0)


# 1-récupérer tous les ingredients dans une seule liste
# 2-nettoyer les ingrédients --> isoler le nom

# 3-mes ingredients = ["sucre","pomme","fuck de chiasse",...]
# 4-Algorithme pour lister les recettes correspondantes à nos ingrédients

# parcourir (for) toutes les recettes
# tous_les_ingrédients = []


liste_recettes_sauvegardees = trier_recettes_par_liste_ingredients(liste_recettes_sauvegardees, MES_INGREDIENTS)

for i in range(len(liste_recettes_sauvegardees)):
    recette = liste_recettes_sauvegardees[i]
    print(i+1, " - ", recette["titre"], " - URL:", recette["url"], "score: ", recette["score_match_ingredients"])
    print("ingrédient disponibles: ", recette["ingredients_correspondants"])
    print("ingrédient indisponibles: ", recette["ingredients_manquants"], "\n")


