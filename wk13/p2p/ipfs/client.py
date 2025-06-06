import requests

# Add a file (string content)
res = requests.post(
    "http://127.0.0.1:5001/api/v0/add",
    files={"file": ("hello.txt", b"Hello IPFS via raw HTTP")}
)
cid = res.json()["Hash"]
print("✅ Added file with CID:", cid)

# Fetch the file
res = requests.post(f"http://127.0.0.1:5001/api/v0/cat?arg={cid}")
print("📦 Retrieved content:", res.text)
