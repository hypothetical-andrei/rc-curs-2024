import bencodepy
import sys
import pprint

def parse_torrent(file_path):
    with open(file_path, 'rb') as f:
        data = bencodepy.decode(f.read())

    # Decode byte strings to normal strings (for readability)
    def decode_item(item):
        if isinstance(item, dict):
            return {decode_item(k): decode_item(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [decode_item(i) for i in item]
        elif isinstance(item, bytes):
            try:
                return item.decode('utf-8')
            except UnicodeDecodeError:
                return item  # Return raw bytes if not decodable
        else:
            return item

    decoded_data = decode_item(data)
    pprint.pprint(decoded_data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <torrent_file>")
    else:
        parse_torrent(sys.argv[1])
