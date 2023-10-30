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
    awards = open('awards_corpus.txt', 'w', encoding='utf-8')
    presenters = open('presenter_corpus.txt', 'w', encoding='utf-8')
    nominees = open('nominee_corpus.txt', 'w', encoding='utf-8')
    golden_globe_awards = open('golden_globe_awards.txt', 'w', encoding='utf-8')
    for i in tweets:
        text = word_tokenize(i)
        if re.search(r'\b(RT @goldenglobes)\b', i) or re.search(r'\b(RT @TVGuide)\b', i) and name == 'gg_awards':
            golden_globe_awards.write(f"{i}\n")
        elif text[0] == 'RT':
            continue
        elif re.search(r'\b(won|wins|win)\b', i) and name == "won":
            win.write(f"{i}\n")
        elif 'Congratulations' in text or 'congratulations' in text and name == "congrats":
            congrats.write(f"{i}\n")
        elif re.search(r'\b(hosts?|host)\b', i) and name == "hosts":
            host.write(f"{i}\n")
        elif re.search(r'(?i)win(s)?\s+best|won\s+best|winning\s+best', i) and name == "awards":
            award_text = re.sub(r'[^a-zA-Z0-9]+', ' ', i).lower()
            awards.write(f"{award_text}\n")
        elif re.search(r'\b(no win)\b', i) or re.search(r'\b(nominated)\b', i) or re.search(r'\b(does not)\b', i) or re.search(r'\b(did not)\b', i) or re.search(r'\b(nominated)\b', i) or re.search(r'\b(should have won)\b', i) or re.search(r'\b(did\'nt win)\b', i) or re.search(r'\b(won over)\b', i) and name == "nominees":
            nominee_text = re.sub(r'[^a-zA-Z0-9]+', ' ', i).lower()
            nominees.write(f"{nominee_text}\n")
        elif re.search(r'\b(presents)\b', i) or re.search(r'\b(presented)\b', i) or re.search(r'\b(presenting)\b', i) and name == "presenters":
            presenter_text = re.sub(r'[^a-zA-Z0-9]+', ' ', i).lower()
            presenters.write(f"{presenter_text}\n")

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
        text = [line.strip() for line in file.readlines()]

    # combined_pattern = r'\b(won|wins|win)\b(.*?)\b(for|at|takes|yet|goes|he|her|their|but|is|oh)\b'
    stopwords = ['for', 'at', 'and', 'while', 'who', 'did', 'not', 'takes', 'goes', 'yet', 'goes', 'he', 'her', 'their', 'but', 'is', 'oh', 'goldenglobes', 'globe', 'golden', 'http', 'via']
    stop_words_pattern = "|".join(map(re.escape, stopwords))
    # pattern = r'wins\s+(.*?)\s+(?:for|at)'
    pattern = rf'wins\s+(.*?)\s+(?:{stop_words_pattern})'

    for i in text:
        award = re.search(pattern, i)
        if award and len(award.group(1).split(' ')) >= 3:
            award_names_file.write(f"{award.group(1)}\n")

def find_awards_v2():
    with open('golden_globe_awards.txt', 'r', encoding='utf-8') as file:
        text = [line.strip() for line in file.readlines()]
    awards_and_winners = open('awards_and_winners.txt', 'w', encoding='utf-8')
    awards = open('awards.txt', 'w', encoding='utf-8')
    winners = open('winners.txt', 'w', encoding='utf-8')

    pattern_1 = r': (.*?)\('
    pattern_2 = r': (.*?)\#'
    award_map = dict()
    for i in text:
        award_1 = re.search(pattern_1, i)
        award_2 = re.search(pattern_2, i)
        if award_1:
            matched_award = award_1.group(1)
            split_award = matched_award.split('-')
            num = len(split_award)
            if 'Best' in split_award[0][0:4]:
                if num == 2:
                    text_award = f"{split_award[0].strip().lower()}"
                    text_winner = f"{split_award[1].strip().lower()}"
                    if text_award not in award_map:
                        award_map[text_award] = text_winner
                elif num >= 3:
                    text_award = f"{split_award[0].strip().lower()} {split_award[1].strip().lower()}"
                    text_winner = f"{split_award[2].strip().lower()}"
                    if text_award not in award_map:
                        award_map[text_award] = text_winner
        if award_2:
            matched_award = award_2.group(1)
            split_award = matched_award.split('-')
            num = len(split_award)
            if 'Best' in split_award[0][0:4]:
                if num == 4 and '@' not in split_award[2]:
                    text_award = f"{split_award[0].strip().lower()}"
                    text_winner = f"{split_award[1].strip().lower()}"
                    if text_award not in award_map and len(text_winner.split()) > 1 and 'or' not in text_winner:
                        award_map[text_award] = text_winner
                if num == 5:
                    text_award = f"{split_award[0].strip().lower()} {split_award[1].strip().lower()}"
                    text_winner = f"{split_award[2].strip().lower()}"
                    if text_award not in award_map:
                        award_map[text_award] = text_winner

    for key in award_map:
        awards.write(f"{key}\n")
        winners.write(f"{award_map[key]}\n")

    
def verify_person(person_name):
    name_pattern = re.compile(r'\s')
    if re.search(name_pattern, person_name):
        return person_name

def group_awards():
    award_groups = open('award_groups.txt', 'w', encoding='utf-8')
    with open('award_names.txt', 'r', encoding='utf-8') as file:
        award_names = [line for line in file.readlines()]

    award_count = Counter(award_names)

    for key in award_count.most_common():
        if key[1] > 2:
            award_groups.write(f"{key[0]}")

def find_winners():
    with open('award_groups.txt','r',encoding='utf-8') as file:
        award_list = [line.strip() for line in file.readlines()] #make sure to strip new lines
    with open('awards.txt', 'r', encoding='utf-8') as file:
        award_corpus = [line for line in file.readlines()]
    winner_file = open("winners.txt", 'w', encoding='utf-8')

    for award in award_list:
        pattern = rf"(.+?)\s+(wins|win|won)\s+{award}"
        for line in award_corpus:
            winner = re.search(pattern, line)
            if winner:
                # print(f"{winner}, {award}")
                winner_file.write(f"{winner.group(1)}, {award}\n")

def counter_winners():
    result = {}

    with open('winners.txt', 'r', encoding='UTF-8') as file:
        lines = [line.strip() for line in file.readlines()]

    for line in lines:
        key = line.split(',')[1]
        value = line.split(',')[0]
        if key in result:
            result[key].append(value)
        else:
            result[key] = [value]

    # print(result)
    top_winners_file = open("top_winners.txt", 'w', encoding='utf-8')

    for key in result.keys():
        win_count = Counter(result[key])
        # print(f"keys: {key}, {win_count}")

        # Finding number one winner
        top_winners_file.write(f"{key}, {max(win_count, key=win_count.get)}\n")

def count_nominees():
    nominee_map = dict()
    names = []

    with open("awards.txt", 'r', encoding='utf-8') as file:
        awards = [line.strip() for line in file.readlines()]
    with open("winners.txt", 'r', encoding='utf-8') as file:
        winners = [line.strip() for line in file.readlines()]
    with open("nominee_corpus.txt", 'r', encoding='utf-8') as file:
        nominee_corpus = file.read()

    doc = NLP(nominee_corpus) # Open file
    entities = [ent for ent in doc.ents]
    for ent in entities:
        names.append(str(ent))

    name_count = Counter(names)
    
    # Finding nominees
    nominees_file = open("nominees.txt", 'w', encoding='utf-8')
    for key in name_count.most_common():
        nominees_file.write(f"{key[0]}\n")

def count_presenters():
    names = []
    with open("presenter_corpus.txt", 'r', encoding='utf-8') as file:
        presenter_corpus = file.read()
    
    doc = NLP(presenter_corpus) # Open file
    entities = [ent for ent in doc.ents]
    for ent in entities:
        names.append(str(ent))

    name_count = Counter(names)

    presenters_file = open("presenters.txt", 'w', encoding='utf-8')
    for key in name_count.most_common():
        presenters_file.write(f"{key[0]}\n")

# create_text_files(name='nominees')
# find_hosts('host.txt')
# find_awards('awards.txt')
# find_awards_v2()
# group_awards()
# find_winners()
# counter_winners()
count_nominees()
count_presenters()