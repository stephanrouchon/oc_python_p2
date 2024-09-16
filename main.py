import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
print(page.content)

soup=BeautifulSoup(page.content,"html.parser")

#extraction du title du livre
Book_Title=soup.find('h1').contents

#extraction de l'url de l'image
Image=soup.find('img')
Image=Image['src']
URL_Image="https://books.toscrape.com/"+Image.replace("../../","")



