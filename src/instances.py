import requests


class InstancesAPI:
    base_url = "https://instances.social/api/1.0/instances/"

    def __init__(self, token):
        self.token = token

    def list_instances(
        self, count, include_down, include_closed, min_users, language, min_id
    ):
        r = requests.get(
            self.base_url + "list",
            params={
                "count": count,
                "include_down": include_down,
                "include_closed": include_closed,
                "min_users": min_users,
            },
            headers={"Authorization": "Bearer " + self.token},
        )

        return r
        instances = r.json()
        return instances
