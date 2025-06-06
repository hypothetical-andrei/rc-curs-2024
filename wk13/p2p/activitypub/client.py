import requests
import uuid

def send_note(from_user, from_server, to_actor_url, content):
    outbox_url = f"{from_server}/outbox/{from_user}"
    activity = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"{from_server}/activities/{uuid.uuid4()}",
        "type": "Create",
        "actor": f"{from_server}/actor/{from_user}",
        "object": {
            "type": "Note",
            "content": content
        },
        "to": [to_actor_url]
    }
    resp = requests.post(outbox_url, json=activity)
    print(resp.status_code, resp.text)
