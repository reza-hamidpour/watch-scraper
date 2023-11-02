import requests
import fitz  # PyMuPDF
import re

class PDF_Reader:

    def __init__(self):
        self.pdf_document = None
        self.attributes_structure = {
            "Movement dimensions": 2,
            "Number of parts": 3,
            "Number of jewels": 2,
            "Chronometric power reserve": 1,
            "Barrels": 5,
            "Balance wheel": 2,
            "Frequency": 1,
            "Balance springs": 3,
            "Main plates": 11,
            "main plates": 11,
            "Escapement platforms": 6,
            "Tourbillon": 1,
            "Gearing": 2,
            "Movement and striking-mechanism displays": 4,
            "Movement": 4,
            "Displays": 4,
            "displays": 4,
            "Case": 9,
            "Striking mechanism Acoustic Mechanism": 5,
            "Automatic winding": 2,
            "Exterior case": 2,
            "Exterior": 2,
            "Case dimensions": 4,
            "Water resistance of the case": 2,
            "Crown with pusher": 2,
            "Crown": 2,
            "Dial": 7,
            "Dial side": 7,
            "Hands": 5,
            "Strap and clasp": 2,
        }
        self.attributes = {
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


    def pattern_generator(self, attribute, number_of_lines):
        txt = attribute.replace(" ", r"\s")
        structure = r"(" + txt + r"[\s*\r\n]+)"
        while number_of_lines > 0:
            structure = structure + r"((.*)+[\r\n]+)"
            number_of_lines -= 1
        structure = structure + r"(%%EOF)*"
        return structure

    def download_pdf(self, pdf_url, pdf_title):
        # Download the PDF
        response = requests.get(pdf_url)
        with open( pdf_title + ".pdf", "wb") as pdf_file:
            pdf_file.write(response.content)

    def read_document(self, pdf_url, document_title):
        # Download our pdf
        self.download_pdf(pdf_url, document_title)
        # Open and read the PDF using PdfReader
        self.pdf_document = fitz.open(document_title + ".pdf")

    def clear_all_attributes(self):
        for attribute, content in self.attributes.items():
            self.attributes[attribute] = "NaN"

    def read_attributes_from(self):
        for attribute, num_line in self.attributes_structure.items():
            pattern = self.pattern_generator(attribute, num_line)
            for page_num in range(len(self.pdf_document)):
                page = self.pdf_document[page_num]
                page_text = page.get_text()
                match = re.search(pattern, page_text, flags=re.A | re.M)
                if match:
                    text = ""
                    for item in match.groups()[1:]:
                        if item:
                            text = text + item
                    self.attributes[attribute] = text
                    break  # Exit loop if attribute is found on a page
        return self.attributes

