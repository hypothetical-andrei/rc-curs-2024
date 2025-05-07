import requests

BASE_URL = 'http://127.0.0.1:5000'  # Adjust if your Flask app runs elsewhere

def print_response(title, response):
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:")
        print(response.json())
    except Exception:
        print(response.text)

# --- Level 0 ---
def test_level_0():
    # Request:
    # POST /api HTTP/1.1
    # Content-Type: application/json
    # 
    # {
    #     "action": "get_user",
    #     "user_id": 1
    # }
    payload = {
        "action": "get_user",
        "user_id": 1
    }
    response = requests.post(f"{BASE_URL}/api", json=payload)
    print_response("Level 0 - The Swamp of POX", response)

# --- Level 1 ---
def test_level_1():
    # Request:
    # POST /level1/users/1 HTTP/1.1
    # Content-Type: application/json
    response = requests.post(f"{BASE_URL}/level1/users/1")
    print_response("Level 1 - Resources", response)

# --- Level 2 ---
def test_level_2_get():
    # Request:
    # GET /level2/users/1 HTTP/1.1
    # Accept: application/json
    response = requests.get(f"{BASE_URL}/level2/users/1")
    print_response("Level 2 - GET User", response)

def test_level_2_put():
    # Request:
    # PUT /level2/users/1 HTTP/1.1
    # Content-Type: application/json
    # 
    # {
    #     "name": "Alice Updated"
    # }
    payload = {
        "name": "Alice Updated"
    }
    response = requests.put(f"{BASE_URL}/level2/users/1", json=payload)
    print_response("Level 2 - PUT (Update User)", response)

def test_level_2_delete():
    # Request:
    # DELETE /level2/users/2 HTTP/1.1
    # Accept: application/json
    response = requests.delete(f"{BASE_URL}/level2/users/2")
    print_response("Level 2 - DELETE User", response)

# --- Level 3 ---
def test_level_3():
    # Request:
    # GET /level3/users/1 HTTP/1.1
    # Accept: application/json
    response = requests.get(f"{BASE_URL}/level3/users/1")
    print_response("Level 3 - HATEOAS", response)

if __name__ == '__main__':
    test_level_0()
    test_level_1()
    test_level_2_get()
    test_level_2_put()
    test_level_2_delete()
    test_level_3()
