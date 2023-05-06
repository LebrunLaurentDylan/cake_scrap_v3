from cake_scrap_lib import *


def afficher_liste_recettes(liste_recettes):
    for i in range(len(liste_recettes)):
        recette = liste_recettes[i]
        ingredients = recette['recettes']['ingredients']
        print(i+1, "-", recette["titre"], "(nb_ingredient :", str(len(ingredients)) + ")", "-", recette['url'])


liste_recettes_sauvegardees = charger_fichier_json(JSON_FILENAME)
if not liste_recettes_sauvegardees:
    print("erreur, aucune donnée")
    exit(0)

print(f"nombre de recettes: {len(liste_recettes_sauvegardees)}\n")
afficher_liste_recettes(liste_recettes_sauvegardees)

# def afficher_liste_recettes(liste_recettes):
#     for recettes in liste_recettes:
#         print(f"titre: {recettes['titre']}\n url: {recettes['url']}\n url_image: {recettes['picture_url']}\n"
#               f"recette:\n\
#               infos : \n\
#                 {recettes['recettes']['infos']}\n\
#               ingredients : \n\
#                 {recettes['recettes']['ingredients']}\n\
#               Etapes  :\n\
#                 {recettes['recettes']['etapes']}")
