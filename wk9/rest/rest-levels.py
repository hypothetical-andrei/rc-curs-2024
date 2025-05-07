from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock user data
users = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"}
}

# --- Level 0: The Swamp of POX ---
@app.route('/api', methods=['POST'])
def level_0_api():
    data = request.get_json()
    action = data.get("action")
    user_id = data.get("user_id", 1)
    
    if action == "get_user":
        user = users.get(user_id)
        if user:
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404
    return jsonify({"error": "Unknown action"}), 400

# --- Level 1: Resources (still using POST) ---
@app.route('/level1/users/<int:user_id>', methods=['POST'])
def level_1_user_resource(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# --- Level 2: Resources + HTTP Verbs ---
@app.route('/level2/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def level_2_user_operations(user_id):
    if request.method == 'GET':
        user = users.get(user_id)
        if user:
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        users[user_id] = {"id": user_id, "name": data.get("name", "Unknown")}
        return jsonify({"message": "User updated", "user": users[user_id]})

    elif request.method == 'DELETE':
        if user_id in users:
            del users[user_id]
            return jsonify({"message": "User deleted"})
        return jsonify({"error": "User not found"}), 404

# --- Level 3: HATEOAS (Hypermedia as the engine of application state) ---
@app.route('/level3/users/<int:user_id>', methods=['GET'])
def level_3_user_with_links(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user["id"],
        "name": user["name"],
        "links": {
            "self": f"/level3/users/{user_id}",
            "update": f"/level2/users/{user_id}",
            "delete": f"/level2/users/{user_id}",
            "orders": f"/users/{user_id}/orders"  # Hypothetical
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
