import bencodepy
import hashlib
import random
import requests
import socket
import urllib.parse
import sys
import struct

def load_torrent(filename):
    with open(filename, 'rb') as f:
        data = bencodepy.decode(f.read())
    return data

def get_info_hash(torrent_dict):
    info = bencodepy.encode(torrent_dict[b'info'])
    return hashlib.sha1(info).digest()

def generate_peer_id():
    return b'-PC0001-' + bytes(''.join([str(random.randint(0, 9)) for _ in range(12)]), 'utf-8')

def get_http_tracker(torrent_dict):
    # Check main announce URL first
    if b'announce' in torrent_dict:
        primary = torrent_dict[b'announce'].decode()
        if primary.startswith('http'):
            return primary

    # Check announce-list if present
    if b'announce-list' in torrent_dict:
        for tier in torrent_dict[b'announce-list']:
            for url in tier:
                url_str = url.decode()
                if url_str.startswith('http'):
                    return url_str

    return None

def build_tracker_url(announce_url, torrent_dict, info_hash, peer_id, port=6881):
    params = {
        'info_hash': info_hash,
        'peer_id': peer_id,
        'port': port,
        'uploaded': 0,
        'downloaded': 0,
        'left': torrent_dict[b'info'].get(b'length', 0),
        'compact': 1,
        'event': 'started'
    }

    return announce_url + '?' + urllib.parse.urlencode(
        {k: v if not isinstance(v, bytes) else v for k, v in params.items()},
        quote_via=urllib.parse.quote
    )

def parse_peers(peers_binary):
    peers = []
    for i in range(0, len(peers_binary), 6):
        ip = socket.inet_ntoa(peers_binary[i:i+4])
        port = struct.unpack('>H', peers_binary[i+4:i+6])[0]
        peers.append((ip, port))
    return peers

def main(torrent_file):
    torrent = load_torrent(torrent_file)
    info_hash = get_info_hash(torrent)
    peer_id = generate_peer_id()

    tracker_url = get_http_tracker(torrent)
    if not tracker_url:
        print("❌ No HTTP(S) tracker found in the torrent file.")
        return

    url = build_tracker_url(tracker_url, torrent, info_hash, peer_id)
    print(f"Connecting to tracker: {tracker_url}")

    try:
        response = requests.get(url, timeout=5)
        tracker_data = bencodepy.decode(response.content)
    except Exception as e:
        print(f"❌ Failed to contact tracker: {e}")
        return

    if b'peers' in tracker_data:
        peers = parse_peers(tracker_data[b'peers'])
        print(f"✅ Found {len(peers)} peers:")
        for ip, port in peers:
            print(f"- {ip}:{port}")
    else:
        print("⚠️ No peers returned by the tracker.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <torrent_file>")
    else:
        main(sys.argv[1])
