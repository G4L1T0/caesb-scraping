import re
import json
import requests
from bs4 import BeautifulSoup
from utils.twitter import post_tweet


def exec_request():
    cookies = {
        'JSESSIONID': 'A3BEFD006C9606E4B87A63AED8715DBD',
        'BIGipServerPOOL_ESTABILIZACAO' : '1828832010.35105.0000'
    }

    headers = {
        'Host': 'www.caesb.df.gov.br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    data = 'javax.faces.partial.ajax=true&javax.faces.source=j_idt44%3Aj_idt45&javax.faces.partial.execute=%40all&javax.faces.partial.render=formFaltaDeAgua&j_idt44%3Aj_idt45=j_idt44%3Aj_idt45&j_idt44=j_idt44&javax.faces.ViewState=e1s1'

    response = requests.post('https://www.caesb.df.gov.br/portal-servicos/app/publico/consultarfaltadagua?execution=e1s1', headers=headers, cookies=cookies, data=data)
    
    if response.status_code == 200:
        return response.text
response = exec_request()


soup = BeautifulSoup(response, 'lxml')
updateXML = soup.find_all('update')
soup2 = BeautifulSoup(str(updateXML[0]), 'html.parser')


cleanr = re.compile('<.*?>') 
def cleanhtml(raw_html):
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_listaGERAL():
    cont = 0
    listaRA = []
    listaGERAL = []
    for tabela_ra in list(soup2.findAll('table')[0].tbody.findAll('td')):
        listaRA.append(cleanhtml(str(tabela_ra)))
        cont += 1
        if cont % 6 == 0:
            listaGERAL.append(listaRA)
            listaRA = []
    return listaGERAL
listaGERAL = get_listaGERAL()


cei_dict = {}
for regiao in listaGERAL:
    if regiao[0][:3].lower() == 'cei':
        cei_dict = {
            'RA' : regiao[0],
            'Áreas Afetadas' : regiao[1],
            'Início' : regiao[2],
            'Normalização' : regiao[3],
            'Tipo de Falta de Água' : regiao[4],
            'Motivo da Falta de Água' : regiao[5]
        }
        print(json.dumps(cei_dict, indent=4, ensure_ascii=False))

