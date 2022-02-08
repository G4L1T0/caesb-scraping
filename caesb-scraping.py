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


