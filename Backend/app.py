from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import joblib
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model
MODEL_PATH = 'botnet_detector_xgboost.model'
model = joblib.load(MODEL_PATH)

# Expected features
EXPECTED_FEATURES = [
    'Unnamed: 0', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts', 'TotLen Fwd Pkts',
    'TotLen Bwd Pkts', 'Fwd Pkt Len Max', 'Fwd Pkt Len Min', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Std',
    'Bwd Pkt Len Max', 'Bwd Pkt Len Min', 'Bwd Pkt Len Mean', 'Bwd Pkt Len Std',
    'Flow Byts/s', 'Flow Pkts/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
    'Fwd IAT Tot', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
    'Bwd IAT Tot', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min',
    'Bwd PSH Flags', 'Fwd Header Len', 'Bwd Header Len', 'Fwd Pkts/s', 'Bwd Pkts/s',
    'Pkt Len Min', 'Pkt Len Max', 'Pkt Len Mean', 'Pkt Len Std', 'Pkt Len Var',
    'FIN Flag Cnt', 'SYN Flag Cnt', 'RST Flag Cnt', 'ACK Flag Cnt', 'Down/Up Ratio',
    'Pkt Size Avg', 'Fwd Seg Size Avg', 'Bwd Seg Size Avg', 'Init Bwd Win Byts',
    'Fwd Act Data Pkts', 'Active Mean', 'Active Std', 'Active Max', 'Active Min',
    'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min'
]

# Threshold logic
NETWORK_THRESHOLDS = {
    'home': 5,
    'soho': 8,
    'enterprise': 12
}

@app.route('/')
def home():
    return '<h2>Welcome to TrafficTracer Backend API! 📦🔍</h2>', 200

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    network_type = request.form.get('networkType', 'home')
    threshold = NETWORK_THRESHOLDS.get(network_type, 5)

    df = pd.read_csv(file)
    df['Unnamed: 0'] = df.index
    df = df[EXPECTED_FEATURES]
    df = df.replace([float('inf'), -float('inf')], 0).fillna(0)

    predictions = model.predict(df)
    botnet_count = (predictions == 1).sum()
    normal_count = (predictions == 0).sum()
    total = len(predictions)

    botnet_ratio = (botnet_count / total) * 100 if total else 0

    verdict = 'Safe ✅' if botnet_ratio < threshold else '⚠️ Potential Threat Detected!'

    return jsonify({
        'total_flows': total,
        'botnet_count': int(botnet_count),
        'normal_count': int(normal_count),
        'botnet_ratio': round(botnet_ratio, 2),
        'threshold': threshold,
        'verdict': verdict,
        'predictions': predictions.tolist()
    })

# Serve CICFlowMeter download (simulate)
@app.route('/download-cicflowmeter')
def download_cicflowmeter():
    return send_from_directory(directory='static', path='CICFlowMeter.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
