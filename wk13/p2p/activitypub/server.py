from flask import Flask, request, jsonify
import uuid
from urllib.parse import urlparse
from data import users, inboxes, outboxes
from federation import deliver

app = Flask(__name__)
BASE_URL = None  # Set dynamically

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    users[username] = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"{BASE_URL}/actor/{username}",
        "type": "Person",
        "name": username,
        "inbox": f"{BASE_URL}/inbox/{username}",
        "outbox": f"{BASE_URL}/outbox/{username}"
    }
    inboxes[username] = []
    outboxes[username] = []
    return jsonify(users[username])

@app.route('/actor/<username>')
def actor(username):
    if username in users:
        return jsonify(users[username])
    return jsonify({'error': 'not found'}), 404

@app.route('/inbox/<username>', methods=['POST'])
def inbox(username):
    if username not in inboxes:
        return jsonify({'error': 'user not found'}), 404
    activity = request.json
    inboxes[username].append(activity)
    return jsonify({'status': 'received'})

@app.route('/outbox/<username>', methods=['POST'])
def outbox(username):
    if username not in outboxes:
        return jsonify({'error': 'user not found'}), 404
    activity = request.json
    outboxes[username].append(activity)

    # Deliver to all recipients
    for target in activity.get('to', []):
        parsed = urlparse(target)
        recipient_actor_url = target
        try:
            res = requests.get(recipient_actor_url)
            recipient_actor = res.json()
            recipient_inbox = recipient_actor['inbox']
            success = deliver(activity, recipient_inbox)
            print(f"Deliver to {recipient_actor_url} -> {'✅' if success else '❌'}")
        except Exception as e:
            print(f"Failed to resolve actor {target}: {e}")

    return jsonify({'status': 'sent'})

@app.route('/inbox/<username>', methods=['GET'])
def get_inbox(username):
    return jsonify(inboxes.get(username, []))

@app.route('/outbox/<username>', methods=['GET'])
def get_outbox(username):
    return jsonify(outboxes.get(username, []))

def start_server(base_url, port):
    global BASE_URL
    BASE_URL = base_url
    app.run(port=port)
