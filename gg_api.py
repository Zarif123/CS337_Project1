from Project_1 import *

'''Version 0.4'''
hard_code_awards = ["best screenplay - motion picture", "best director - motion picture", "best performance by an actress in a television series - comedy or musical","best foreign language film","best performance by an actor in a supporting role in a motion picture","best performance by an actress in a supporting role in a series, mini-series or motion picture made for television","best motion picture - comedy or musical","best performance by an actress in a motion picture - comedy or musical","best mini-series or motion picture made for television","best original score - motion picture", "best performance by an actress in a television series - drama","best performance by an actress in a motion picture - drama", "cecil b. demille award", "best performance by an actor in a motion picture - comedy or musical","best motion picture - drama","best performance by an actor in a supporting role in a series, mini-series or motion picture made for television","best performance by an actress in a supporting role in a motion picture", "best television series - drama", "best performance by an actor in a mini-series or motion picture made for television","best performance by an actress in a mini-series or motion picture made for television","best animated feature film","best original song - motion picture","best performance by an actor in a motion picture - drama","best television series - comedy or musical","best performance by an actor in a television series - drama","best performance by an actor in a television series - comedy or musical"]
def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = find_hosts("host.txt")
    # print('hosts are', hosts)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards = find_awards_v2()
    # print('awards are', awards)
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = dict()
    nominees = match_nominees()
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winner_result = dict()
    find_winners()
    awards, winners = counter_winners()
    missed_awards = []

    for award in hard_code_awards:
        if award not in awards:
            missed_awards.append(award)

    for i in range(len(awards)):
        winner_result[awards[i]] = winners[i]

    for miss in missed_awards:
        winner_result[miss] = ""
    
    return winner_result

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = dict()
    presenters = match_presenters()
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    tweets = create_df()
    initial_text = create_text_files(tweets)
    print("Wrote initial text files")
    hard_award = create_hard_award_corpus(tweets)
    print("Wrote hardcoded awards text file")
    if initial_text and hard_award:
        counted_nominees = count_nominees()
        counted_presenters = count_presenters()
        if counted_nominees and counted_presenters:
            create_nominee_match_tweets(tweets)
            print("Wrote nominee match tweets")
            create_presenter_match_tweets(tweets)
            print("Wrote presenter match tweets")
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    pre_ceremony()
    hosts = get_hosts(2013)
    print("Got hosts")
    awards = get_awards(2013)
    print("Got awards")
    winners = get_winner(2013)
    print("Got winners")
    nominees = get_nominees(2013)
    print("Got nominees")
    presenters = get_presenters(2013)
    print("Got presenters")
    create_human_output(hosts, winners, nominees, presenters)
    print("Made human readable output")
    # hosts = ['amy', 'ben']
    # winners = {'django': 'william', 'pirates': 'johnny'}
    # nominees = {'django': ['carl', 'kevin'], 'pirates': ['don', 'edward']}
    # presenters = {'django': ['fred', 'guifa'], 'pirates': ['leo', 'pelt']}
    # awards = ['django', 'pirates']
    create_json_output(hosts, winners, nominees, presenters, hard_code_awards)
    print("Made json output")
    return

if __name__ == '__main__':
    main()
