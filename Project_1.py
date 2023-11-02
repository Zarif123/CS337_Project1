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

NLP = spacy.load('en_core_web_sm') # Loads spacy model
hard_code_awards = ["best screenplay - motion picture", "best director - motion picture", "best performance by an actress in a television series - comedy or musical","best foreign language film","best performance by an actor in a supporting role in a motion picture","best performance by an actress in a supporting role in a series, mini-series or motion picture made for television","best motion picture - comedy or musical","best performance by an actress in a motion picture - comedy or musical","best mini-series or motion picture made for television","best original score - motion picture", "best performance by an actress in a television series - drama","best performance by an actress in a motion picture - drama", "cecil b. demille award", "best performance by an actor in a motion picture - comedy or musical","best motion picture - drama","best performance by an actor in a supporting role in a series, mini-series or motion picture made for television","best performance by an actress in a supporting role in a motion picture", "best television series - drama", "best performance by an actor in a mini-series or motion picture made for television","best performance by an actress in a mini-series or motion picture made for television","best animated feature film","best original song - motion picture","best performance by an actor in a motion picture - drama","best television series - comedy or musical","best performance by an actor in a television series - drama","best performance by an actor in a television series - comedy or musical"]
sub_hard_code_awards = [re.sub(r'performance by an ', '', s) for s in hard_code_awards]

def create_df():
    df = pd.read_json('gg2013.json')
    tweets = df['text'] #list of tweet text
    return tweets

# used just for reference
def create_text_files(tweets):
    with open('gg2013.json') as f:
        d = json.load(f)
        with open('tweets.txt', "w", encoding="utf-8") as t:
            for i in d:
                t.write(f"{i['text']}\n")

    golden_globe_awards = open('golden_globe_awards.txt', 'w', encoding='utf-8')
    host = open('host.txt', 'w', encoding='utf-8')
    awards = open('awards_corpus.txt', 'w', encoding='utf-8')
    nominees = open('nominee_corpus.txt', 'w', encoding='utf-8')
    presenters = open('presenter_corpus.txt', 'w', encoding='utf-8')

    for i in tweets:
        text = word_tokenize(i)
        if re.search(r'\b(RT @goldenglobes)\b', i) or re.search(r'\b(RT @TVGuide)\b', i):
            golden_globe_awards.write(f"{i}\n")
        if text[0] == 'RT':
            continue
        if re.search(r'\b(hosts?|host)\b', i):
            host.write(f"{i}\n")
        if re.search(r'(?i)win(s)?\s+best|won\s+best|winning\s+best', i):
            award_text = re.sub(r'[^a-zA-Z0-9]+', ' ', i).lower()
            awards.write(f"{award_text}\n")
        if re.search(r'\b(no win)\b', i) or re.search(r'\b(nominated)\b', i) or re.search(r'\b(does not)\b', i) or re.search(r'\b(did not)\b', i) or re.search(r'\b(nominated)\b', i) or re.search(r'\b(should have won)\b', i) or re.search(r'\b(did\'nt win)\b', i) or re.search(r'\b(won over)\b', i):
            nominee_text = re.sub(r'[^a-zA-Z0-9]+', ' ', i)
            nominees.write(f"{nominee_text}\n")
        if re.search(r'\b(presents)\b', i) or re.search(r'\b(presented)\b', i) or re.search(r'\b(presenting)\b', i):
            presenter_text = re.sub(r'[^a-zA-Z0-9]+', ' ', i)
            presenters.write(f"{presenter_text}\n")
    return True

def create_hard_award_corpus(tweets):
    hard_code_awards_corpus = open('hard_code_awards_corpus.txt', 'w', encoding='utf-8')

    for i in tweets:
        if re.search("|".join(re.escape(elem) for elem in sub_hard_code_awards), i.lower()):
            hard_code_awards_corpus.write(f"{i}\n")
        if re.search("|".join(re.escape(elem) for elem in hard_code_awards), i.lower()):
            hard_code_awards_corpus.write(f"{i}\n")

    return True

def create_nominee_match_tweets(tweets):
    with open('nominees.txt', 'r', encoding='utf-8') as file:
        nominees = [line.strip() for line in file.readlines()]

    match_list = hard_code_awards + nominees
    pattern = "|".join(re.escape(i) for i in match_list)
    no_rt = open('match_nominees_tweets.txt', 'w', encoding='utf-8')

    for i in tweets:
        text = word_tokenize(i)
        if text[0] == 'RT':
            continue
        elif re.search(pattern, i):
            no_rt.write(f"{i}\n")

def create_presenter_match_tweets(tweets):
    with open('presenters.txt', 'r', encoding='utf-8') as file:
        presenters = [line.strip() for line in file.readlines()]

    match_list = hard_code_awards + presenters
    pattern = "|".join(re.escape(i) for i in match_list)
    no_rt = open('match_presenters_tweets.txt', 'w', encoding='utf-8')

    for i in tweets:
        text = word_tokenize(i)
        if text[0] == 'RT':
            continue
        elif re.search(pattern, i):
            no_rt.write(f"{i}\n")
    

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

def get_entity_names(file_name):
    # Getting people's names from a file
    names = []

    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    doc = NLP(text) # Open file
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    for ent in entities:
        if ent[1] == 'PERSON' or ent[1] == 'WORK_OF_ART':
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
    try:
        highest_two = [host_names[0][0], host_names[1][0]]
    except:
        highest_two = [host_names[0][0]]
    
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
    awards = open('awards.txt', 'w', encoding='utf-8')
    award_list = []
    # winners = open('winners.txt', 'w', encoding='utf-8')

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
        award_list.append(key)
        # winners.write(f"{award_map[key]}\n")
    return award_list

def verify_person(person_name):
    name_pattern = re.compile(r'^[A-Z][a-z]+ [A-Z][a-z]+$')
    if re.search(name_pattern, person_name):
        if 'golden globes' not in person_name.lower():
            return person_name
    
def verify_entity(entity_name):
    name_pattern = re.compile(r'^[A-Z][a-z]+ [A-Z][a-z]+$')
    entity_pattern = re.compile(r'^[A-Z][A-Za-z0-9\s\-.\'(),:]*$')
    if re.search(name_pattern, entity_name) or re.search(entity_pattern, entity_name):
        if 'goldenglobes' not in entity_name.lower() or 'golden globes' not in entity_name.lower():
            return entity_name

def group_awards():
    award_groups = open('award_groups.txt', 'w', encoding='utf-8')
    with open('award_names.txt', 'r', encoding='utf-8') as file:
        award_names = [line for line in file.readlines()]

    award_count = Counter(award_names)

    for key in award_count.most_common():
        if key[1] > 2:
            award_groups.write(f"{key[0]}")

def find_winners():
    with open('hard_code_awards_corpus.txt', 'r', encoding='utf-8') as file:
        award_corpus = [line.strip() for line in file.readlines()]
    winner_file = open("winner_corpus.txt", 'w', encoding='utf-8')

    for award in hard_code_awards:
        original_award = award
        sub_award = re.sub(r'performance by an ', '', award)

        pattern_1 = rf"(.+?)\s+(wins|win|won|the)\s+{sub_award}"
        pattern_2 = rf"{sub_award} -(.*?)(?:\(|#|-)"
        pattern_3 = rf"{original_award}"
        pattern_4 = rf"{sub_award}"

        for line in award_corpus:
            winner = re.search(pattern_1, line.lower())
            winner_2 = re.search(pattern_2, line.lower())
            winner_3 = re.search(pattern_3, line.lower())
            winner_4 = re.search(pattern_4, line.lower())
            if winner:
                winner_file.write(f"{winner.group(1)}% {original_award}\n")
            if winner_2:
                winner_file.write(f"{winner_2.group(1).strip()}% {original_award}\n")
            if winner_3:
                winner_file.write(f"{line.lower()}% {original_award}\n")
            if winner_4:
                winner_file.write(f"{line.lower()}% {original_award}\n")
                

def counter_winners():
    result = {}
    result_awards = []
    result_winners = []

    with open('winner_corpus.txt', 'r', encoding='UTF-8') as file:
        lines = [line.strip() for line in file.readlines()]

    for line in lines:
        key = line.split('%')[1].strip()
        value = line.split('%')[0].strip()

        if len(value.split(" ")) > 2:
            doc = NLP(value)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            for ent in entities:
                if ent[1] == 'PERSON':
                    value = ent[0]

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
        num_one = max(win_count, key=win_count.get)
        top_winners_file.write(f"{key}, {num_one}\n")

        result_awards.append(key)
        result_winners.append(num_one)
    return [result_awards, result_winners]

def count_nominees():
    verified_names = []
    names = get_entity_names("nominee_corpus.txt")
    for name in names:
        if verify_person(name) and name != 'Bill Clinton' and 'really' not in name.lower() and 'wrong' not in name.lower() and 'Smh' not in name and 'latter' not in name.lower():
            verified_names.append(name)
            
    name_count = Counter(verified_names)

    nominees_file = open("nominees.txt", 'w', encoding='utf-8')
    for key in name_count.most_common()[2:]:
        nominees_file.write(f"{key[0]}\n")
    return True

def match_nominees():
    result = dict()
    with open('nominees.txt', 'r', encoding='utf-8') as file:
        nominees = [line.strip() for line in file.readlines()]

    matched_nominees = open('matched_nominees.txt','w',encoding='utf-8')

    for award in hard_code_awards:
        match_award = award
        matched_nominees_list = []
        if "\"" in award:
            pattern = r'"[^"]*"'
            award = re.sub(pattern, '', award)
        if "comedy" in award or "drama" in award:
            pattern = r'(\bcomedy\b|\drama\b)'
            award = re.sub(pattern, r'- \1', award)

        for nominee in nominees:
            dist = find_distance('match_nominees_tweets.txt', nominee.lower(), award.lower())
            matched_nominees_list.append([dist, nominee, match_award])

        sorted_matches = sorted(matched_nominees_list, key=lambda x: x[0])
        top5_list = [[x[1],x[2]] for x in sorted_matches[:5]]
        for i in top5_list:
            if i[1] in result:
                result[i[1]].append(i[0])
            else:
                result[i[1]] = [i[0]]
            matched_nominees.write(f"{i[1]}, {i[0]}\n")

    return result

def count_presenters():
    verified_names = []
    names = get_human_names("presenter_corpus.txt")
    for name in names:
        if verify_person(name) and name != 'Bill Clinton':
            verified_names.append(name)
            
    name_count = Counter(verified_names)

    presenters_file = open("presenters.txt", 'w', encoding='utf-8')
    for key in name_count.most_common():
        presenters_file.write(f"{key[0]}\n")
    return True

def match_presenters():
    result = dict()
    with open('presenters.txt', 'r', encoding='utf-8') as file:
        presenters = [line.strip() for line in file.readlines()]

    matched_presenters = open('matched_presenters.txt','w',encoding='utf-8')

    for award in hard_code_awards:
        match_award = award
        matched_presenters_list = []
        if "\"" in award:
            pattern = r'"[^"]*"'
            award = re.sub(pattern, '', award)
        if "comedy" in award or "drama" in award:
            pattern = r'(\bcomedy\b|\drama\b)'
            award = re.sub(pattern, r'- \1', award)

        for presenter in presenters:
            dist = find_distance('match_presenters_tweets.txt', presenter.lower(), award.lower())
            matched_presenters_list.append([dist, presenter, match_award])

        sorted_matches = sorted(matched_presenters_list, key=lambda x: x[0])
        top5_list = [[x[1],x[2]] for x in sorted_matches[:2]]
        for i in top5_list:
            if i[1] in result:
                result[i[1]].append(i[0])
            else:
                result[i[1]] = [i[0]]
            matched_presenters.write(f"{i[1]}, {i[0]}\n")
    return result

def find_distance(filename, string1, string2):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().lower()
    try:
        index1 = lines.index(string1)
        index2 = lines.index(string2)
        distance = abs(index1 - index2)
        return distance
    except:
        return float('inf')

def create_human_output(hosts, winners, nominees, presenters):
    human_output_text = open('human_output_text.txt', 'w', encoding='utf-8')
    human_output_text.write("Host(s): ")
    for i in range(len(hosts)):
        if i < len(hosts):
            human_output_text.write(f"{hosts[i]},")
        else:
            human_output_text.write(f"{hosts[i]}\n")
    for award in hard_code_awards:
        human_output_text.write(f"Award: {award}\n")
        for i in range(len(presenters[award])):
            if i < len(presenters[award]):
                human_output_text.write(f"Presenters: {presenters[award][i]}\n")
            else:
                human_output_text.write(f"Presenters: {presenters[award][i]},")
        for i in range(len(nominees[award])):
            if i < len(nominees[award]):
                human_output_text.write(f"Presenters: {nominees[award][i]}\n")
            else:
                human_output_text.write(f"Presenters: {nominees[award][i]},")
        human_output_text.write(f"Winner: {winners[award]}\n\n")

def create_json_output(hosts, winners, nominees, presenters, awards):
    award_data = {}
    for award in awards:
        award_data[award] = {"nominees": nominees[award], "presenters": presenters[award], "winner": winners[award]}
    
    answer = {"hosts": hosts,
              "award_data": award_data
            }
    
    with open("student_answers2013.json", "w") as json_file:
        json.dump(answer, json_file, indent=4)
    

# create_text_files(name='nominees')
# find_hosts('host.txt')
# find_awards_v2()
# group_awards()
# find_winners()
# counter_winners()
# count_nominees()
# count_presenters()
# create_nominee_match_tweets()
# match_nominees()
# create_presenter_match_tweets()
# match_presenters()