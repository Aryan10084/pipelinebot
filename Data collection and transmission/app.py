from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Store incoming data
sensor_data = []

@app.route('/data', methods=['POST'])
def receive_data():
    global sensor_data
    data = request.json
    data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    sensor_data.append(data)
    print(f"Received: {data}")
    return jsonify({"status": "success"})

@app.route('/')
def index():
    return render_template('index.html', data=sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
