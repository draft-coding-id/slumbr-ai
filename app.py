import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# 1. Inisialisasi Aplikasi Flask
app = Flask(__name__)
CORS(app)

# 2. Muat Model Machine Learning
try:
    model = joblib.load('random_forest_psqi_model_terbaik.pkl')
except Exception as e:
    print(f"Error saat memuat model: {e}")
    model = None

def calculate_comp2(row):
    p2_score = 0
    if row['P2'] > 60:
        p2_score = 3
    elif row['P2'] > 30:
        p2_score = 2
    elif row['P2'] >= 16:
        p2_score = 1
    
    p5_1_score = row['P5_1']
    total_score = p2_score + p5_1_score
    
    if total_score == 0:
        return 0
    elif total_score <= 2:
        return 1
    elif total_score <= 4:
        return 2
    else:
        return 3

def calculate_comp3(p4_hours):
    if p4_hours > 7:
        return 0
    elif p4_hours >= 6:
        return 1
    elif p4_hours >= 5:
        return 2
    else:
        return 3

def calculate_comp4(row):
    try:
        bed_time = pd.to_datetime(row['P1'], format='%H:%M:%S', errors='coerce')
        wake_time = pd.to_datetime(row['P3'], format='%H:%M:%S', errors='coerce')

        if pd.isna(bed_time) or pd.isna(wake_time):
            return 3 

        if wake_time < bed_time:
            wake_time += pd.Timedelta(days=1)
            
        time_in_bed_hours = (wake_time - bed_time).total_seconds() / 3600
        sleep_hours = row['P4']
        
        if time_in_bed_hours == 0:
            return 3
            
        efficiency = (sleep_hours / time_in_bed_hours) * 100
        
        if efficiency >= 85:
            return 0
        elif efficiency >= 75:
            return 1
        elif efficiency >= 65:
            return 2
        else:
            return 3
    except Exception:
        return 3

def calculate_comp5(row):
    disturbance_sum = sum([row.get(f'P5_{i}', 0) for i in range(2, 11)])
    
    if disturbance_sum == 0:
        return 0
    elif disturbance_sum <= 9:
        return 1
    elif disturbance_sum <= 18:
        return 2
    else:
        return 3

def calculate_comp7(row):
    dysfunction_sum = row.get('P8', 0) + row.get('P9', 0)
    
    if dysfunction_sum == 0:
        return 0
    elif dysfunction_sum <= 2:
        return 1
    elif dysfunction_sum <= 4:
        return 2
    else:
        return 3

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model tidak dapat dimuat.'}), 500

    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])
        
        input_df['C1_Subj_Sleep_Quality'] = input_df['P6']
        input_df['C2_Sleep_Latency'] = input_df.apply(calculate_comp2, axis=1)
        input_df['C3_Sleep_Duration'] = input_df['P4'].apply(calculate_comp3)
        input_df['C4_Sleep_Efficiency'] = input_df.apply(calculate_comp4, axis=1)
        input_df['C5_Sleep_Disturbance'] = input_df.apply(calculate_comp5, axis=1)
        input_df['C6_Meds_Use'] = input_df['P7']
        input_df['C7_Day_Dysfunction'] = input_df.apply(calculate_comp7, axis=1)

        features_for_model = [
            'C1_Subj_Sleep_Quality', 'C2_Sleep_Latency', 'C3_Sleep_Duration',
            'C4_Sleep_Efficiency', 'C5_Sleep_Disturbance', 'C6_Meds_Use', 'C7_Day_Dysfunction'
        ]
        
        model_input = input_df[features_for_model]
        prediction = model.predict(model_input)

        scores = {
            'C1': int(input_df['C1_Subj_Sleep_Quality'].iloc[0]),
            'C2': int(input_df['C2_Sleep_Latency'].iloc[0]),
            'C3': int(input_df['C3_Sleep_Duration'].iloc[0]),
            'C4': int(input_df['C4_Sleep_Efficiency'].iloc[0]),
            'C5': int(input_df['C5_Sleep_Disturbance'].iloc[0]),
            'C6': int(input_df['C6_Meds_Use'].iloc[0]),
            'C7': int(input_df['C7_Day_Dysfunction'].iloc[0])
        }

        # Cari komponen dengan skor tertinggi
        highest_c = max(scores, key=scores.get)

        # Gabungkan semua data untuk respons akhir
        response_data = {
            'kualitas_tidur_prediksi': prediction[0],
            'komponen_tertinggi': highest_c,
            'scores': scores
        }
        
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Jalankan Aplikasi
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)