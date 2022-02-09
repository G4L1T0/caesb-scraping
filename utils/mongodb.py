import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
link_DB = os.environ.get('LINK_DB')

client = MongoClient(link_DB)
db = client.get_database('incansaveis')
infos_ceilandia = db.infos_ceilandia


def inputDB(new_data):
    vaiadd = infos_ceilandia.insert_one(new_data)
    print(f'_id:ObjectId("{vaiadd.inserted_id}")')


def updateDB(cei_dictJSON):
    if len(list(infos_ceilandia.find())) == 0:
        inputDB(cei_dictJSON)
        print('First data!')
    else:
        DB_ultimo_item = list(infos_ceilandia.find())[-1]
        normalizacao_DB = DB_ultimo_item['Normalização']
        endereco_DB = DB_ultimo_item['Áreas Afetadas']

        if endereco_DB != cei_dictJSON['Áreas Afetadas'] or normalizacao_DB != cei_dictJSON['Normalização']:
            inputDB(cei_dictJSON)
            print('New info in DB')


# infos_ceilandia.drop()

