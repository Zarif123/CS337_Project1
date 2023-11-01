from Project_1 import *

'''Version 0.4'''
hard_code_awards = ["best screenplay - motion picture", "best director - motion picture", "best performance by an actress in a television series - comedy or musical","best foreign language film","best performance by an actor in a supporting role in a motion picture","best performance by an actress in a supporting role in a series, mini-series or motion picture made for television","best motion picture - comedy or musical","best performance by an actress in a motion picture - comedy or musical","best mini-series or motion picture made for television","best original score - motion picture", "best performance by an actress in a television series - drama","best performance by an actress in a motion picture - drama", "cecil b. demille award", "best performance by an actor in a motion picture - comedy or musical","best motion picture - drama""best performance by an actor in a supporting role in a series, mini-series or motion picture made for television","best performance by an actress in a supporting role in a motion picture", "best television series - drama", "best performance by an actor in a mini-series or motion picture made for television","best performance by an actress in a mini-series or motion picture made for television","best animated feature film","best original song - motion picture","best performance by an actor in a motion picture - drama","best television series - comedy or musical","best performance by an actor in a television series - drama","best performance by an actor in a television series - comedy or musical"]
def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    tweets = create_df()
    create_text_files(tweets, name='tweets')
    create_text_files(tweets, name="gg_awards")
    create_text_files(tweets, name="nominees")
    create_text_files(tweets, name="presenters")
    create_text_files(tweets, name="hosts")
    create_nominee_match_tweets(tweets)
    create_presenter_match_tweets(tweets)
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
    return

if __name__ == '__main__':
    main()
