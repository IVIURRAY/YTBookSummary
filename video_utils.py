import os

import requests
import time

def get_video_id(summary_text:str):
    url = "https://api.d-id.com/talks"
    payload = {
        "script": {
            "type": "text",
            "provider": {
                "type": "microsoft",
                "voice_id": "Jenny"
            },
            "ssml": "false",
            "input": summary_text
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": "https://create-images-results.d-id.com/api_docs/assets/noelle.jpeg"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {os.getenv('D_ID_API_KEY')}"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["id"]


def get_video_url(id:str):
    url = f"https://api.d-id.com/talks/{id}"

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {os.getenv('D_ID_API_KEY')}"
    }
    for _ in range(1000):
        response = requests.get(url, headers=headers)
        try:
            return response.json()["result_url"]
        except KeyError:
            pass
        time.sleep(5)
        print("result_url not found, trying again...")


if __name__ == "__main__":
    summary = "This is a test."
    video_id = get_video_id(summary)
    print(video_id)
    video_url = get_video_url(video_id)
    print(video_url)
