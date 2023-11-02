import requests
import fitz  # PyMuPDF
import re
import csv

import requests
from bs4 import BeautifulSoup, Tag
import csv
from greubel_pdf_attributes import PDF_Reader

# Define the URL of the page
collections = {
    "collection-convexe":"https://www.greubelforsey.com/en/collections/collection-convexe",
    "collection": "https://www.greubelforsey.com/en/collections/collection"
}

base_url = "https://www.greubelforsey.com"


def get_attrs():
    return {
            "Eternal url": "",
            "collection": "",
            "Nickname": "",
            "Pricing": "",
            "Movement dimensions": '',
            "Number of parts": '',
            "Number of jewels": '',
            "Chronometric power reserve": '',
            "Barrels": '',
            "Balance wheel": '',
            "Frequency": '',
            "Balance springs": '',
            "Main plates": '',
            "main plates": '',
            "Escapement platforms": '',
            "Tourbillon": '',
            "Gearing": '',
            "Movement and striking-mechanism displays": '',
            "Movement": '',
            "Displays": '',
            "displays": '',
            "Case": '',
            "Striking mechanism Acoustic Mechanism": '',
            "Automatic winding": '',
            "Exterior case": '',
            "Exterior": '',
            "Case dimensions": '',
            "Water resistance of the case": '',
            "Crown with pusher": '',
            "Crown": '',
            "Dial": "",
            "Dial side": "",
            "Hands": "",
            "Strap and clasp": "",
        }
# Send a GET request to the page

for col_name, col_url in collections.items():
    response = requests.get(col_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all product links on the page
        all_contents = soup.find_all("article", class_="watch-card")

        # Define a list to store product data
        product_data = []

        for product in all_contents:
            attributes = get_attrs()
            # Extract the product page URL
            product_wrapper = product.find('div', class_="wrapper")

            if product_wrapper.find('figure', class_="block-visual").find('img'):
                attributes["pic_url"] = base_url + product_wrapper.find('figure', class_="block-visual").find('img')[
                    'src']

            if product_wrapper.find('div', class_="block-content").find('a'):
                attributes['Eternal url'] = base_url + product_wrapper.find('div', class_="block-content").find('a')[
                    "href"]
                attributes['Nickname'] = product_wrapper.find('div', class_="block-content").find('a').text.strip()
            else:
                continue

            # Send a GET request to the product page
            product_response = requests.get(attributes['Eternal url'])
            # Check if the request was successful
            if product_response.status_code == 200:
                # Parse the HTML content of the product page
                product_soup = BeautifulSoup(product_response.content, "html.parser")
                # Extract the attributes you need
                technical_section = product_soup.find("section", class_='technical-data').find('div', class_='wrapper')
                for elem in technical_section.find('ul', class_="setColumns").find_all('li'):
                    elem_ = elem.findChild("strong", class_='data-title')
                    if elem_ and elem_.text.strip() in attributes:
                        attributes[elem_.text.strip()] = elem.findChild("span", class_='data-content').text.strip()

                # collection_name = product_soup.find("h1", class_="product-collection").text.strip()
                data_sheet_url = technical_section.find('div', class_="col-1")
                if data_sheet_url and data_sheet_url.find("a"):
                    attributes['Manual Sheet'] = base_url + data_sheet_url.find("a")["href"]
                    gather_pdf_sheet = PDF_Reader()
                    gather_pdf_sheet.read_document(attributes['Manual Sheet'],
                                                   attributes['Nickname'].strip().replace(' ', '-'))
                    gather_pdf_sheet.clear_all_attributes()
                    pdf_attributes = gather_pdf_sheet.read_attributes_from()
                    for attr, val in pdf_attributes.items():
                        attributes[attr] = val
                product_data.append(attributes)
        # Save the extracted data to a CSV file
        csv_filename = col_name + "greubel_forsey_products.csv"
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header row
            writer.writerow(list(product_data[0].keys()))
            # Write attribute-value pairs
            for attributes in product_data:
                writer.writerow(list(attributes.values()))
            # for attribute, value in attributes.items():
            #     writer.writerow([attribute, value])

        print(f"Data " + col_name + " saved to {csv_filename}")
        csv_file.close()
    else:
        print("Failed to retrieve the page.")
