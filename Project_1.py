import pandas as pd
import json
import nltk
import re
import gg_api
from nltk.tokenize import word_tokenize
from imdb import Cinemagoer

df = pd.read_json('gg2013.json')
tweets = df['text'] #list of tweet text
accounts = df['user'] #list of usersy

# used just for reference
def create_text_files():
    with open('gg2013.json') as f:
        d = json.load(f)
        with open('tweets.txt', "w", encoding="utf-8") as t:
            for i in d:
                t.write(f"{i['text']}\n")
        with open('users.txt', 'w', encoding='utf-8') as t:
            for i in d:
                t.write(f"{i['user']['screen_name']}\n")

congrats = open('congrats.txt', 'w', encoding='utf-8')
win = open('win.text', 'w', encoding='utf-8')
host = open('host.txt', 'w', encoding='utf-8')
presenters = open('presenters.txt', 'w', encoding='utf-8')
Nominees = open('nominees.txt', 'w', encoding='utf-8')
for i in tweets:
    text = word_tokenize(i)
    if re.search(r'\b(won|wins|win)\b', i):
        win.write(f"{i}\n")
    if 'Congratulations' in text or 'congratulations' in text:
        congrats.write(f"{i}\n")
    if re.search(r'\b(hosts?|host)\b', i):
        host.write(f"{i}\n")




