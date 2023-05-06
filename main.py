import os.path
import requests
from bs4 import BeautifulSoup
import json
from cake_scrap_lib import *
# Chercher user_agent sur navigateur pour trouver celui qui correspond et s'en servir après dans requests
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.4044.113 "
                         "Safari/5370.36 Brave/5035"}

# -------------URLS TESTS------------- #
# url = "https://www.cuisine-libre.org/gateau-au-chocolat-granuleux"
# url = "https://www.cuisine-libre.org/gateau-au-miel-de-litha"
# url = "https://www.cuisine-libre.org/soft-a-la-pomme"
# url = "https://www.cuisine-libre.org/tartelettes-aux-myrtilles"

BASE_URL = "https://www.cuisine-libre.org/"
JSON_EXCLUDE_FILENAME = "recettes_exclues.json"


def telecharger_et_sauvegarder_image(url):
    response = requests.get(url)
    filename = url.split("/")[-1]
    index_point_interrogation = filename.find("?")
    if index_point_interrogation != -1:
        filename = filename[:index_point_interrogation]
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)


def nettoyer_text(t):
    return t.replace("\xa0", " ").replace("\n", "").strip()


def decoder_caracter_unicode(s):
    return s.encode().decode("unicode-escape")


def extraire_duree_recette(recipe_infos_p, class_name):
    span = recipe_infos_p.find("span", class_=class_name)
    duree = span.find("time").text if span else "Ya pas"
    return nettoyer_text(duree).replace("?", "")


def extraire_info_recette(url):
    response = requests.get(url, headers=HEADERS) # headers=HEADERS : parametre important pour se faire passer
    # pour un navigateur
    soup = BeautifulSoup(response.text, "html.parser")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        titre = nettoyer_text(str(soup.find("h1").contents[0]))
        print("titre:", titre)
    else:
        print(f"Error Status {response.status_code} biatch !")

    license_footer = soup.find("footer", id='license')
    if license_footer:
        license_text = license_footer.text
        license_valide = "cc0" in license_text.lower() or "domaine public" in license_text.lower()
    if not license_footer or not license_valide:
        return None

    recipe_infos_p = soup.find("p", id="recipe-infos")
    # duree_preparation = recipe_infos_p.find("time", class_="article-duree_preparation-2628").text
    duree_preparation = extraire_duree_recette(recipe_infos_p, "duree_preparation")
    duree_cuisson = extraire_duree_recette(recipe_infos_p, "duree_cuisson")
    duree_repos = extraire_duree_recette(recipe_infos_p, "duree_repos")
    methode_cuisson_a = recipe_infos_p.find("a")
    methode_cuisson = methode_cuisson_a.text if methode_cuisson_a else ""

    infos = {"duree_preparation": duree_preparation,
             "duree_cuisson": duree_cuisson,
             "duree_repos": duree_repos,
             "methode_cuisson": methode_cuisson}

    div_ingredients = soup.find("div", id="ingredients")
    ingredients_li = div_ingredients.find_all('li', class_='ingredient') if div_ingredients else ""
    ingredients = [nettoyer_text(i.text) for i in ingredients_li if not i.find("i")]

    div_preparation = soup.find("div", id="preparation")
    preparation_steps = div_preparation.find_all("p") if div_preparation else None
    if preparation_steps:
        steps = [nettoyer_text(step.text) for step in preparation_steps]
    else:
        preparation_steps = div_preparation.find_all("li") if div_preparation else None
        steps = [nettoyer_text(step.text) for step in preparation_steps]

    recette = {"titre": titre,
               "infos": infos,
               "ingredients": ingredients,
               "etapes": steps}
    # print("\nInfos", infos)
    # print("\nIngredients:", ingredients)
    # print("\nEtapes:", steps)
    # print("\nrecette:", recette)
    return recette


def extraire_liste_recettes(url, url_exclues = None):
    # {"titre": "", "url": "", "picture_url": ""}
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    div_recettes = soup.find("div", id="recettes")
    ul_recettes = div_recettes.find("ul", recursive=False)
    li_recettes = ul_recettes.find_all("li")

    nouvelles_url_a_exclure = []

    recettes_info = []
    for li in li_recettes:
        a = li.find("a")
        strong = a.find("strong")
        titre = nettoyer_text(strong.text)
        url = BASE_URL + a["href"]
        img = a.find("img")
        picture_url = BASE_URL + img["src"]

        if url_exclues and url in url_exclues:
            continue

        recettes = extraire_info_recette(url)
        if recettes:
            recettes_info.append({"titre": titre, "url": url, "picture_url": picture_url, "recettes": recettes})
        else:
            nouvelles_url_a_exclure.append(url)

    return recettes_info, nouvelles_url_a_exclure





def sauvegarder_fichier_json(filename, data):
    json_data = json.dumps(data)
    f = open(filename, "w")
    f.write(json_data)
    f.close()


liste_recettes_sauvegardees = charger_fichier_json(JSON_FILENAME)
if not liste_recettes_sauvegardees:
    liste_recettes_sauvegardees = []

url_recettes_a_exclure_sauvegardees = charger_fichier_json(JSON_EXCLUDE_FILENAME)
if not url_recettes_a_exclure_sauvegardees:
    url_recettes_a_exclure_sauvegardees = []


url_recette_a_exclure = [r["url"] for r in liste_recettes_sauvegardees]
url_recette_a_exclure.extend(url_recettes_a_exclure_sauvegardees)

url = "https://www.cuisine-libre.org/boulangerie-et-patisserie?mots%5B%5D=83&mots%5B%5D=&max=300"
liste_recettes, nouvelles_url_a_exclure = extraire_liste_recettes(url, url_recette_a_exclure)
liste_recettes_sauvegardees.extend(liste_recettes)
liste_recettes = liste_recettes_sauvegardees
print(liste_recettes)
print(len(liste_recettes))

# sauvegarder les donnees
sauvegarder_fichier_json(JSON_FILENAME, liste_recettes)
url_recettes_a_exclure_sauvegardees.extend(nouvelles_url_a_exclure)
sauvegarder_fichier_json(JSON_EXCLUDE_FILENAME, url_recettes_a_exclure_sauvegardees)


# for r in liste_recettes:
#     telecharger_et_sauvegarder_image(r["picture_url"])



