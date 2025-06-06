import requests

def webfinger_lookup(username, domain):
    resource = f"acct:{username}@{domain}"
    url = f"https://{domain}/.well-known/webfinger?resource={resource}"

    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        print(f"✅ Found WebFinger record for {username}@{domain}:\n")
        for link in data.get('links', []):
            rel = link.get('rel', 'N/A')
            href = link.get('href', 'N/A')
            type_ = link.get('type', 'N/A')

            print(f"- rel: {rel}")
            print(f"  href: {href}")
            print(f"  type: {type_}")
            print()

    except Exception as e:
        print(f"❌ WebFinger lookup failed: {e}")

# Example usage
webfinger_lookup("gargron", "mastodon.social")
