import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import requests
from PyPDF2 import PdfReader
from functionforDownloadButtons import download_button
from io import StringIO
from streamlit_tags import st_tags
API_URL = "https://api-inference.huggingface.co/models/joeddav/xlm-roberta-large-xnli"


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
    links = []
    for i in range(size):
        link = 'https://seekingalpha.com' + response['data'][i]['links']['self']
        links.append(link)
    return links

def ArticleText(links):
    texts = []
    for link in links:
        url = link    
        response = requests.get(url)        
        soup = BeautifulSoup(response.content, 'html.parser')        
        text = soup.get_text()        

        #print(text)
        text = text.split("Stock Ideas",1)[1]
        text = text.split("This article",1)[0]
        texts.append(text)
        
    return texts
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
    Size = st.text_input('How much article do you want ?', '')
    if Stock and Size:
        st.write(Size ,' Article for ', Stock, 'Stock')
        articleurl = getArticle(Stock,int(Size))
        article_text = ArticleText(articleurl)
        st.write(article_text)

    def get_values(column_names, labels_from_st_tags ):
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()


        label_lists = {}

        for element in labels_from_st_tags:
            label_lists[element] = []

        for row in article_text:

            output = query({
                "inputs": row,
                "parameters": {"candidate_labels": labels_from_st_tags},
            })
            st.write(output)

        return output



    form = st.form(key="annotation")
    with form:

        labels_from_st_tags = st_tags(
            value=["account", "credit", "reporting"],
            maxtags=5,
            suggestions=["account", "credit", "reporting"],
            label="",
        )

        submitted = st.form_submit_button(label="Submit")


