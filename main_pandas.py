import pandas as pd

# data = {
#     "noms": ["jen","jan","jean"],
#     "age": [30,20,66],
#     "sexe":["F","F","M"]
# }
#
# nom_age_sexe = pd.DataFrame(data)
# nom_age_sexe.to_csv("nom_age-sexe.csv")
# nom_age_sexe.to_excel("nom_age-sexe.xlsx")
# print(nom_age_sexe)

recettes = pd.read_json("recettes.json")
print(recettes.info())

