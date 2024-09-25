#Automatiser une tache

L'application extrait dans des fichiers '.csv' par catégorie la liste et des information sur les ouvrages referencés sur le site booktoscrape.com :

Les informations recoltées sont les suivantes : 
    ● product_page_url
    ● universal_ product_code (upc)
    ● title
    ● price_including_tax
    ● price_excluding_tax
    ● number_available
    ● product_description
    ● category
    ● review_rating
    ● image_url

les champs sont séparés par des virgules dans les fichiers. les fichiers sont nommés en fonction de la catégorie des livres

Les images sont téléchargées dans un dossier files/images et avec un dossier pour chaque catégorie.

l'instalation nécessite la version 3.12 de python

pour installer l'application, il est nécessaire d'activer un environnement virtuel :
par la commande à l'intérieur du dossier :

**python -m venv env**

puis activez l'environnement grace a la commande :

sous linux ou mac :
_**source env/bin/activate**_
sous windows :
**_env\Scripts\activate.bat_**

pour installer les paquets python nécessaires tapez la commande suivante :
pip install -r requirements.txt






 