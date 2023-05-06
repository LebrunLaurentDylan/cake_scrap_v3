import pandas as pd
from cake_scrap_lib import *

liste_recettes_sauvegardees = charger_fichier_json(JSON_FILENAME)
liste_recettes_sauvegardees = trier_recettes_par_liste_ingredients(liste_recettes_sauvegardees, MES_INGREDIENTS)


recettes_a_exporter = []
for recettes in liste_recettes_sauvegardees:
    ingredients = recettes["recettes"]["ingredients"]
    ingredients_str = ", ".join(ingredients)
    recettes_a_exporter.append({"titre": recettes["titre"], "ingredients": ingredients_str, "url": recettes["url"]})
recettes_a_exporter_dataframe = pd.DataFrame(recettes_a_exporter)
# print(recettes_a_exporter_dataframe.loc[0])
recettes_a_exporter_dataframe.to_csv("recettes.csv")
recettes_a_exporter_dataframe.to_excel("recettes.xlsx")

# extraire recettes.json
# titre / ingredients / url
# utiliser (join) pour les ingredients
# exporter au format .csv avec pandas --> "recettes.csv" ou .xlsx

# recettes = pd.read_json("recettes.json")
# recettes_csv = {"titre": "",
#                 "ingredients": "",
#                 "url": ""}
# for r in recettes:
#     ingredient_join = ",".join(r["recettes"]["ingredients"])
#     recettes_csv["titre"].append(r["titre"])
#     recettes_csv["ingredients"].append(ingredient_join)
#     recettes_csv["url"].append(r["url"])

