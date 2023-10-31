from textblob import TextBlob
import re

exclude_words = ['best', 'supporting']
result = {}


def get_sentiment(winner=True):
    if winner:
        with open('tweets.txt', 'r', encoding='UTF-8') as file:
            tweets = [line.strip() for line in file.readlines()]
        with open('top_winners.txt', 'r', encoding='UTF-8') as file:
            winners = [line.split(',')[1].strip() for line in file.readlines()]
        sentiment_winner = open("sentiment_winner.txt", 'w', encoding='utf-8')

    # pdb.set_trace()
    for winner in winners:
        score = 0
        for tweet in tweets:
            if re.search(winner, tweet):
                for word in exclude_words:
                    tplist = [w for w in tweet if w.lower() != word]
                sentence = " ".join(tplist)
                analysis = TextBlob(sentence)
                # score += analysis.sentiment.polarity
                if analysis.sentiment.polarity > 0:
                    score += 1
                if analysis.sentiment.polarity < 0:
                    score -= 1

        if score > 0:
            sentiment_winner.write(f"{winner}, {score}, positive\n")
        elif score < 0:
            sentiment_winner.write(f"{winner}, {score}, negative\n")
        else:
            sentiment_winner.write(f"{winner}, {score}, neutral\n")

# get_sentiment()
