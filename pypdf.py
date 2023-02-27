from PyPDF2 import PdfReader

# creating a pdf reader object
reader = PdfReader('C:/Users/Ugur/Desktop/Sweephy/dosya/visualization.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

for i in range(len(reader.pages)):
    # getting a specific page from the pdf file
    page = reader.pages[i]

    # extracting text from page
    text = page.extract_text()
    print(text + '\n')