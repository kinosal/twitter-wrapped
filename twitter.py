"""Twitter API connector."""

# Import from standard library
import os
from datetime import datetime
import pytz
import logging

# Import from 3rd party libraries
import streamlit as st
import tweepy

# Assign credentials from environment variable or streamlit secrets dict
consumer_key = os.getenv("TWITTER_CONSUMER_KEY") or st.secrets["TWITTER_CONSUMER_KEY"]
consumer_secret = (
    os.getenv("TWITTER_CONSUMER_SECRET") or st.secrets["TWITTER_CONSUMER_SECRET"]
)
access_key = os.getenv("TWITTER_ACCESS_KEY") or st.secrets["TWITTER_ACCESS_KEY"]
access_secret = (
    os.getenv("TWITTER_ACCESS_SECRET") or st.secrets["TWITTER_ACCESS_SECRET"]
)

# Assign timezone for datetime object comparisons
utc = pytz.UTC


class Twitter:
    """Twitter API connector."""

    def __init__(self, account):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)
        self.account = account.replace("@", "")

    def fetch_likes(self, max_id: str = None) -> list:
        """Fetch a batch of likes for an account."""
        try:
            return self.api.get_favorites(
                screen_name=self.account,
                count=200,
                max_id=max_id,
            )
        except tweepy.errors.NotFound as e:
            logging.error(str(e).split("\n")[0])
            st.error("Account not found")
            return []
        except tweepy.errors.Unauthorized as e:
            logging.error(str(e).split("\n")[0])
            st.error("Unauthorized")
            return []
        except Exception as e:
            logging.error(e)
            return []

    def fetch_all_likes_since(self, since: str, until: str) -> list:
        """Fetch all likes between two dates for an account."""
        likes = self.fetch_likes()
        if not likes:
            return []

        response_length = len(likes)

        try:
            while (
                likes[-1].created_at >= utc.localize(datetime.fromisoformat(since))
                and response_length >= 190  # API sometimes returns less than 200 likes
            ):
                response = self.fetch_likes(max_id=likes[-1].id - 1)
                likes.extend(response)
                response_length = len(response)
        except Exception as e:
            logging.error(e)

        return [
            like
            for like in likes
            if like.created_at >= utc.localize(datetime.fromisoformat(since))
            and like.created_at <= utc.localize(datetime.fromisoformat(until))
        ]

    @staticmethod
    def get_liked_authors(likes: list, number: int = -1) -> dict:
        """Get the most liked authors for a list of likes."""
        authors = [
            (like.user.screen_name, like.user.profile_image_url) for like in likes
        ]
        author_counts = {author: authors.count(author) for author in set(authors)}
        return list(sorted(author_counts.items(), key=lambda x: x[1], reverse=True))[
            :number
        ]
