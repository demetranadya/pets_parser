import csv
import re
import requests as r
from bs4 import BeautifulSoup
import json
import time


page_num = 5
list_items = []

URL = "https://www.petshop.ru/adverts/cats?page=%s"
domen = "https://www.petshop.ru"

headerDict = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1'}

for page_i in range(1, page_num+1):
    time.sleep(4)
    # try:
    page = r.get(URL % page_i, headers=headerDict)

    if page.status_code == 200:
        # import ipdb; ipdb.set_trace()
        soup = BeautifulSoup(page.text, 'lxml')
        catalog_products = soup.find("section", {"class": "adverts-list"})
        if catalog_products:
            list_product = catalog_products.findAll("div", {"class": "articles-item"})
            print("Длина %s" % len(list_product))

            for i in list_product:
                name = ''
                breed = ''
                price = ''
                cat_url = ''
                description = ''
                
                articles_el = i.find("div", {"class": "articles-text"})
                if articles_el:
                    article = articles_el.text 
                    h2 = articles_el.find("h2")
                    if h2:
                        name = h2.text
                        cat_url = i.find("a").attrs["href"]

                    discription_el = articles_el.find("div", {"class": "text"})
                    if discription_el:
                        description = discription_el.text

                info_el = i.find("div",{"class": "quick-info"})
                if info_el:
                    price_el = info_el.find("div", {"class": "price"})
                    if price_el:
                        price = price_el.find("span")
                        if price:
                            price_text =  price.text
                    breed_el = info_el.find("div", {"class": "breed"})
                    if breed_el:
                        breed = breed_el.find("span")
                        if breed:
                            breed_text = breed.text

                # import ipdb;ipdb.set_trace()
                list_items.append({'name': name, 'breed': breed_text, 'price': price_text, 'cat_url': f'{domen}{cat_url}', "description": description})
                time.sleep(3)
    else:
        print("Status code not 200")
        print(page.text)

path = "output.csv"
with open(path, "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    for item in list_items:
        line = [item.get('name'),item.get('breed'), item.get('price'), item.get('cat_url'), item.get('description')]
        writer.writerow(line)