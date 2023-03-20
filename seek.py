import requests
from bs4 import BeautifulSoup

url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/list"
keyword = 'tsla'
size = 5
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

#print(links)
for link in links:
    url = link    
    response = requests.get(url)        
    soup = BeautifulSoup(response.content, 'html.parser')        
    text = soup.get_text()        

    #print(text)
    text = text.split("Stock Ideas",1)[1]
    text = text.split("This article",1)[0]

    print(text)