# pylint: disable=import-error
import re
from datetime import datetime

from anilist import make_anilist_request
from info import info
from file_operations import open_file

def check_overlaps(a, b):
    """Checks for any overlaps between two arrays"""
    for i in a:
        if i in b:
            return True
    return False

def process(file):
    volumes = []

    mediaid, volumes = open_file(file)

    response = make_anilist_request(mediaid)
    if not response.ok:
        print(f"[ERROR] AniList returned an unsuccessful status code: {response.status_code}")
        exit(1)

    json_dict = response.json()
    activities = json_dict["data"]["Page"]["activities"]

    results = []
    previous_started = None
    previous_finished = None
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

        if started_reading is not None and finished_reading is not None:
            previous_started = started_reading
            previous_finished = finished_reading
            results.append({"volume": i + 1, "started_reading": started_reading, "finished_reading": finished_reading})
        else:
            results.append({"volume": i + 1, "started_reading": previous_started, "finished_reading": previous_finished})

    output = ""
    for r in results:
        volume = r["volume"]
        finished = r["finished_reading"]
        time = datetime.utcfromtimestamp(finished).strftime("%d/%m/%Y %H:%M")
        output += f"Volume {volume}\nFinished: {time}\n------------------------\n\n"

    return info(output.strip())
