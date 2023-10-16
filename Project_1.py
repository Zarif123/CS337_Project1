import pandas as pd
import json
import nltk
import re
import gg_api
from nltk.tokenize import word_tokenize
from imdb import Cinemagoer
import spacy
from imdb import IMDb
from collections import Counter

df = pd.read_json('gg2013.json')
tweets = df['text'] #list of tweet text
accounts = df['user'] #list of users
ia = IMDb()
NLP = spacy.load('en_core_web_sm') # Loads spacy model

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
        if text[0] == 'RT':
            continue
        if re.search(r'\b(won|wins|win)\b', i):
            win.write(f"{i}\n")
        if 'Congratulations' in text or 'congratulations' in text:
            congrats.write(f"{i}\n")
        if re.search(r'\b(hosts?|host)\b', i):
            host.write(f"{i}\n")

def get_human_names(file_name):
    # Getting people's names from a file
    names = []

    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    doc = NLP(text) # Open file
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    for ent in entities:
        if ent[1] == 'PERSON':
            names.append(ent[0])
    return names

def find_hosts(host_file):
    host_names_file = open('host_names.txt', 'w', encoding='utf-8')
    host_list = get_human_names(host_file)
    valid_host_list = []

    for name in host_list:
        verified = verify_person(name)
        if verified != None:
            valid_host_list.append(verified)

    counter = Counter(valid_host_list)
    host_names = counter.most_common()
    highest_two = [host_names[0][0], host_names[1][0]]
    
    for i in highest_two:
        host_names_file.write(f"{i}\n")
    return highest_two

def verify_person(person_name):
    name_pattern = re.compile(r'\s')
    if re.search(name_pattern, person_name):
        return person_name
    # # Perform the search
    # if len(person_name.split(' ')) < 2:
    #     return
    # search_results = ia.search_person(person_name)

    # # Display search results
    # if search_results:
    #     for result in search_results:
    #         #print(f"Name: {result['name']}, ID: {result.personID}")
    #         return result

#create_text_files()
find_hosts('host.txt')