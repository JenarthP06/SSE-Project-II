from flask import Flask, jsonify, request

app = Flask(__name__)

users = {
    "1": {"username":"john_doe", "email": "john@example.com"},
    "2": {"username": "jane_smith", "email": "jane@example.com"},
}

@app.route('/user/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/user', methods=['POST'])
def create_user_profile():
    data = request.get_json()
    user_id = str(len(users) + 1)
    users[user_id] = {"username": data['username'], "email": data['email']}
    return jsonify({"message": "User created successfully", "user_id": user_id}), 201

if __name__ == '__main__':
    app.run(debug=True)   