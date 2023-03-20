import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import requests
from PyPDF2 import PdfReader
from functionforDownloadButtons import download_button
from io import StringIO



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

st.set_page_config(page_icon="images/icon.png", page_title="Seeking Alpha")

def getArticle(keyword, size):
    url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/list"

    querystring = {"id":keyword,"size":size,"number":"1"}

    headers = {
        "X-RapidAPI-Key": "7b530f132bmsh9ce89c66c2eb5d1p1864c8jsnd7c0c3f9ed02",
        "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

c2, c3 = st.columns([6, 1])

with c2:
    c31, c32 = st.columns([12, 2])
    with c31:
        st.caption("")
        st.title("Seeking Alpha")
    with c32:
        st.image(
            "images/logo.png",
            width=200,
        )
    Stock = st.text_input('Stock Name', '')
    if Stock:
        st.write('The current Stock Name is', Stock)
    Size = st.text_input('How much article do you want ?', '')



