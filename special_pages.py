import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import csv
# Define the URL of the main page
main_url = "https://www.seikowatches.com/ca-en/products/presage/specialpage"
website_url = "https://www.seikowatches.com"
headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

params = {
  'q': 'how to create minecraft server',
  'gl': 'us',
  'hl': 'en',
}
# Send a GET request to the main page
response = requests.get(main_url, headers=headers, params=params)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the links to special pages
special_page_links = [a['href'] for a in soup.select('.specialList-item a')]

# Initialize lists to store data
titles = []
texts = []
images = []

# Loop through each special page
csv_file = open(" special_pages_seiko_watches.csv", mode="w", encoding="utf-8", newline="")
print("Scrapping collection started.")
csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    "url",
    "collection | series",
    "content",
    "images"
])
for link in special_page_links:
    # Construct the URL of the special page
    special_url = website_url + link  # You might need to modify this based on the actual link structure

    # Send a GET request to the special page
    special_response = requests.get(special_url, headers=headers, params=params)
    special_soup = BeautifulSoup(special_response.content, 'html.parser')

    # Extract title
    title = special_soup.select_one('title')
    if title:
        title.text.strip()
    else:
        title = "N/A"
    titles.append(title)
    texts = []
    # Extract text content
    for section in special_soup.find_all("section"):
        if section.has_attr('id') and "concept" == section['id']:
            texts.append("concept")
        elif section.has_attr('id') and section['id'] == "main":
            continue
        else:
            title = section.find("div", class_="txt_box")
            if isinstance(title, Tag) and title.findChild("h2"):
                title = title.findChild("h2")
                if isinstance(title, Tag):
                    texts.append(title.text.strip())
                elif isinstance(section.find("div", class_="txt_box").findChild("h3"), Tag):
                    texts.append(section.find("div", class_="txt_box").findChild("h3").text.strip())
        content = section.find("div", class_="inner")
        if isinstance(content, Tag):
            content = content.find("p")
            if content:
                content = content.text.strip()
            texts.append(content)
        # Find the image element and extract the image URL
        image_element = section.find('div', class_="img_box")
        images = []
        if isinstance(image_element, Tag):
            extracted_image_url = [main_url + image_['src'] if image_ else None for image_ in image_element.findChildren("img")]
            images.append(extracted_image_url)
    csv_writer.writerow([
        special_url,
        title,
        texts,
        images
    ])

# Create a DataFrame from the extracted data
# df = pd.DataFrame({'Title': titles, 'Text': texts, 'Image': images})

# Save the DataFrame to a CSV file
# df.to_csv('scraped_data.csv', index=False)