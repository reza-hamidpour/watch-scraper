from bs4 import BeautifulSoup as bsoup
from bs4 import NavigableString, Tag
import requests
import csv
from collections.abc import Iterable


def clear_attributes(dic_):
    for key in dic_:
        dic_[key] = "Not Available"
    return dic_


all_values = {"url": "",
              "Collections": "",
              "Name": "",
              "Description": "",
              "Product Reference": "",
              "Pricing": "",
              "Material": "",
              "Gem-setting": "",
              "Dimensions": "",
              "Height": "",
              "Caseback": "",
              "Water-resistance (bar)": "",
              "TYPE": "",
              "Caliber": "",
              "Functions": "",
              "Composition": "",
              "Buckle": "",
              "Total gem-setting": "",
              "MÉTIER D'ART": "",
              "Limited edition": "",
              "Type": "",
              "Add on": "",
              "img 1": "",
              "img 2": "", }

collection_url = 'https://www.harrywinston.com/en/themes/2023-ocean-collection-25th-anniversary'
base_url = "https://www.harrywinston.com"

# loading all product
collection_page = requests.get(collection_url)
collection_souper = bsoup(collection_page.content, 'html.parser')
with open('result.csv', 'w') as csvfile:
    write = csv.DictWriter(csvfile, fieldnames=all_values.keys())
    write.writeheader()
    for product in collection_souper.find_all('div', {'class', 'product__wrapper'}):

        attributes = clear_attributes(all_values)

        # we have all product new we dive into each product page
        product_page = requests.get(base_url + product.find('a').get('href'))
        product_souper = bsoup(product_page.content, 'html.parser')
        # product title extraction
        attributes['Name'] = product_souper.find('h1', {'class', 'pdp-header__product-name'}).text.strip()
        attributes['Collections'] = product_souper.find('p', {'class', 'pdp-header__collection-name'}).find('a').get('title')
        attributes['url'] = base_url + product.find('a').get('href')
        # product description and content
        content = product_souper.find('div', {'class', 'pdp-header__product-description'})
        attributes['Description'] = content.find('p').text.strip()
        attributes['Product Reference'] = content.find('div', {'class',
                                                               'pdp-header__product-description--product-number'}).text.strip()

        technical_section = product_souper.find_all('div', {'class', 'pdp-timepiece-specifications__specs-section'})
        for each_section in technical_section:
            items = each_section.find('div', {'class', 'pdp-timepiece-specifications__specs-section-row'})
            items = items.find_all('div', {'class', 'pdp-timepiece-specifications__specs-section-item'})
            for item in items:
                item_title = item.find('h5').text.strip()
                if item_title in attributes:
                    attributes[item_title] = item.find('div',
                                                       {'class',
                                                        'pdp-timepiece-specifications__specs-section-text'}).text.strip()
                else:
                    print(item_title)
                    print(item.find('div', {'class', 'pdp-timepiece-specifications__specs-section-text'}).text.strip())
        write.writerow(attributes)
