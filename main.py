import io
import os
from dotenv import dotenv_values
from supabase import create_client, Client

from src.instances import InstancesAPI


def main():
    config = dotenv_values(".env")
    instances_api = InstancesAPI(config["INSTANCES_SECRET"])
    instances = instances_api.list_instances(10, "false", "false", 100, "", "")
    file = io.FileIO("instances.txt", mode="w")
    file.writelines(instances)


if __name__ == "__main__":
    main()
