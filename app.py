"""Streamlit app."""

# Import standard libraries
import logging

# Import 3rd party libraries
import streamlit as st

# Import modules
import twitter as twi

# Configure logger
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, force=True)


# Define functions
def top_authors(account: str) -> list:
    twitter = twi.Twitter(account=account)
    likes = twitter.fetch_all_likes_since(since="2022-01-01")
    if likes:
        logging.info(f"Likes: {len(likes)}")
        return twitter.get_liked_authors(likes=likes, number=5)
    return []


# Render Streamlit page
st.set_page_config(page_title="Twitter Wrapped", page_icon="🤖")

st.title("Twitter Wrapped")
st.markdown(
    """
        Generate your and other people's **Twitter Wrapped 2022** - an overview of a Twitter account's most liked Tweet authors for this year (inspired by [Spotify Wrapped](https://spotify.com/wrapped)). You can find the code for this mini-app on [GitHub](https://github.com/kinosal/twitter-wrapped) and the author on [Twitter](https://twitter.com/kinosal).
    """
)
account = st.text_input(label="Twitter account")
if account:
    logging.info(f"Account: {account}")
    top_authors = top_authors(account=account)
    if top_authors:
        st.markdown("""---""")
        st.markdown(
            f"""
                **#TwitterWrapped 2022**\n
                Top authors for [@{account.replace("@", "")}](https://twitter.com/{account})
            """
        )
        for i, author in enumerate(top_authors):
            cols = st.columns([1, 2, 13])
            cols[0].markdown(f"**{i + 1}**")
            cols[1].image(author[0][1], width=40)
            cols[2].markdown(
                f"**[@{author[0][0]}](https://twitter.com/{author[0][0]})**"
            )
        cols = st.columns([1, 15])
        cols[0].image("twitter.png", width=30)
        cols[1].markdown(
            """Made with [twitter-likes.streamlit.app](https://twitter-likes.streamlit.app)"""
        )
        logging.info(f"Top authors: {', '.join([a[0][0] for a in top_authors])}")
        st.markdown("""---""")
