import csv
import re

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
    book["price_exluding_tax"] = informations[2]
    book["universal_ product_code"] = informations[0]

    #récuperer la valeur numérique du stock dans la string et la convertir
    stock_text = re.findall(r'\d+',informations[5])
    stock = stock_text[0]
    book["number_available"] = int(stock)

    #récuperer la class star rating
    book["review_rating"] = soup.find('p', class_=re.compile(r'^star-rating')).get('class')[1]

    #recuperer la catégorie du livre
    categorie = soup.find('li').find_next('li').find_next('li')
    categorie = categorie.get_text()
    book["category"] = categorie.replace("\n", "")
    return book

livre = scrapbook(url)


#Création fichier csv
with open('livres.csv','w') as fichier:
    writer = csv.writer(fichier, delimiter=',')




