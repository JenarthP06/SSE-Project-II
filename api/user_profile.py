from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from supabase.client import create_client
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Supabase client
url = os.environ.get("supabase_url")
key = os.environ.get("supabase_key")
supabase = create_client(url, key)

# Check if the username already exists
data, count = supabase.table('users').select('*').execute()

db = SQLAlchemy(app)

# Storing credentials
@app.route('/store_credentials', methods=['POST'])
def store_credentials():
    data = request.get_json()

    # Extract username and password from the request data
    username = data.get('username')
    password = data.get('password')

    if username and password:
        # Simulate storing user credentials in the Supabase database
        new_user_data = {"username": username, "password": password}
        supabase.table('user_credentials').upsert([new_user_data], on_conflict=['username'])

        return jsonify({"message": "Credentials stored successfully"}), 201
    else:
        return jsonify({"error": "Missing username or password"}), 400

# Presenting user information
@app.route('/user_profile/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({"username": user.get("username", "N/A")})
    else:
        return jsonify({"error": "User not found"}), 404
    
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)   