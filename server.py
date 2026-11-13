from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable to store the latest command for the Arduino
arduino_command = "0"  # Default to "closed"

# Define a route for "/"
@app.route('/')
def home():
    return "Welcome to the Flask Server!"

# Define other routes if needed
@app.route('/test')
def test():
    return "This is a test route!"


@app.route('/update', methods=['POST'])
def update_command():
    global arduino_command
    data = request.json
    if 'command' in data:
        arduino_command = data['command']
        return jsonify({"status": "success", "message": f"Command updated to {arduino_command}"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/command', methods=['GET'])
def get_command():
    return jsonify({"command": arduino_command}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
