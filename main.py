import csv
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"

def scrapbook(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content,"html.parser")
    book={}
    book["product_page_url"]=url

    #extraction du title du livre
    book["title"] = soup.find('h1').get_text()

    #extraction de l'url de l'image
    image = soup.find('img')
    image = image['src']
    book["image_url"] = "https://books.toscrape.com/" + image.replace("../../", "")


    #extraction de la description du livre
    description = soup.find('div',id="product_description")
    book["product_description"] = description.find_next('p').get_text()

    #extraction des donnees du tableau du livre
    table = soup.find('table')

    informations = []
    for info in table:
        information = info.find('td')
        if information != -1:
            informations.append(information.text)

    book["price_including_tax"] = informations[3]
    book["price_excluding_tax"] = informations[2]
    book["universal_product_code"] = informations[0]

    #récuperer la valeur numérique du stock dans la string et la convertir
    stock_text = re.findall(r'\d+',informations[5])
    stock = stock_text[0]
    book["number_available"] = int(stock)

    #récuperer la class star rating
    note = soup.find('p', class_=re.compile(r'^star-rating')).get('class')[1]
    match note:
        case 'One':
            book["review_rating"] = 1
        case 'Two':
            book["review_rating"] = 2
        case 'Three':
            book["review_rating"] = 3
        case 'Four':
            book["review_rating"] = 4
        case 'Five':
            book["review_rating"] = 5
        case _:
            book["review_rating"] = 0

    #recuperer la catégorie du livre
    categorie = soup.find('li').find_next('li').find_next('li')
    categorie = categorie.get_text()
    book["category"] = categorie.replace("\n", "")
    return book

livre = scrapbook(url)

ordre_cles=['product_page_url',
            'universal_product_code',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url']

#Création fichier csv
filename = "fichier.csv"
with open(filename,'w',newline='') as fichier:
    writer=csv.writer(fichier, delimiter=",")

#Insertion en tete
    writer.writerow(ordre_cles)

#Insertion données
    writer.writerow([livre[cle] for cle in ordre_cles])


url_category = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# extraire les urls d'une catégorie'
r = requests.get(url_category)
liste_livre = BeautifulSoup(r.content,'html.parser')

h3_tags = liste_livre.find_all('h3')

data=[]
links=[]
for link in h3_tags:
    links.append("https://books.toscrape.com/catalogue"+((link.find('a')['href']).replace("../../..","")))

#extraction de toutes les infos des livres d'une categorie

for i in links:
    info= scrapbook(i)
    data.append(info)

pprint(data)




