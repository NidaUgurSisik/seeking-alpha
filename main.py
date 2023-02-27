import re

import pandas as pd
import streamlit as st
import requests
from PyPDF2 import PdfReader
from functionforDownloadButtons import download_button
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}

    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="images/icon.png", page_title="Entity Extractor")


API_KEY = st.sidebar.text_input(
    "Enter your HuggingFace API key",
    help="Once you created you HuggingFace account, you can get your free API token in your settings page: https://huggingface.co/settings/tokens",
    type="password",
)

# Adding the HuggingFace API inference URL.
API_URL = "https://api-inference.huggingface.co/models/StanfordAIMI/stanford-deidentifier-base"

# Now, let's create a Python dictionary to store the API headers.
headers = {"Authorization": f"Bearer {API_KEY}"}

df = pd.DataFrame()
person = []
location = []
date = []
id = []
company = []
output = []
c2, c3 = st.columns([6, 1])

with c2:
    c31, c32 = st.columns([12, 2])
    with c31:
        st.caption("")
        st.title("Entity Extractor")
    with c32:
        st.image(
            "images/logo.png",
            width=200,
        )


# Convert PDF to JPG

uploaded_file = st.file_uploader(
    " ",
    key="1",
    help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
)


def copyWriter(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if uploaded_file is not None:
    output_string = StringIO()
    
    parser = PDFParser(uploaded_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    output = copyWriter({
            "inputs": output_string.getvalue(),
        })

    #st.write(merged_text)
    st.write(output_string.getvalue())
for i in output:
    st.write(i['start'], i['end'])