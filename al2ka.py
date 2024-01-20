"""Convert Anilist activities to human readable format for volume start date and end date"""
import json
import re
from datetime import datetime

import requests

def make_anilist_request(mediaId, page = 1):
    """Makes a request to AniList"""
    url = "https://graphql.anilist.co"
    query = """
    query ($mediaId: Int, $page: Int) {
        Page(page: $page, perPage: 500) {
                activities(userId: 5613718, mediaId: $mediaId) {
                ... on ListActivity {
                    createdAt
                    media {
                        title {
                            userPreferred
                        }
                    }
                    status
                    progress
                }
            }
        }
    }
    """
    variables = {
        "mediaId": mediaId,
        "page": page
    }

    return requests.post(url, json={"query": query, "variables": variables}, timeout=60)

def check_overlaps(a, b):
    """Checks for any overlaps between two arrays"""
    for i in a:
        if i in b:
            return True
    return False

def main():
    """Entry point"""
    volumes = []

    with open("json/HellParadise.json", "r", encoding="utf8") as file:
        contents = file.read()
        jayson = json.loads(contents)
        mediaid = jayson["id"]
        volumes = jayson["volumes"]

    response = make_anilist_request(mediaid)
    if not response.ok:
        print(f"[ERROR] AniList returned an unsuccessful status code: {response.status_code}")
        exit(1)

    json_dict = response.json()
    activities = json_dict["data"]["Page"]["activities"]

    results = []
    for i, volume in enumerate(volumes):
        volume_start = volume["start"]
        volume_end = volume["end"]
        started_reading = None
        finished_reading = None

        for activity in activities:
            created = activity["createdAt"]

            # If the volume is the last volume and the activity is completed
            if volume == volumes[-1] and activity["status"] == "completed":
                if started_reading is None:
                    started_reading = created
                elif created < started_reading:
                    started_reading = created

                if finished_reading is None:
                    finished_reading = created
                elif created > finished_reading:
                    finished_reading = created
                continue

            if activity["status"] != "read chapter":
                continue

            regex = re.findall(r"(\d+)", activity["progress"])
            if regex is None:
                continue

            my_start = int(regex[0])
            my_end = int(regex[-1])
            if check_overlaps(range(volume_start, volume_end + 1), range(my_start, my_end + 1)):
                if started_reading is None:
                    started_reading = created
                elif created < started_reading:
                    started_reading = created

                if finished_reading is None:
                    finished_reading = created
                elif created > finished_reading:
                    finished_reading = created

        results.append({"volume": i + 1, "started_reading": started_reading, "finished_reading": finished_reading})

    for r in results:
        volume = r["volume"]
        finished = r["finished_reading"]
        time = datetime.utcfromtimestamp(finished).strftime("%d/%m/%Y %H:%M")
        print(f"Volume {volume}")
        print(f"Finished: {time}")
        print("------------------------")

if __name__ == "__main__":
    main()
