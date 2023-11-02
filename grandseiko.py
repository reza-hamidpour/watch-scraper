import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from requests_html import HTMLSession
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# URL of the main page with the watch collection
main_url = "https://www.grand-seiko.com/ca-en/collections/all?page=1&collection=Masterpiece"
headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

params = {
  'q': 'how to create minecraft server',
  'gl': 'us',
  'hl': 'en',
}
# Send a GET request to the main URL
# response = requests.get(main_url, headers=headers, params=params)
# response.html
session = HTMLSession()
response = session.get(main_url)
response.html.render()
soup = BeautifulSoup(response.html.html, 'lxml')
# Find all watch links on the main page
watch_links = []
links_ = soup.find('div', id="app").findChild("div", class_="section").findChild("div", class_="section-body")
links_ = links_.find("div", class_="container")
for row in links_.findChildren("div", class_="row"):
    for link in row.find_all("a", class_="productCard"):
        watch_links.append(link.get("href"))

# Initialize a list to store watch details
session.close()
watch_details = []

# Loop through each watch link and scrape the required information
for watch_link in watch_links:
    watch_url = f"https://www.grand-seiko.com{watch_link}"
    watch_session = HTMLSession()
    request_watch = watch_session.get(watch_url)
    # watch_response = requests.get(watch_url, headers=HEADERS)
    request_watch.html.render()
    watch_soup = BeautifulSoup(request_watch.html.html, "lxml")
    # Extract watch details using the appropriate tags or classes
    date = watch_soup.find("span", text=re.compile("Date:"))
    if date:
        date = date.find_next_sibling("span").text.strip()
    else:
        date = "N/A"

    limited_edition = watch_soup.find("span", text=re.compile("Limited edition:"))
    if limited_edition:
        limited_edition = limited_edition.find_next_sibling(
            "span").text.strip()
    else:
        limited_edition = "N/A"
    gender = watch_soup.find("span", text=re.compile("Gender:"))
    if gender:
        gender = gender.find_next_sibling("span").text.strip()
    else:
        gender = "N/A"
    # Extract other details similarly
    # Extract watch features using the appropriate tags or classes
    # features = watch_soup.find("div", class_="c-product-detail__description").text.strip()
    features = watch_soup.find("div", class_="productSpec-data").text.strip()

    # Additional features
    # case_back = re.search(r"Case back:(.*)", features, re.IGNORECASE).group(1).strip()
    case_back = watch_soup.find('table', class_="_table").find('th', string="Case Back:")
    if case_back:
        case_back = case_back.find_next_sibling().text.strip()
    else:
        case_back = "N/A"
    # glass_material = re.search(r"Glass Material:(.*)", features, re.IGNORECASE).group(1).strip()
    glass_material = watch_soup.find('table', class_="_table").find('th', string="Glass Material:")
    if glass_material:
        glass_material = glass_material.find_next_sibling().text.strip()
    else:
        glass_material = "N/A"
    # glass_coating = re.search(r"Glass Coating:(.*)", features, re.IGNORECASE).group(1).strip()
    glass_coating = watch_soup.find('table', class_="_table").find('th', string="Glass Coating:")
    if glass_coating:
        glass_coating = glass_coating.find_next_sibling().text.strip()
    else:
        glass_coating = "N/A"
    # case_size = re.search(r"Case size:(.*)", features, re.IGNORECASE).group(1).strip()
    case_size = watch_soup.find('table', class_="_table").find('th', string="Case size:")
    if case_size:
        case_size = case_size.find_next_sibling().text.strip()
    else:
        case_size = "N/A"
    # band_width = re.search(r"Band width:(.*)", features, re.IGNORECASE).group(1).strip()
    band_width = watch_soup.find('table', class_="_table").find('th', string="Band width:")
    if band_width:
        band_width = case_size.find_next_sibling().text.strip()
    else:
        band_width = "N/A"
    # band_material = re.search(r"Band Material:(.*)", features, re.IGNORECASE).group(1).strip()
    band_material = watch_soup.find('table', class_="_table").find('th', string="Band Material:")
    if band_material:
        band_material = band_material.find_next_sibling().text.strip()
    else:
        band_material = "N/A"
    # clasp_type = re.search(r"Clasp type:(.*)", features, re.IGNORECASE).group(1).strip()
    clasp_type = watch_soup.find('table', class_="_table").find('th', string="Clasp type:")
    if clasp_type:
        clasp_type = clasp_type.find_next_sibling().text.strip()
    else:
        clasp_type = "N/A"
    # movement = re.search(r"Movement:(.*)", features, re.IGNORECASE).group(1).strip()
    movement = watch_soup.find('table', class_="_table").find('th', string="Movement:")
    if movement:
        movement = movement.find_next_sibling().text.strip()
    else:
        movement = "N/A"
    # caliber_number = re.search(r"Caliber Number:(.*)", features, re.IGNORECASE).group(1).strip()
    caliber_number = watch_soup.find('table', class_="_table").find('th', string="Caliber Number:")
    if caliber_number:
        caliber_number = caliber_number.find_next_sibling().text.strip()
    else:
        caliber_number = "N/A"
    # accuracy = re.search(r"Accuracy:(.*)", features, re.IGNORECASE).group(1).strip()
    accuracy = watch_soup.find('table', class_="_table").find('th', string="Accuracy:")
    if accuracy:
        accuracy = accuracy.find_next_sibling().text.strip()
    else:
        accuracy = "N/A"
    # functions = re.search(r"Functions:(.*)", features, re.IGNORECASE).group(1).strip()
    functions = watch_soup.find('table', class_="_table").find('th', string="Functions:")
    if functions:
        functions = functions.find_next_sibling().text.strip()
    else:
        functions = "N/A"
    # water_resistance = re.search(r"Water resistance:(.*)", features, re.IGNORECASE).group(1).strip()
    water_resistance = watch_soup.find('table', class_="_table").find('th', string="Water resistance:")
    if water_resistance:
        water_resistance = water_resistance.find_next_sibling().text.strip()
    else:
        water_resistance = "N/A"
    # magnetic_resistance = re.search(r"Magnetic resistance:(.*)", features, re.IGNORECASE).group(1).strip()
    magnetic_resistance = watch_soup.find('table', class_="_table").find('th', string="Magnetic resistance:")
    if magnetic_resistance:
        magnetic_resistance = magnetic_resistance.find_next_sibling().text.strip()
    else:
        magnetic_resistance = "N/A"
    # other_details = re.search(r"Features:(.*)", features, re.IGNORECASE).group(1).strip()
    other_details = watch_soup.find('table', class_="_table").find('th', string="Features:")
    if other_details:
        other_details = other_details.find_next_sibling().text.strip()
    else:
        other_details = "N/A"
    # Extract image URLs



    image_urls = [img.get("src") for img in watch_soup.find_all("img", ["loading", "lazy"])]

    # Store the scraped data
    watch_details.append({
        "watch_url": watch_url,
        "date": date,
        "limited_edition": limited_edition,
        "gender": gender,
        "case_back": case_back,
        "glass_material": glass_material,
        "glass_coating": glass_coating,
        "case_size": case_size,
        "band_width": band_width,
        "band_material": band_material,
        "clasp_type": clasp_type,
        "movement": movement,
        "caliber_number": caliber_number,
        "accuracy": accuracy,
        "functions": functions,
        "water_resistance": water_resistance,
        "magnetic_resistance": magnetic_resistance,
        "other_details": other_details,
        "image_urls": image_urls
    })
    watch_session.close()

# Create a DataFrame from the scraped data
df = pd.DataFrame(watch_details)

# Save the DataFrame to a CSV file
csv_filename = "watch_details.csv"
df.to_csv(csv_filename, index=False)

print(f"Scraped watch details saved to {csv_filename}")