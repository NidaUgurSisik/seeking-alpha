import requests

API_URL = "https://api-inference.huggingface.co/models/StanfordAIMI/stanford-deidentifier-base"
headers = {"Authorization": f"Bearer {'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'}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "My name is Sarah Jessica Parker but you can call me Jessica, I live in Berlin",
})

print(output)



for i in output:
    if i['entity_group'] == 'HOSPITAL' and i['word'] != "":
        location.append(i['word'])
    if i['entity_group'] == 'HCW' and i['word'] != "":
        person.append(i['word'])
    if i['entity_group'] == 'DATE' and i['word'] != "":
        date.append(i['word'])
    if i['entity_group'] == 'ID' and i['word'] != "":
        id.append(i['word'])
    if i['entity_group'] == 'VENDOR' and i['word'] != "":
        company.append(i['word'])



df['person'] = person
df['location'] = location
df['date'] = date
df['id'] = id
df['company'] = company
c29, c30, c31 = st.columns([1, 1, 2])
with c29:

    CSVButton = download_button(
        df,
        "FlaggedFile.csv",
        "Download to CSV",
    )