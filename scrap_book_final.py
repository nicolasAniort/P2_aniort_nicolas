import csv
import shutil
import urllib
import datetime
import requests
import os
from typing import List, Union, Any
from bs4 import BeautifulSoup

prefix_url_category = "https://books.toscrape.com/catalogue/category/books/"
suffix_url_category = "/index.html"
compteur: int
url_prefix_livre: str = "https://books.toscrape.com/catalogue"
url_prefixe: str = "https://books.toscrape.com/"
infos_livre_tr = []
infos_livre_categorie = []
url_rec: str
cpt_page: str
cpt_categorie: int
"""
interface de recuperation durl
"""
def recuperation_url():
    url_rec = input('Entrez l\'url à traiter : ')
    extraction_des_categories(url_rec)
    return url_rec
"""
creation de l'horodatage
"""
def horodater():

    horodate = datetime.datetime.now()
    annee = horodate.strftime("%A")
    heure = horodate.strftime("%H")
    mois = horodate.strftime("%m")
    horodatage_fichier: str = annee + heure + mois
    return horodatage_fichier
""

def extraction_des_categories(url):

    # lien de la page à scrapper
    retour = requests.get(url)
    page = retour.content
    soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
    liste_categorie =  soup.find("ul", class_="nav nav-list").find('ul').find_all('a')
    nombrecategorie = len(liste_categorie)
    a = 0
    while a < (nombrecategorie):
            url_de_categorie = url_prefixe + liste_categorie[a].get("href")
            extraction_de_page(url_de_categorie)
            a = a + 1

def extraction_de_page(url_page):
    # lien de la page à scrapper
    retour = requests.get(url_page)
    page_cat = retour.content
    # transforme (parse) le HTML en objet BeautifulSoup
    soup_cat: BeautifulSoup = BeautifulSoup(page_cat, 'html.parser')
    compteur_de_page(soup_cat, url_page)

    return url_page

def extractionlistelivre(nombrepagenum: int, soup_cat, url_rec: str):
    """
        recuperation d'un objet soup contenant les <a> de la categorie product_pod
    """
    soup_list_: BeautifulSoup = []
    """
    Si la categorie compte un nombre de page supérieur à 1
    """
    a = 1
    if int(nombrepagenum) > 1 :
        #initalisation du compteur de boucle
        nombredeligne_brute: int
        """
        tant que le compteur de boucle "a" est inférieur au nombre de page + 1
        """
        while a <= (int(nombrepagenum)):

            for a in range(int(a),int(nombrepagenum)):
                reponse = requests.get(url_rec.replace("index.html","page-" + str(a) + ".html"))
                page_cat = reponse.content
                soup_cat: BeautifulSoup = BeautifulSoup(page_cat, 'html.parser')
                soup_list_article = soup_cat.find("article", class_="product_pod")
                soup_list_a_brute = soup_list_article.find_all_next('a')
                if a==1 :
                    nombredeligne_brute: int = len(soup_list_a_brute)
                else:
                    nombredeligne_brute = nombredeligne_brute +  len(soup_list_a_brute)
            a = a + 1
            """
            bloc de recuperation des url relatives de livres
            """
            for i in range(0, nombredeligne_brute):
                if i == 0 :
                    balise_a = soup_list_a_brute[i]
                    attribut_href = balise_a['href']
                    soup_list_.append(str(attribut_href))
                elif i%2 == 0:
                    balise_a = soup_list_a_brute[i]
                    attribut_href = balise_a['href']
                    soup_list_.append(str(attribut_href))
            """
            tant que le l'on est pas arrivé à la derniere page de la categorie
            """
            if (int(nombrepagenum) > a):
                """ boucles de recuperation de la liste de livres et des information des livres"""
                nombredeligne: int = len(soup_list_)
                cptour = 0
                for j in range(0, nombredeligne):
                    """ Condition si la liste est inferieure 20 livres """
                    if (nombredeligne != 0) :
                        # nom de categorie
                        categorie: str = url_rec.replace("https://books.toscrape.com/catalogue/category/books/", "").replace(
                            "/index.html", "")
                        categories = categorie
                        # creation de l\'url du livre
                        cleaner_url_livre: str = soup_list_[j]
                        product_page_urls = cleaner_url_livre.replace('../../..', str(url_prefix_livre))
                        reponse = requests.get(product_page_urls)
                        page_cat = reponse.content
                        # transforme (parse) le HTML en objet BeautifulSoup
                        soup = BeautifulSoup(page_cat, 'html.parser')
                        #appel de la definition d'extraction des informations du livre
                        information_livre = []
                        information_livre = etl(product_page_urls,soup)
                        upc = information_livre[1]
                        title =information_livre[2]
                        price_including_tax = information_livre[3]
                        price_excluding_tax = information_livre[4]
                        number_available = information_livre[5]
                        product_description = information_livre[6]
                        category = information_livre[7]
                        review_rating = information_livre[8]
                        image_url = information_livre[9]
                        # construction des lignes par livre
                        infos_livre_categorie.append([categories, product_page_urls, upc, title, price_including_tax,
                                                 price_excluding_tax, number_available, product_description, category,
                                                 review_rating, image_url])
                        a =  cptpage + 1

            elif a == (int(nombrepagenum)):
                    nombredeligne: int = len(soup_list_)
                    cptpage = a
                    # lien de la page à scrapper fabriquer en modifiant le suffixe index.html par page-x.html
                    reponse = requests.get(url_rec.replace("index.html", "page-" + str(cptpage) + ".html"))
                    page_cat = reponse.content
                    # transforme (parse) le HTML en objet BeautifulSoup
                    soup_cat: BeautifulSoup = BeautifulSoup(page_cat, 'html.parser')
                    # recuperation d'un objet soup contenant les <a> de la categorie product_pod
                    soup_list_article = soup_cat.find("article", class_="product_pod")
                    # soup_mlis-a_multi contient toutes les url relatives des livres en double
                    soup_list_a_brute = soup_list_article.find_all_next('a')
                    # on obtient le nombre de ligne d'url récupérées dans nombredeligne_brute
                    nombredeligne_brute: int = len(soup_list_a_brute)
                    if nombredeligne_brute > 38:
                        nombredeligne_brute = 38
                    else:
                        nombredeligne_brute = nombredeligne_brute
                    print('nombredeligne')

                    for j in range(0, nombredeligne):
                        if (j < (nombredeligne)) :

                            # nom de categorie
                            categorie: str = url_rec.replace("https://books.toscrape.com/catalogue/category/books/",
                                                             "").replace(
                                "/index.html", "")
                            categories = categorie
                            # url du livre
                            cleaner_url_livre: str = soup_list_[j]
                            product_page_urls = cleaner_url_livre.replace('../../..', str(url_prefix_livre))
                            try:
                                reponse = requests.get(product_page_urls)
                            except:
                                j = j + 1
                            page_cat = reponse.content
                            # transforme (parse) le HTML en objet BeautifulSoup
                            soup = BeautifulSoup(page_cat, 'html.parser')
                            information_livre = etl(product_page_urls, soup)
                            upc = information_livre[1]
                            title = information_livre[2]
                            price_including_tax = information_livre[3]
                            price_excluding_tax = information_livre[4]
                            number_available = information_livre[5]
                            product_description = information_livre[6]
                            category = information_livre[7]
                            review_rating = information_livre[8]
                            image_url = information_livre[9]
                            # construction des lignes par livre
                            infos_livre_categorie.append([categories, product_page_urls, upc, title, price_including_tax, price_excluding_tax, number_available, product_description,
                                                          category,review_rating, image_url])
                        a = int(nombrepagenum)
            #construction de l'entete
            en_tete = ["categories", "urls", "upcs", "titre", "prix TTC", "prix HT", "nombre de livres disponibles", "description",
                       "categories", "nombre d'étoile", "url de l'image de couverture"]
            #construction des lignes par livre
            compt = int(len(infos_livre_categorie))
    else:
            """ 
            Bloc de traitement des page livre s'il n'y a qu'une page dans la catégorie
            
            """
            reponse = requests.get(url_rec)
            page_cat = reponse.content
            # transforme (parse) le HTML en objet BeautifulSoup
            soup_cat: BeautifulSoup = BeautifulSoup(page_cat, 'html.parser')
            # recuperation d'un objet soup contenant les <a> de la categorie product_pod
            soup_list_article = soup_cat.find("article", class_="product_pod")
            soup_list_a_brute = soup_list_article.find_all_next('a')
            nombredeligne_brute: int = len(soup_list_a_brute)

            for i in range(0, nombredeligne_brute):

                if i == 0:

                    balise_a = soup_list_a_brute[i]
                    attribut_href = balise_a['href']
                    soup_list_.append(str(attribut_href))
                elif i%2 == 0:

                    balise_a = soup_list_a_brute[i]
                    attribut_href = balise_a['href']
                    soup_list_.append(str(attribut_href))

            nombredeligne = len(soup_list_)

            for j in range(0, nombredeligne):
                if (j < (nombredeligne)):

                    # nom de categorie
                    categorie: str = url_rec.replace("https://books.toscrape.com/catalogue/category/books/", "").replace(
                        "/index.html", "")
                    categories = categorie
                    # url du livre
                    cleaner_url_livre: str = soup_list_[j]
                    product_page_urls = cleaner_url_livre.replace('../../..', str(url_prefix_livre))
                    reponse = requests.get(product_page_urls)
                    page_cat = reponse.content
                    # transforme (parse) le HTML en objet BeautifulSoup
                    soup = BeautifulSoup(page_cat, 'html.parser')
                    information_livre = []
                    information_livre = etl(product_page_urls,soup)
                    upc = information_livre[1]
                    title =information_livre[2]
                    price_including_tax = information_livre[3]
                    price_excluding_tax = information_livre[4]
                    number_available = information_livre[5]
                    product_description = information_livre[6]
                    category = information_livre[7]
                    review_rating = information_livre[8]
                    image_url = information_livre[9]
                    # construction des lignes par livre
                    infos_livre_categorie.append([categories, product_page_urls, upc, title, price_including_tax,
                                             price_excluding_tax, number_available, product_description, category,
                                             review_rating, image_url])


            #construction de l'entete
            en_tete = ["categories", "urls", "upcs", "titre", "prix TTC", "prix HT", "nombre de livres disponibles", "description",
            "categories", "nombre d'étoile", "url de l'image de couverture"]
            #construction des lignes par livre
            compt = int(len(infos_livre_categorie))

    # Génération du fichier csv
    charger_donnees("donnees_categorie_" + "-" + category + "-" + horodater() + ".csv", en_tete, compt, infos_livre_categorie)

def compteur_de_page(soup_cat: BeautifulSoup, url_page):

    """
    charger les données dans un fichier csv
    Si la classe pager existe, il y a plusieurs pages, on va donc
    compter le nombre de pages à traiter pour la categorie concernée
    """
    vide=[]
    pager = soup_cat.select(".pager")
    if pager != vide:
        li_current: str = soup_cat.find(class_="current").text.replace("\n", "").replace(" ", "")
        taille_chaine = len(li_current)
        placeof = li_current.index('of')
        nbpagenum: int = li_current[(placeof + 2):taille_chaine]
        extractionlistelivre(nbpagenum, soup_cat, url_page)
    else:
        nbpagenum = 1
        extractionlistelivre(nbpagenum, soup_cat, url_page)

def charger_donnees(nom_fichier, en_tete, compt, infos_livre_categorie):

    """
    On crée un fichier, on cree les entetes, et on alimente les colonnes lignes par lignes
    """
    with open(nom_fichier, 'w', newline='') as fichier_csv:

        try:
            #creation du csv
            writer = csv.writer(fichier_csv, delimiter=',')
            #creation de la ligne d'entete du fichier
            writer.writerow(en_tete)
            #compteur recevant le nombre de livre
            cpt = int(compt)

            for i in range(0, cpt):
                writer.writerow(infos_livre_categorie[i])

            fichier_csv.close()
            infos_livre_categorie.clear()
        except:

            fichier_csv.close()
            infos_livre_categorie.clear()
#recuperation des infos d'un livre
def etl(url,soup):

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = soup

    # récupération de L'url de la page du produit
    product_page_urls = url
    # récupération de l'upc
    try:
        upc = soup.find("th", text="UPC").find_next_sibling("td").text
    except:
        upc ='donnée manquante'
    # récupération du titres ok
    try:
        title = soup.find("h1").text
    except:
        title ='donnée manquante'
    # récupération du prix TTC
    try:
        price_including_tax = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").text
        price_including_tax: str = price_including_tax
    except:
        price_including_tax ='donnée manquante'
    # récupération du prix HT
    try:
        price_excluding_tax = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text
        price_excluding_tax: str = price_excluding_tax
    except:
        price_excluding_tax = 'donnée manquante'
    # récupération du nombre disponible
    try:
        chaine_nombre_stock: str = soup.find("th", text="Availability").find_next_sibling("td").text
        loc_debut_chaine: int = chaine_nombre_stock.find('(') + 1
        loc_fin_chaine: int = chaine_nombre_stock.find(' available)')
        number_available: int = chaine_nombre_stock[loc_debut_chaine: loc_fin_chaine]
        number_available: str = number_available
    except:
        number_available = 'donnée manquante'
    # récupération de la descriptions ok
    try:
        product_description = soup.find("p", class_="").text
    except:
        product_description = 'donnée manquante'
    # récupération de la categorie du produit prendre les li à l'envers
    try:
        category = soup.find("a", text="Books").find_next("a").text
    except:
        category ='donnée manquante'
    # récupération de review rating
    balise_etoile = soup.find("p", class_="instock availability").find_next("p").attrs
    class_etoile: str = balise_etoile['class']
    chaine_class_etoile = class_etoile[1]
    if chaine_class_etoile == 'Five':
        review_rating = 5
    elif chaine_class_etoile == "Four":
            review_rating = 4
    elif chaine_class_etoile == 'Three':
            review_rating = 3
    elif chaine_class_etoile == 'Two':
            review_rating = 2
    elif chaine_class_etoile == 'One':
            review_rating = 1
    else:
        review_rating = 0
    review_rating: str = review_rating
    # récupération de l'url de l'image
    div_img_tag = soup.find("div", class_="item active")
    image = div_img_tag.img
    image_url_brute = image['src']
    image_url = image_url_brute.replace('../..', 'https://books.toscrape.com')
    #telechargement de l'image dans un dossier
    prefixe_dir = 'img_livre' + '_'+ horodater() + '/'
    file_img_libre = prefixe_dir + category +'_'+upc + '.jpg'
    try:
        os.mkdir(prefixe_dir)
    except:
        prefixe_dir = prefixe_dir

    #telechargement de l'image et creation du fichier en local
    urllib.request.urlretrieve(image_url, file_img_libre)

    infos_livre = [product_page_urls, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]

    return infos_livre
"""
creation d'un objet soup à partir de lurl saisie
renvoi de l'objet à la def compteur_de_page
"""
# lanceur
extraction_des_categories(recuperation_url())