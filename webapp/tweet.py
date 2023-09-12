
from django.conf import settings
from django.db.transaction import atomic
from django.contrib.auth.models import User

from webapp.models import SearchQuery, SearchResult

import tweepy
from textblob import TextBlob


def fetch_tweets_for_query(query: str):
    """ Fetch query for searched query """

    auth= tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

    api=tweepy.API(auth)

    public_tweets=api.search_tweets(q=query, lang="en")

    tweet_list = []

    for tweet in public_tweets:
        
        tweet_text = tweet.text

        analysis = TextBlob(tweet.text)
        
        polarity = analysis.polarity

        if(polarity > 0):
            polarity_text = "Overall tweet is POSITIVE!,Polarity value is {:3f}".format(polarity)

        if(polarity == 0):
            polarity_text = "Overall Tweet is Neutral!,Polarity value is {:3f}".format(polarity)

        if(polarity < 0):
            polarity_text = "Overall Tweet is Negative!,Polarity value is {:3f}".format(polarity)


        subjectivity = analysis.subjectivity

        if(subjectivity == 0):
            subjectivity_text = "Overll Tweet is Very Objective!,Subjectivity value is {:3f}".format(subjectivity)

        if(subjectivity == 1):
            subjectivity_text = "Overall Tweet is Very Subjective!,Subjectivity value is {:3f}".format(subjectivity)

        if(subjectivity == 0.5):
            subjectivity_text = "Overall Tweet is Neutral towards the topic!,Subjectivity value is {:3f}".format(subjectivity)

        if(subjectivity < 0.5):
            subjectivity_text = "Overall tweet is Objective!,Subjectivity value is {:3f}".format(subjectivity)

        if(subjectivity > 0.5):
            subjectivity_text = "Overall Tweet is Subjective!, Subjectivity value is {:3f}".format(subjectivity)

        tweet_list.append({
            "tweet": tweet_text,
            "polarity": {
                "value": round(polarity,3),
                "text": polarity_text,
            },
            "subjectivity": {
                "value": round(subjectivity,3),
                "text": subjectivity_text,
            },
        })

    return tweet_list



@atomic
def save_query_and_result(user_id: int, query: str, tweet_list: list) -> None:

    user = User.objects.get(id = user_id)

    query_obj = SearchQuery(user = user, query = query)
    query_obj.save()

    for tweet in tweet_list:
        result_obj = SearchResult(query_id = query_obj, tweet=tweet['tweet'], polarity=tweet['polarity']['value'], subjectivity=tweet['subjectivity']['value'], polarity_text=tweet['polarity']['text'], subjectivity_text=tweet['subjectivity']['text'])
        result_obj.save()

    query_list = SearchResult.objects.filter(query_id = query_obj)
    return query_list

