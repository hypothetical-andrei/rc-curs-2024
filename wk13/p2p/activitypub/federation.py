import requests

def deliver(activity, recipient_inbox_url):
    try:
        res = requests.post(recipient_inbox_url, json=activity, timeout=5)
        return res.status_code == 200
    except Exception as e:
        print(f"❌ Failed to deliver: {e}")
        return False
