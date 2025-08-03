from flask import Flask, request, jsonify
import sqlite3
import json
import bcrypt

app = Flask(__name__)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def home():
    return "User Management System"

@app.route('/users', methods=['GET'])
def get_all_users():
    cursor.execute("SELECT id,name,email FROM users")
    users = cursor.fetchall()
    
    return jsonify({"status": "success", "data": users}), 200

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = json.loads(request.get_data())

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password cannot be empty"}), 400

    if '@' not in email or '.' not in email:
        return jsonify({"error": "Invalid email format"}), 400

    # hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, hashed_password)
    )
    conn.commit()

    print("User created successfully!")
    return jsonify({"message": "User created"}), 201


@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_data()
    data = json.loads(data)
    
    name = data.get('name')
    email = data.get('email')
    
    if name and email:
        try:
            cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
            conn.commit()
            return jsonify({"status": "success", "message": "User updated"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
    else:
        return jsonify({"status": "error", "message": "Name and email are required"}), 400


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return jsonify({"status": "success", "message": f"User {user_id} deleted"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error deleting user: {str(e)}"}), 500
    
    
@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400
    
    # Use parameterized query to prevent SQL injection
    query = "SELECT id, name, email  FROM users WHERE name LIKE ?"
    cursor.execute(query, (f"%{name}%",))

    users = cursor.fetchall()
    return jsonify(users)

    

@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.get_data())

    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if '@' not in email or '.' not in email:
        return jsonify({"error": "Invalid email format"}), 400

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        stored_password = user[3]  # assuming password is the 4th column (index 3)
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return jsonify({"status": "success", "user_id": user[0]})
        else:
            return jsonify({"status": "failed", "error": "Incorrect password"}), 401
    else:
        return jsonify({"status": "failed", "error": "User not found"}), 404
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)