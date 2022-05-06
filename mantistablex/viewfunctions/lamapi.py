import requests
import json


class LamAPIWrapper:
    ACCESS_TOKEN = "ee4ba0c4f8db0eb3580cb3b7b5536c54"

    def __init__(self, endpoint, port=8093):
        self._endpoint = endpoint
        self._port = port

    def sameAs(self, entity):
        return self._make_request(
            lambda: requests.post(
                self._api_url("sameas"),
                json={"json": entity},
                params={"token": self.ACCESS_TOKEN},
                timeout=30 
            )
        )

    def labels(self, entity):
        return self._make_request(
            lambda: requests.post(
                self._api_url("labels"),
                json={"json": entity},
                params={"token": self.ACCESS_TOKEN, "kg": "wikidata","lang":"en"},
                timeout=30 
            )
        )

    def concepts(self, entities):
        #self._log("concepts", entities)
        return self._make_request(
            lambda: requests.post(
                self._api_url("concepts"),
                json={"json": entities},
                params={"token": self.ACCESS_TOKEN},
                timeout=30 
            )
        )

    def objects(self, subjects):
        if len(subjects) == 0:
            return {}

        self._log("objects", subjects)
        return self._make_request(
            lambda: requests.post(
                self._api_url("objects"),
                json={"json": subjects},
                params={"token": self.ACCESS_TOKEN},
                timeout=30 
            )
        )    

    def _api_url(self, suburl):
        return f"http://{self._endpoint}:{self._port}/{suburl}"

    def _make_request(self, requester):
        response = requester()
        if response.status_code != 200:
            return {}

        return response.json()

    def _log(self, endpoint_name, query):
        q = str(query).replace('\n', '')[0:10] + '...'
        print(f"LAMAPI {endpoint_name} {q}")
        

def main():
    lamapi = LamAPIWrapper("149.132.176.84", 8097)


if __name__ == "__main__":
    main()