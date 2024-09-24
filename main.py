import csv
import re

from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

def scrapbook(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content,"html.parser")
    book={}
    book["product_page_url"]=url

    #extraction du title du livre
    book["title"] = soup.find('h1').get_text()
    print(book["title"])

    #extraction de l'url de l'image
    image = soup.find('img')
    image = image['src']
    book["image_url"] = "https://books.toscrape.com/" + image.replace("../../", "")

    #extraction de la description du livre
    if soup.find('div',id="product_description"):
        description = soup.find('div', id="product_description")
        book["product_description"] = description.find_next('p').get_text()
    else: book["product_description"]=""

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

#extrait la liste des catégories

url="https://books.toscrape.com/index.html"
r = requests.get(url)
category_soup = BeautifulSoup(r.content,"html.parser")
categorys = category_soup.find('ul', class_="nav nav-list")

category_links = categorys.find_all('a')
hrefs_categorys =["https://books.toscrape.com/"+link.get('href') for link in category_links if link.get('href')]

for href in hrefs_categorys[1:]:
    url_category = href

    links=[]

    # extrait les urls d'une catégorie'

    r = requests.get(url_category)
    liste_livre = BeautifulSoup(r.content, 'html.parser')
    h3_tags = liste_livre.find_all('h3')
    for link in h3_tags:
        links.append("https://books.toscrape.com/catalogue" + ((link.find('a')['href']).replace("../../..", "")))

    while liste_livre.find('li',class_='next'):
                url= liste_livre.find('li',class_='next')
                next_url=(url.find('a')['href'])
                parsed_url_category = urlparse(url_category)
                next_url = "https://books.toscrape.com/"+"/".join(parsed_url_category.path.split("/")[:-1])+"/"+next_url

                request2 = requests.get(next_url)
                liste_livre = BeautifulSoup(request2.content, 'html.parser')
                h3_tags = liste_livre.find_all('h3')
                for link in h3_tags:
                    links.append("https://books.toscrape.com/catalogue" + ((link.find('a')['href']).replace("../../..", "")))


#extraction de toutes les infos des livres d'une categorie

    data = []
    for i in links:

            info= scrapbook(i)
            data.append(info)

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

    category = data[0]['category']

    filename = f"files/{category}.csv"
    with open(filename,'w',newline='',encoding='utf-8') as fichier:
            writer=csv.DictWriter(fichier,ordre_cles, delimiter=",")
            #Insertion en tete
            writer.writeheader()
            #Insertion données
            writer.writerows(data)










