import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the web driver
driver = webdriver.Chrome()  # You can use other browsers too
wait = WebDriverWait(driver, 10)  # Set a maximum wait time for locating elements

# Open the initial page
# url = "https://www.grand-seiko.com/ca-en/collections/all?page=1"
url = "https://www.grand-seiko.com/ca-en/collections/all?page=7"
driver.get(url)

# Scroll to load all watches
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find and extract watch links
watch_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.productCard')))
watch_urls = [link.get_attribute("href") for link in watch_links]

# Initialize CSV file for saving data
csv_filename = "grandseiko_result.csv"
csv_headers = ["url", "Date", "Limited edition", "Gender", "Reference Number", "Brand", "Series", "Exterior:",
               "Case back:", "Glass", "Glass Material:", "Glass Coating:", "Case size:", "Band width:", "Band Material:", "Clasp type:","Movement", "Caliber no.:", "Accuracy:", "Functions", "Water resistance:", "Magnetic resistance:",
               "Other details / Features:", "url of images"]

with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(csv_headers)

    # Iterate through each watch page
    for watch_url in watch_urls:
        driver.get(watch_url)
        watch_data = {"url": watch_url}
        try:
            watch_data["Reference Number"] = driver.find_element(By.CSS_SELECTOR, "h1._title").text
        except Exception as e:
            watch_data["Reference Number"] = "N/A"

        try:
            watch_data["Date"] = driver.find_element(By.XPATH, "//span[text()='NEW']")
            watch_data["Date"] = watch_data["Date"].text
        except Exception as e:
            watch_data["Date"] = "N/A"
        try:
            watch_data["Limited edition"] = driver.find_element(By.XPATH,
                                                                "//span[contains(text(), 'Limited')]")
            watch_data['Limited edition'] = watch_data['Limited edition'].text
        except Exception as e:
                watch_data["Limited edition"] = "N/A"
        try:
            watch_data["collection"] = driver.find_element(By.CSS_SELECTOR, "p._collection").text
        except Exception as e:
            watch_data["collection"] = "N/A"

        try:
            watch_data["Gender"] = driver.find_element(By.XPATH, "//span[contains(text(), 'Gender')]")
            watch_data["Gender"] = watch_data["Gender"].text
        except Exception as e:
            watch_data["Gender"] = "N/A"

        table_rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table._table tr')))
        for row in table_rows:
            value = row.find_element(By.TAG_NAME, 'td').text.strip()
            try:
                if row.find_element(By.TAG_NAME, 'th').text.strip():
                    header = row.find_element(By.TAG_NAME, 'th').text.strip()
                watch_data[header] = value
            except Exception as e:
                watch_data[header] += value

        # ... continue extracting other features
        image_urls = [img.get_attribute("src") for img in
                      driver.find_elements(By.CSS_SELECTOR, 'img[loading="lazy"]')]
        watch_data["url of images"] = ", ".join(image_urls)
        # Write the extracted data to the CSV file
        csv_writer.writerow([watch_data.get(header, "") for header in csv_headers])

# Close the web driver
driver.quit()

