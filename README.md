# API Prediksi Kualitas Tidur (PSQI)

API ini dibuat menggunakan Flask untuk melakukan prediksi kualitas tidur ("Baik" atau "Buruk") berdasarkan 7 komponen skor dari kuesioner PSQI. Model yang digunakan adalah Random Forest Classifier.

## ⚙️ Setup & Instalasi

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/draft-coding-id/slumbr-ai.git](https://github.com/draft-coding-id/slumbr-ai.git)
    cd REPO_ANDA
    ```

2.  **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
    ```

3.  **Install semua pustaka yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi Flask:**
    ```bash
    python app.py
    ```
    API akan berjalan di `http://127.0.0.1:5000`.

## 🚀 Cara Menggunakan API

Kirim request **POST** ke endpoint `/predict` dengan data JSON yang berisi jawaban kuesioner mentah.

**Contoh menggunakan cURL:**
```bash
curl -X POST [http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict) \
-H "Content-Type: application/json" \
-d '{
    "P1": "11:00:00 PM", "P2": 30, "P3": "05:20:00 AM", "P4": 7.0,
    "P5_1": 1, "P5_2": 1, "P5_3": 0, "P5_4": 0, "P5_5": 0, "P5_6": 0,
    "P5_7": 0, "P5_8": 0, "P5_9": 0, "P5_10": 0, "P6": 2, "P7": 1,
    "P8": 2, "P9": 1
}'
```

**Contoh Respon Sukses:**
```json
{
  "kualitas_tidur_prediksi": "Baik"
}
```