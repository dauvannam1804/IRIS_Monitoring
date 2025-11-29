import requests
import time
import random
import logging
from datetime import datetime

URL = "http://localhost:8000/predict"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("Simulator")

def generate_normal_iris():
    """Sinh dữ liệu Iris chuẩn, phân phối đều"""
    return {
        "features": [
            round(random.uniform(4.3, 7.9), 1), # sepal_length
            round(random.uniform(2.0, 4.4), 1), # sepal_width
            round(random.uniform(1.0, 6.9), 1), # petal_length
            round(random.uniform(0.1, 2.5), 1) # petal_width
        ]
    }

def generate_drift_iris():
    return {
        "features": [
            round(random.uniform(8.0, 10.0), 1), # Rất to
            round(random.uniform(4.5, 6.0), 1),
            round(random.uniform(7.0, 9.0), 1), # Rất dài
            round(random.uniform(3.0, 5.0), 1)
        ]
    }

def generate_error_payload():
    error_types = [
        {"features": [1, 2]}, # Thiếu features
        {"features": ["a", "b", "c", "d"]}, # Sai data type (str thay vì float)
        {"wrong_key": [1, 2, 3, 4]}, # Sai key
        {} # Empty
    ]
    return random.choice(error_types)

def run_scenario(name, duration_sec, delay_range, data_func):
    logger.info(f"--- BẮT ĐẦU SCENARIO: {name} ({duration_sec}s) ---")
    end_time = time.time() + duration_sec

    while time.time() < end_time:
        try:
            payload = data_func()
            response = requests.post(URL, json=payload, timeout=5)
            if response.status_code == 200:
                # Chỉ in dấu chấm để đỡ spam màn hình khi chạy nhanh, hoặc in chi tiết nếu cần
                pred = response.json().get('prediction')
                print(f" {name} | Pred: {pred} | Input: {payload['features']}", end="\r")
            else:
                print(f"\n {name} | Status: {response.status_code} | Error: {response.text}")

        except Exception as e:
            print(f"\n Connection Error: {e}")

        time.sleep(random.uniform(*delay_range))
    print("\n")

if __name__ == "__main__":
    print(f"Starting ADVANCED traffic generation to {URL}...")
    print("Cycle: Normal -> High Load -> Data Drift -> Errors -> Normal...")

    try:
        while True:
            run_scenario(
                name="NORMAL MODE",
                duration_sec=30,
                delay_range=(0.5, 1.5),
                data_func=generate_normal_iris
            )
            run_scenario(
                name="HIGH LOAD SPIKE",
                duration_sec=15,
                delay_range=(0.01, 0.05),
                data_func=generate_normal_iris
            )
            run_scenario(
                name="DATA DRIFT",
                duration_sec=20,
                delay_range=(0.3, 0.8),
                data_func=generate_drift_iris
            )
            run_scenario(
                name="ERROR STORM",
                duration_sec=10,
                delay_range=(0.2, 0.6),
                data_func=generate_error_payload
            )

    except KeyboardInterrupt:
        print("\n Stopped by user.")
