import requests
import json

operation_name = "CollectionRevisionMods"
query = """
  query CollectionRevisionMods($slug: String!, $revision: Int, $viewAdultContent: Boolean = false) {
  collectionRevision(
    slug: $slug
    revision: $revision
    viewAdultContent: $viewAdultContent
  ) {
    externalResources {
      ...ExternalResourceFields
    }
    modFiles {
      file {
        ...ModFileFields
      }
      fileId
      optional
    }
  }
}
fragment ExternalResourceFields on ExternalResource {
  id
  name
  resourceType
  resourceUrl
}
fragment ModFileFields on ModFile {
  fileId
  mod {
    game {
      domainName
    }
    modId
    version
  }
}
"""


class NexusModsGraphql:
    def __init__(self, cookies_path: str = "cookies.json"):
        self.graphql_url = "https://api-router.nexusmods.com/graphql/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            # "x-graphql-operationname": "CollectionRevisionMods",
            "Referer": "https://www.nexusmods.com/",
            "Content-Type": "application/json",
        }
        self.cookies = self._load_cookies(cookies_path)

    def _load_cookies(self, cookies_path: str) -> dict:
        try:
            with open(cookies_path, "r") as f:
                cookies_list = json.load(f)
            return {cookie["name"]: cookie["value"] for cookie in cookies_list}
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return {}

    def _get_raw_data(self, url_collection: str) -> dict:
        url_collection = url_collection.lower().replace("https://", "")
        splitted_url = url_collection.split("/")
        slug = splitted_url[4]

        formatted_json = {
            "operationName": operation_name,
            "query": query,
            "variables": {
                "slug": slug,
                "viewAdultContent": True,
            },
        }

        response = requests.post(
            self.graphql_url,
            data=json.dumps(formatted_json),
            headers=self.headers,
            cookies=self.cookies,
        )

        return response.json()

    def get_mods(self, url_collection: str) -> list:
        raw_data = self._get_raw_data(url_collection)
        mod_urls = {"internal_resources": [], "external_resources": []}

        for mod_file in raw_data["data"]["collectionRevision"]["modFiles"]:
            mod = mod_file["file"]["mod"]
            domain_name = mod["game"]["domainName"]
            mod_id = mod["modId"]
            file_id = mod_file["file"]["fileId"]

            mod_urls["internal_resources"].append(
                {
                    "mod_id": mod_id,
                    "game_domain": domain_name,
                    "version": mod["version"],
                    "file_id": file_id,
                    "url": f"https://www.nexusmods.com/{domain_name}/mods/{mod_id}?tab=files&file_id={file_id}&nmm=1",
                }
            )

        for external_resource in raw_data["data"]["collectionRevision"][
            "externalResources"
        ]:
            mod_urls["external_resources"].append(
                {
                    "name": external_resource["name"],
                    "resource_type": external_resource["resourceType"],
                    "resource_url": external_resource["resourceUrl"],
                }
            )

        return mod_urls
