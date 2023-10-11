import pandas as pd
import json
import nltk
import re
import gg_api
from nltk.tokenize import word_tokenize

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

f = open('win.text', 'w', encoding='utf-8')
for i in tweets:
    text = word_tokenize(i)
    if 'win' in text:
        f.write(f"{i}\n")




