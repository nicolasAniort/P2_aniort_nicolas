# Books scraping 


Ce script sert à effectuer le scraping de données depuis le site Books to Scrape. 
Lors de son exécution, il va générer un fichier csv par catégorie de livre , à partir d'une URL spécifique, qui va 
permettre d'enregistrer certaines de leurs données (product_page_url,upc,title,price_including_tax,price_excluding_tax,
number_available,product_description,category,review_rating,image_url) dans un fichier au format CSV.
Il générera aussi un dossier contenant toutes les images de couverture des ouvrages.

## Installation :

### Téléchargement des fichiers depuis un dépôt distant dans le dossier "/Users/user_name/documents" :

''' 
- $ cd /Users/user_name/documents
- $ git clone https://github.com/nicolasAniort/P2_aniort_nicolas.git custom_project_name
- $ cd custom_project_name
'''
### Création d'un environnement virtuel nommé "env" :
''' 
- $ python -m venv env
'''
### Activation de l'environnement :
''
- $ source env/bin/activate # OSX 
- $ source env/Scripts/activate # Windows
''
### Installation des packages nécessaire depuis le fichier "requirements.txt" :
'' 
- $ pip install -r requirements.txt
''
## Utilisation :

### Exécution du script :
''
- $ python scrap_book_final.py
''
Le script va alors demander à l'utilisateur une URL à utiliser.

Pour l'utiliser, si l'utilisateur appuie sur la touche "ENTER", le script utilisera une url d'exemple de livre :

Please, insert the URL to scrape : https://books.toscrape.com/
