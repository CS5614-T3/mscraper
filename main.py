import json
import os
from dotenv import dotenv_values
from supabase import create_client, Client

from src.instances import InstancesAPI


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


    try:
        response = supabase.table("instances_raw").upsert(instances).execute()
    except Exception as exception:
        print(exception)


def get_instances():
    config = dotenv_values(".env")
    instances_api = InstancesAPI(config["INSTANCES_SECRET"])
    instances = instances_api.list_instances(100, "false", "false", 100, "", "").json()
    return instances

if __name__ == "__main__":
    main()
