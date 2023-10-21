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
import os

df = pd.read_json('gg2013.json')
tweets = df['text'] #list of tweet text
accounts = df['user'] #list of users
ia = IMDb()
NLP = spacy.load('en_core_web_sm') # Loads spacy model

# used just for reference
def create_text_files(name):
    with open('gg2013.json') as f:
        d = json.load(f)
        if name == "tweets":
            with open('tweets.txt', "w", encoding="utf-8") as t:
                for i in d:
                    t.write(f"{i['text']}\n")
        if name == "users":
            with open('users.txt', 'w', encoding='utf-8') as t:
                for i in d:
                    t.write(f"{i['user']['screen_name']}\n")

    congrats = open('congrats.txt', 'w', encoding='utf-8')
    win = open('win.text', 'w', encoding='utf-8')
    host = open('host.txt', 'w', encoding='utf-8')
    awards = open('awards.txt', 'w', encoding='utf-8')
    presenters = open('presenters.txt', 'w', encoding='utf-8')
    nominees = open('nominees.txt', 'w', encoding='utf-8')
    for i in tweets:
        text = word_tokenize(i)
        if text[0] == 'RT':
            continue
        if re.search(r'\b(won|wins|win)\b', i) and name == "won":
            win.write(f"{i}\n")
        if 'Congratulations' in text or 'congratulations' in text and name == "congrats":
            congrats.write(f"{i}\n")
        if re.search(r'\b(hosts?|host)\b', i) and name == "hosts":
            host.write(f"{i}\n")
        if re.search(r'(?i)win(s)?\s+best|won\s+best', i) and name == "awards":
            award_text = re.sub(r'[.!:#?@&^%$*()+=]', '', i)
            awards.write(f"{award_text}\n")

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

def find_awards(awards_file):
    award_names_file = open('award_names.txt', 'w', encoding='utf-8')

    with open(awards_file, 'r', encoding='utf-8') as file:
        text = file.read()

    win_pattern = r'\b(won|wins|win)\b'
    stop_words = r'\b(for)\b'
    combined_pattern = r'\b(won|wins|win)\b(.*?)\b(for|at|takes|yet|goes|he|her|their|but|is|oh)\b'

    awards = re.findall(combined_pattern, text)

    for i in awards:
        # print(i[1].split(' '))
        print(i)
        if len(i[1].split(' ')) >= 4 + 2:
            award_names_file.write(f"{i[1]}\n")
    

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

# create_text_files(name='awards')
# find_hosts('host.txt')
find_awards('awards.txt')



# with open('award_names.txt', 'r') as file:
#     award_names = [line.strip() for line in file.readlines()]

# os.makedirs('awardGroupings', exist_ok=True)

# def extract_named_entities(text):
#     doc = NLP(text)
#     named_entities =set([ent.text for ent in doc.ents])
#     return named_entities

# grouped_awards = {}
# for award in award_names:
#     named_entities = extract_named_entities(award)
#     key = ', '.join(sorted(named_entities))
#     if key in grouped_awards:
#         grouped_awards[key].append(award)
#     else:
#         grouped_awards[key] =[award]

# for key, group in grouped_awards.items():
#     print(f"Group:{key}\nNames:{group}\n")

# for key, group in grouped_awards.items():
#     with open(f'awardGroupings/{key}.txt', 'w') as group_file:
#         group_file.write('\n'.join(group))
