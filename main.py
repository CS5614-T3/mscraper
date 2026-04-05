import json
from dotenv import dotenv_values
from supabase import create_client, Client

from src.instances import InstancesAPI


def main():
    get_instances()


def get_instances():
    config = dotenv_values(".env")
    instances_api = InstancesAPI(config["INSTANCES_SECRET"])
    instances = instances_api.list_instances(1, "false", "false", 100, "", "").json()
    file = open("instances.json", mode="w")
    json.dump(instances, file, indent=2)


if __name__ == "__main__":
    main()
