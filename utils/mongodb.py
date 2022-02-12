import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from utils.twitter import post_tweet, message_tweet

load_dotenv()
link_DB = os.environ.get('LINK_DB')

def db_cei():
    client = MongoClient(link_DB)
    db = client.get_database('incansaveis')
    infos_ceilandia = db.infos_ceilandia
    return infos_ceilandia
infos_ceilandia = db_cei()

def inputDB(new_data):
    vaiadd = infos_ceilandia.insert_one(new_data)
    print(f'\033[0;32m[ + ]\033[0;0m ObjectId("{vaiadd.inserted_id}")')


DB_ultimos_dez = list(infos_ceilandia.find())[-10:]


def updateDB(list_dict):
    for cei_item in list_dict:
        contador = 0
        
        atual_area = cei_item['Áreas Afetadas']
        atual_normalizacao = cei_item['Normalização'] 

        for DB_item in DB_ultimos_dez:
            DB_id = DB_item['_id']
            DB_areas = DB_item['Áreas Afetadas']
            DB_normalizacao = DB_item['Normalização']
        
            if atual_area != DB_areas or atual_normalizacao != DB_normalizacao:
                contador += 1

        if contador == len(DB_ultimos_dez):
            inputDB(cei_item)
            post_tweet(message_tweet(cei_item))


# infos_ceilandia.drop()


