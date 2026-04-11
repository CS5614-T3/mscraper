from dotenv import dotenv_values
from supabase import create_client, Client
from mastodon import Mastodon
from mastodon.return_types import Tag
from mastodon.types_base import NonPaginatableList


class TrendsAPI:

    def __init__(self, url: str):
        self.base_url: str = url
        self.mastodonAPI = Mastodon(api_base_url=url)
        config = dotenv_values(".env")
        url: str | None = config["SUPABASE_URL"]
        key: str | None = config["SUPABASE_KEY"]

        if url is None or key is None:
            raise ValueError("No Supabase url or key provided")

        self.supabase: Client = create_client(url, key)


    def get_trends(self):
        trends: NonPaginatableList[Tag] = self.mastodonAPI.trending_tags()
        return trends

    def insert_trends(self):
        trends = self.get_trends()

        try:
            response = self.supabase.table("trends_raw").upsert(
                [{
                    "id": trend.id,
                    "name": trend.name,
                    "base_url": self.base_url,
                    "url": trend.url,
                } for trend in trends]
            ).execute()

            for trend in trends:
                response = self.supabase.table("trends_history_raw").upsert(
                [{"day": history.day,
                  "uses": history.uses,
                  "accounts": history.accounts,
                  "trend_id": trend.id
                  } for history in trend.history
                 ]
                ).execute()

        except Exception as exception:
            print(exception)
