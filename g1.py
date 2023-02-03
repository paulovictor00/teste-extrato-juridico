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

regex_titulos = re.findall(r'<div\s*class="_evt"><h2><a\shref="[^>]*"\s*class="feed-post-link gui-color-primary\s*gui-color-hover"\s[^>]*">([^>]*)</a></h2>',str(html),re.S)

regex_subtitulos = re.findall(r'<div class="bstn-fd-relatedtext"><a class="[^>]*"\s*href="[^>]*">([^<]*)</a>|<div class="feed-post-body-resumo" elementtiming="text-ssr">(.*?)</div>',str(html),re.S)

regex_fotos = re.findall(r'<img class="bstn-fd-picture-image".*?srcSet="(.*?)"\s*/>', html, re.IGNORECASE)

lista_subtitulo = []

for eliminar_espaco_em_branco in regex_subtitulos:
    for eliminar in range(len(eliminar_espaco_em_branco)):
        if eliminar_espaco_em_branco[eliminar] != "":
            lista_subtitulo.append(eliminar_espaco_em_branco[eliminar])
            
data = {}

for titulo in range(len(regex_titulos)):
    dados = data[regex_titulos[titulo]] = lista_subtitulo[titulo]


with open("dados.json", "w", encoding="utf-8") as arquivo:
    json.dump(data, arquivo, ensure_ascii=False)

print(json.dumps(data))

cout = 0
for foto in regex_fotos:

    split_fotos = foto.split(",")[0]
    split_fotos = split_fotos[:-5]


    url_foto = split_fotos
    response = requests.get(url_foto).content

    with open(f"fotos/picture_{str(cout)}.jpg", "wb") as f:
        f.write(response)
    
    cout = cout + 1
