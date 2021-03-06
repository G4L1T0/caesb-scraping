import re
import json
import requests
from bs4 import BeautifulSoup
from utils.twitter import post_tweet, message_tweet
from utils.mongodb import inputDB, updateDB, db_cei


def get_JSESSIONID():
    session = requests.Session()
    response = session.get('https://www.caesb.df.gov.br/portal-servicos/app/publico/consultarfaltadagua?execution=e1s1')
    dict_cookies = session.cookies.get_dict()
    return dict_cookies['JSESSIONID'], list(dict_cookies.values())[0]
cookie_JSESSIONID, cookie_BIGipServerPOOL = get_JSESSIONID()


def exec_request(cookie_JSESSIONID, cookie_BIGipServerPOOL):
    cookies = {
        'JSESSIONID': cookie_JSESSIONID,
        'BIGipServerPOOL_ESTABILIZACAO' : cookie_BIGipServerPOOL
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
response = exec_request(cookie_JSESSIONID, cookie_BIGipServerPOOL)


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

infos_ceilandia = db_cei()

def get_cei():
    cei_list = []
    for regiao in listaGERAL:
        if regiao[0].lower().count('cei'):
            cei_dict = {
                'RA' : regiao[0],
                '??reas Afetadas' : regiao[1],
                'In??cio' : regiao[2],
                'Normaliza????o' : regiao[3],
                'Tipo de Falta de ??gua' : regiao[4],
                'Motivo da Falta de ??gua' : regiao[5]
            }
            cei_list.append(cei_dict)
    return cei_list
cei_list = get_cei()


if len(list(infos_ceilandia.find())) == 0:
    for new_data in cei_list:
        inputDB(new_data)
        post_tweet(message_tweet(new_data))
else:
    updateDB(cei_list)


