import os
import tweepy # https://github.com/tweepy/tweepy/tree/master/examples/API_v2
from dotenv import load_dotenv

load_dotenv()
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
consumer_secret = os.environ.get('CONSUMER_SECRETKEY')
consumer_key = os.environ.get('CONSUMER_APIKEY')
bearer_token = os.environ.get('BEARER_TOKEN')
access_token = os.environ.get('ACCESS_TOKEN')


def post_tweet(message):

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    response = client.create_tweet(text=message)
    print(response)


def message_tweet(item_dict):
    message = f'''
Falta de água! 🚨📢

Região: {item_dict["RA"]}
Áreas Afetadas: {item_dict["Áreas Afetadas"]}
Início: {item_dict["Início"]}
Normalização: {item_dict["Normalização"]}
Tipo de Falta de Água: {item_dict["Tipo de Falta de Água"]}
Motivo da Falta de Água: {item_dict["Motivo da Falta de Água"]}
'''
    return message
