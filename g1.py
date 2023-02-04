import re
import requests
import json

url = "https://g1.globo.com/"

header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"
}

html = requests.get(url,headers=header).content.decode('utf-8')

regex_sub_ti = re.findall(r'class=[^>]*chapeu">([^<]*)</span>.*?class=[^>]*ssr">([^<]*)<',html,re.S)


regex_fotos = re.findall(r'<img class="bstn-fd-picture-image".*?srcSet="(.*?)"\s*/>', html, re.IGNORECASE)


            
data = {}

for titulo in regex_sub_ti:
    title = titulo[0]
    subtitle = titulo[1]
    data[title] = subtitle 


with open("dados.json", "w", encoding="utf-8") as arquivo:
    json.dump(data, arquivo, ensure_ascii=False,indent=4)

print(json.dumps(data,indent=4))

cout = 0
for foto in regex_fotos:

    split_fotos = foto.split(",")[0]
    split_fotos = split_fotos[:-5]


    url_foto = split_fotos
    response = requests.get(url_foto).content

    with open(f"fotos/picture_{str(cout)}.jpg", "wb") as f:
        f.write(response)
    
    cout = cout + 1
     


