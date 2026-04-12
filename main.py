
from dotenv import dotenv_values
from supabase import Client, create_client

from src.instances import InstancesAPI
from src.trends import TrendsAPI


def main():
    config = dotenv_values(".env")
    url: str | None = config["SUPABASE_URL"]
    key: str | None = config["SUPABASE_KEY"]

    if url is None or key is None:
        raise ValueError("No Supabase url or key provided")

    supabase: Client = create_client(url, key)

    instances = get_instances()["instances"]

    # Unpack the info object into the main object
    [instance.update(instance.pop("info", None)) for instance in instances]

    # Load instances into instances_raw
    try:
        response = supabase.table("instances_raw").upsert(instances).execute()
    except Exception as exception:
        print(exception)

    for instance in instances:
        # load instance data into snapshot table
        try:
            response = supabase.table("instances_snapshot_raw").insert({
                "id": instance["id"],
                "users": instance[ "users" ],
                "statuses": instance["statuses"],
                "connections": instance[ "connections"],
                "active_users": instance["active_users"]
                }).execute()
        except Exception as exception:
            print(exception)

        trendAPI = TrendsAPI(instance["name"])
        trendAPI.insert_trends()

def get_instances():
    config = dotenv_values(".env")
    instances_api = InstancesAPI(config["INSTANCES_SECRET"])
    instances = instances_api.list_instances(100, "false", "false", 100, "", "").json()
    return instances

if __name__ == "__main__":
    main()
