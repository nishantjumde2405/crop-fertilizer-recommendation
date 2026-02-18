import numpy as np
import pickle
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


# Serve the index.html file at root
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# --- Load all the saved models and encoders ---
try:
    crop_model = pickle.load(open('crop_model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    fertilizer_model = pickle.load(open('fertilizer_model.pkl', 'rb'))
    label_encoders = pickle.load(open('label_encoders.pkl', 'rb'))
    target_encoder = pickle.load(open('target_encoder.pkl', 'rb'))
except FileNotFoundError as e:
    print(f"Error loading a .pkl file: {e}")
    print("Please make sure all .pkl files are in the same directory as app.py")
    # Exit or handle the error appropriately
    exit()


# API endpoint for CROP prediction
@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    """Receives soil and weather data, returns a crop recommendation."""
    data = request.get_json()
    
    # Prepare features for crop prediction in the correct order
    try:
        crop_features = np.array([[
            data['N'], data['P'], data['K'], data['temperature'],
            data['humidity'], data['ph'], data['rainfall']
        ]])
    except KeyError as e:
        return jsonify({'error': f'Missing data for key: {e}'}), 400
    
    # Scale the features
    crop_features_scaled = scaler.transform(crop_features)
    
    # Predict the crop
    predicted_crop = crop_model.predict(crop_features_scaled)[0]
    
    return jsonify({'crop_recommendation': str(predicted_crop)})


# API endpoint for FERTILIZER prediction
@app.route('/predict_fertilizer', methods=['POST'])
def predict_fertilizer():
    """Receives soil, weather, and crop data, returns a fertilizer recommendation."""
    data = request.get_json()
    
    # Prepare features for fertilizer prediction
    try:
        fertilizer_df = {
            'Temparature': data['temperature_fert'],
            'Humidity': data['humidity_fert'],
            'Moisture': data['moisture_fert'],
            'Soil_Type': data['soil_type_fert'],
            'Crop_Type': data['crop_type_fert'],
            'Nitrogen': data['N_fert'],
            'Potassium': data['K_fert'],
            'Phosphorous': data['P_fert']
        }
    except KeyError as e:
        return jsonify({'error': f'Missing data for key: {e}'}), 400

    # Encode categorical features
    try:
        for col in ['Soil_Type', 'Crop_Type']:
            le = label_encoders[col]
            fertilizer_df[col] = le.transform([fertilizer_df[col]])[0]
    except (KeyError, ValueError) as e:
         return jsonify({'error': f'Error encoding data: {e}'}), 400
    
    # Convert to a list in the correct order
    fertilizer_features = [list(fertilizer_df.values())]

    # Predict the fertilizer (encoded value)
    predicted_fertilizer_encoded = fertilizer_model.predict(fertilizer_features)[0]
    
    # Decode the fertilizer name
    predicted_fertilizer = target_encoder.inverse_transform([predicted_fertilizer_encoded])[0]

    return jsonify({'fertilizer_recommendation': str(predicted_fertilizer)})





import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)