"""Streamlit app."""

# Import standard libraries
import logging

# Import 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import twitter as twi

# Configure logger
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, force=True)

# Define functions
@st.experimental_memo(ttl=60*60*12, show_spinner=False)
def top_authors(account: str) -> list:
    twitter = twi.Twitter(account=account)
    likes = twitter.fetch_all_likes_since(since="2022-01-01")
    if likes:
        logging.info(f"Likes: {len(likes)}")
        return twitter.get_liked_authors(likes=likes, number=5)
    return []


# Configure Streamlit page and state
st.set_page_config(page_title="Twitter Wrapped", page_icon="🤖")

# Force responsive layout for columns also on mobile
st.write(
    """<style>
    @media (max-width: 480px) {
        [data-testid="column"] {
            min-width: calc(9% - 1rem);
            padding: 0 0.2rem;
        }
    }
    </style>""",
    unsafe_allow_html=True,
)

# Render Streamlit page
st.title("Twitter Wrapped")
st.markdown(
    """
        Generate your and other people's **Twitter Wrapped 2022** - an overview of a Twitter account's most liked Tweet authors for this year (inspired by [Spotify Wrapped](https://spotify.com/wrapped)). You can find the code for this mini-app on [GitHub](https://github.com/kinosal/twitter-wrapped) and the author on [Twitter](https://twitter.com/kinosal).
    """
)
account = st.text_input(label="Twitter account handle").replace("@", "")
if account:
    logging.info(f"Account: {account}")
    top_authors = top_authors(account=account)
    if top_authors:
        st.markdown("""---""")
        st.markdown(
            f"""
                **#TwitterWrapped 2022**\n
                Top authors for [@{account}](https://twitter.com/{account})
            """
        )
        for i, author in enumerate(top_authors):
            cols = st.columns([1, 2, 13])
            cols[0].markdown(f"**{i + 1}**")
            cols[1].image(author[0][1], width=35)
            cols[2].markdown(
                f"**[@{author[0][0]}](https://twitter.com/{author[0][0]})**"
            )
        cols = st.columns([1, 15])
        cols[0].image("twitter.png", width=25)
        cols[1].markdown(
            """Made with [twitter-likes.streamlit.app](https://twitter-likes.streamlit.app)"""
        )
        logging.info(f"Top authors: {', '.join([a[0][0] for a in top_authors])}")

        st.markdown("""---""")
        formatted_top_authors = "\n".join(
            [f"{i+1}) @{a[0][0]} " for i, a in enumerate(top_authors)]
        )
        st.markdown("Share your result on Twitter (add a screenshot  of the above list as image if you like):")
        components.html(
            f"""
                <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="#TwitterWrapped 2022\n\n@{account}'s most liked accounts:\n{formatted_top_authors}\n\nMade with" data-url="twitter-likes.streamlit.app" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            """,
            height=40,
        )

        st.markdown("""---""")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**Other Streamlit apps by [@kinosal](https://twitter.com/kinosal)**"
            )
            st.markdown("[Tweet Generator](https://tweets.streamlit.app)")
            st.markdown("[Content Summarizer](https://web-summarizer.streamlit.app)")
            st.markdown("[Code Translator](https://english-to-code.streamlit.app)")
            st.markdown("[PDF Analyzer](https://pdf-keywords.streamlit.app)")
        with col2:
            st.write("If you like this app, please consider to")
            components.html(
                """
                    <form action="https://www.paypal.com/donate" method="post" target="_top">
                    <input type="hidden" name="hosted_button_id" value="8JJTGY95URQCQ" />
                    <input type="image" src="https://pics.paypal.com/00/s/MDY0MzZhODAtNGI0MC00ZmU5LWI3ODYtZTY5YTcxOTNlMjRm/file.PNG" height="35" border="0" name="submit" title="Donate with PayPal" alt="Donate with PayPal button" />
                    <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
                    </form>
                """,
                height=45,
            )
            st.write("so I can keep it alive. Thank you!")
