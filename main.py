import datetime
import os
import time
from bs4 import BeautifulSoup
import streamlit as st
import requests
from streamlit_tags import st_tags
import pandas as pd
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}

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

def getArticle(keyword,until_unix,since_unix):
    url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/list"

    querystring = {"until": until_unix,
    "since": since_unix,"id":keyword,"number":"1"}

    headers = {
        "X-RapidAPI-Key": os.getenv('X-RapidAPI-Key'),
        "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    links = []
    for i in range(len(response['data'])):
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
        #text = text.split("Summary",1)[1]
        #text = text.split("Seeking Alpha's Disclosure:",1)[0]
        texts.append(text)
        
    return texts

def get_values(article_text,labels_from_st_tags):
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
            for index_, value in enumerate(output['labels']):
                label_lists[value].append(round(output['scores'][index_], 2))

        for vals in labels_from_st_tags:
            df[vals] = label_lists[vals]


        return df

c2, c3 = st.columns([50, 1])

with c2:
    c31, c32 = st.columns([24, 4])
    with c31:
        st.caption("")
        st.title("Seeking Alpha")
    with c32:
        st.image(
            "images/logo.png",
            width=200,
        )
    Stock = st.text_input('Stock Name', '')
    since = st.date_input(
        "Since",
        datetime.date(2023, 2, 2))
    since_unix = time.mktime(since.timetuple())
    until = st.date_input(
        "Until",
        datetime.date(2023, 2, 2))
    until_unix = time.mktime(until.timetuple())

    if Stock and until and since:
        st.write(' Article for ', Stock, 'Stock')
        articleurl = getArticle(Stock,until_unix,since_unix)
        article_text = ArticleText(articleurl)

    form = st.form(key="annotation")
    with form:

        labels_from_st_tags = st_tags(
            value=["positive", "negative"],
            maxtags=5,
            suggestions=["positive", "negative"],
            label="",
        )

        submitted = st.form_submit_button(label="Submit")

    if submitted:
        df = pd.DataFrame(articleurl)
        result = get_values(article_text, labels_from_st_tags)
        edited_df = st.experimental_data_editor(df)