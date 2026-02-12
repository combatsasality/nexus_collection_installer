from nexus_graphql import NexusModsGraphql
from selenium_wrapper import SeleniumWrapper
import os

while True:
    if not os.path.exists("cookies.json"):
        print("You need to create a cookies.json file with your Nexus Mods cookies.")
        print("Read the README.md for more information.")
        break

    url_collection = input("Enter the URL of the Nexus Mods collection: ")
    if url_collection.lower() == "exit":
        break

    nexus_graphql = NexusModsGraphql()
    mods = nexus_graphql.get_mods(url_collection)

    selenium_wrapper = SeleniumWrapper()
    selenium_wrapper.set_cookies()

    for mod in mods["internal_resources"]:
        selenium_wrapper.open_new_tab_and_start_downloading(
            mod["url"],
        )

    print("You have external resources, please download them manually:\n")
    for mod in mods["external_resources"]:
        print(mod["url"] + "\n")
