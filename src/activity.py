
from dotenv import dotenv_values
from supabase import create_client, Client
from mastodon import Mastodon
from mastodon.return_types import Activity
from mastodon.types_base import NonPaginatableList


class ActivityAPI:

    def __init__(self, url: str):
        self.base_url: str = url
        self.mastodonAPI = Mastodon(api_base_url=url)
        config = dotenv_values(".env")
        url: str | None = config["SUPABASE_URL"]
        key: str | None = config["SUPABASE_KEY"]

        if url is None or key is None:
            raise ValueError("No Supabase url or key provided")

        self.supabase: Client = create_client(url, key)


    def get_activity(self):
        activity: NonPaginatableList[Activity] = self.mastodonAPI.instance_activity()
        return activity

    def insert_activity(self):
        activities = self.get_activity()

        try:
            response = self.supabase.table("activity_raw").upsert(
                [{
                    "base_url": self.base_url,
                    "week": activity.week.isoformat(),
                    "logins": activity.logins,
                    "registrations": activity.registrations,
                    "statuses": activity.statuses
                } for activity in activities]
            ).execute()

        except Exception as exception:
            print(exception)
