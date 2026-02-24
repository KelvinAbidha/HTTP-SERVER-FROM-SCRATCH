from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# In-memory user store (for demonstration purposes)
users = {}

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if username in users and users[username] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if username in users:
        return jsonify({'message': 'User already exists'}), 409

    users[username] = password

    # Make a request to the data service to create a profile
    try:
        profile_data = {'username': username, 'profile_data': 'Default profile'}
        # The hostname 'data-service' is resolvable because of Docker's internal networking
        response = requests.post('http://data-service:5001/data/profile', json=profile_data)
        if response.status_code == 201:
            return jsonify({'message': 'User registered and profile created'}), 201
        else:
            return jsonify({'message': 'User registered, but profile creation failed'}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({'message': 'User registered, but data service is unavailable'}), 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
