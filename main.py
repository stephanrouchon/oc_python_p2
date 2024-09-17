import re

import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)

soup=BeautifulSoup(page.content,"html.parser")

#extraction du title du livre
book_title=soup.find('h1').contents

#extraction de l'url de l'image
image=soup.find('img')
image=image['src']
url_image="https://books.toscrape.com/"+image.replace("../../","")

#extraction de la description du livre
description=soup.find('div',id="product_description")
description=description.find_next('p')
description=description.contents

#extraction des donnees du tableau du livre
table=soup.find('table')
tableau=[]

#for lignes in table.find_all('tr'):
#    colonnes= lignes.find_all('td')
#   tableau.append(colonnes)
#    print(colonnes)

informations=[]
for info in table:
    information = info.find('td')
    if information !=-1:
        informations.append(information.string)

#récuperer la valeur numérique du stock dans la string et la convertir
stock_text = re.findall(r'\d+',informations[5])
stock = stock_text[0]
informations[5]=int(stock)


