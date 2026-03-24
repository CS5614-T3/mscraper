from mastodon import Mastodon


def main():
    mastodon = Mastodon(api_base_url="https://mastodon.social")
    trends = mastodon.trending_tags()
    file = open("trends.json", mode="w")
    for trend in trends:
        file.write(trend.to_json())


if __name__ == "__main__":
    main()
