import csv
import requests
from bs4 import BeautifulSoup, Tag

# URL of the main page
url = ""
categories = {

    "prospex": "https://www.seikowatches.com/ca-en/products/prospex/lineup",
   "presage": "https://www.seikowatches.com/ca-en/products/presage/lineup",
    "astron": "https://www.seikowatches.com/ca-en/products/astron/lineup",
    "5sports": "https://www.seikowatches.com/ca-en/products/5sports/lineup",
    "discovermore" : "https://www.seikowatches.com/ca-en/products/discovermore/lineup",

}

original_hrl = "https://www.seikowatches.com"
# Send an HTTP request to the main page
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
csv_file = open("all_seiko_watches.csv", mode="w", encoding="utf-8", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Url", "collection", "Date", "Gender", "Reference Number", "Brand", "Series",
                     "Movement", "Caliber Number", "Movement Type", "Precision",
                     "Power Reserve", "Jewels", "Functions", "Case/Band",
                     "Case Material", "Case Size", "Crystal", "Crystal Coating",
                     "LumiBrite", "Clasp", "Distance between lugs", "Other Details",
                     "Water Resistance", "Magnetic Resistance", "Weight", "Features",
                     "Image URLs"])
for key_ in categories:
    response = requests.get(categories[key_], headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all watch containers
    watch_containers = soup.find_all("a", ["class", "card-product"])

    # Create a CSV file to write the data

    print("Scrapping " + key_ + " collection started.")


    # Loop through watch containers
    for watch_container in watch_containers:
        watch_url = watch_container["href"]
        watch_response = requests.get(original_hrl + watch_url, headers=HEADERS)
        watch_soup = BeautifulSoup(watch_response.content, "html.parser")

        # Extract information from the watch's page
        url = watch_url
        date = watch_soup.find("span", class_="_new").text.strip() if watch_soup.find("span",
                                                                                      class_="_new") else "Not available"
        if watch_soup.find('dt', string="Functions") != None:
            functions = '\n'.join(
                [i.text.strip() if i else "N/A" for i in watch_soup.find('dt', string="Functions").find_next("dd").findChildren('li')])
        else:
            functions = "N/A"
        movement = ""
        gender = watch_soup.find("span", class_="_gender")
        if gender:
            gender = gender.text.strip()

        reference_number = watch_soup.find("h1", class_="_title")
        if reference_number:
            reference_number = reference_number.text.strip()

        brand = watch_soup.find('div', class_="_subTitle")
        if brand:
            brand = brand.findChildren('span')[0].text.strip()

        series = watch_soup.find('div', class_="_subTitle")
        if series and len(series.findChildren('span')) > 1:
            series = series.findChildren('span')[1].text.strip()

        caliber_number = watch_soup.find("dt", string="Caliber Number")
        if caliber_number:
            caliber_number = caliber_number.find_next("dd").text.strip()

        movement_type = watch_soup.find("dt", string="Movement Type")
        if movement_type:
            movement_type = movement_type.find_next("dd").text.strip()

        precision = watch_soup.find("dt", string="Precision")
        if precision:
            precision = precision.find_next("dd").text.strip()

        power_reserve = watch_soup.find("dt", string="Power reserve")
        if power_reserve:
            power_reserve = power_reserve.find_next("dd").text.strip()

        jewels = watch_soup.find("dt", string="Jewels")
        if jewels:
            jewels = jewels.find_next("dd").text.strip()

        case_material = watch_soup.find("dt", string="Case Material")
        if case_material:
            case_material = case_material.find_next("dd").text.strip()

        case_band = watch_soup.find("dt", string="Case Band")
        if case_band:
            case_band = case_band.find_next("dd").text.strip()

        case_size = watch_soup.find("dt", string="Case Size")
        if case_size:
            case_size = case_size.find_next("dd").text.strip()

        # Crystal
        crystal = watch_soup.find('dt', string="Crystal")
        if crystal:
            crystal = crystal.find_next('dd')
            if crystal:
                crystal = crystal.text.strip()

        # Crystal Coating
        crystal_coating = watch_soup.find('dt', string="Crystal Coating")
        if crystal_coating:
            crystal_coating = crystal_coating.find_next('dd')
            if crystal_coating:
                crystal_coating = crystal_coating.text.strip()

        # LumiBrite
        lumibrite = watch_soup.find('dt', string="LumiBrite")
        if lumibrite:
            lumibrite = lumibrite.find_next('dd')
            if lumibrite:
                lumibrite = lumibrite.text.strip()

        # Clasp
        clasp = watch_soup.find('dt', string="Clasp")
        if clasp:
            clasp = clasp.find_next('dd')
            if clasp:
                clasp = clasp.text.strip()

        # Distance between Lugs
        distance_between_lugs = watch_soup.find('dt', string="Distance between lugs")
        if distance_between_lugs:
            distance_between_lugs = distance_between_lugs.find_next('dd')
            if distance_between_lugs:
                distance_between_lugs = distance_between_lugs.text.strip()

        # Water Resistance
        water_resistance = watch_soup.find('dt', string="Water Resistance")
        if water_resistance:
            water_resistance = water_resistance.find_next('dd')
            if water_resistance:
                water_resistance = water_resistance.text.strip()

        # Magnetic Resistance
        magnetic_resistance = watch_soup.find('dt', string="Magnetic Resistance")
        if magnetic_resistance:
            magnetic_resistance = magnetic_resistance.find_next('dd')
            if magnetic_resistance:
                magnetic_resistance = magnetic_resistance.text.strip()

        # Weight
        weight = watch_soup.find('dt', string="Weight")
        if weight:
            weight = weight.find_next('dd')
            if weight:
                weight = weight.text.strip()

        other_details = ""
        if watch_soup.find('dt', string="Features") != None:
            features = '\n'.join(
                [i.text.strip() for i in watch_soup.find('dt', string="Features").find_next('dd').findChildren('li')])
        else:
            features = "N/A"
        # Extract image URLs
        image_elements = watch_soup.find_all("div", class_="js-productVisual-photoswipe")
        image_elements = [image_element.findChild('img', class_="_image") for image_element in image_elements]
        image_urls = [original_hrl + image_element["src"] for image_element in image_elements]

        # Write data to the CSV file
        csv_writer.writerow([url, key_, date, gender, reference_number, brand, series,
                             movement, caliber_number, movement_type, precision,
                             power_reserve, jewels, functions, case_band,
                             case_material, case_size, crystal, crystal_coating,
                             lumibrite, clasp, distance_between_lugs, other_details,
                             water_resistance, magnetic_resistance, weight, features,
                             '\n'.join(image_urls)])

    # Close the CSV file
csv_file.close()
print("Scraping " + key_ + "  completed. Data saved to all_seiko_watches.csv")