from flask import Flask, render_template, request, jsonify
import os
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Certifique-se de que a pasta uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    data = request.json
    photo_data = data.get('photo')
    if photo_data:
        photo_data = photo_data.split(',')[1]
        photo_bytes = base64.b64decode(photo_data)
        filename = secure_filename('photo.png')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(photo_bytes)
        return jsonify({"message": "Photo uploaded successfully!", "filepath": filepath}), 200
    return jsonify({"message": "No photo data provided"}), 400

@app.route('/save_location', methods=['POST'])
def save_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if latitude and longitude:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'location.txt'), 'w') as f:
            f.write(f"Latitude: {latitude}, Longitude: {longitude}")
        return jsonify({"message": "Location saved successfully!"}), 200
    return jsonify({"message": "Invalid location data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
