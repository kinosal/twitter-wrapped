import twitter as twi


def main():
    liker_conn = twi.Twitter("kinosal")
    likes = liker_conn.fetch_all_likes_since(since="2022-01-01")
    liked_authors = liker_conn.get_liked_authors(likes=likes, number=5)
    print(liked_authors)


if __name__ == "__main__":
    main()
