import os
import random
import time
import requests

API_URL = os.getenv("API_URL", "http://api:5000")

SENSORS = [
    {"deviceId": "sensor-001", "temp": (20, 23)},
    {"deviceId": "sensor-002", "temp": (18, 21)},
    {"deviceId": "sensor-003", "temp": (22, 25)},
]


def measurement(sensor):
    data = {
        "deviceId": sensor["deviceId"],
        "temperature": round(random.uniform(*sensor["temp"]), 2),
        "humidity": round(random.uniform(35, 65), 2),
        "battery": random.randint(40, 100),
    }

    # sensor-003 är medvetet opålitlig.
    if sensor["deviceId"] == "sensor-003" and random.random() < 0.15:
        if random.random() < 0.5:
            data["temperature"] = "ERROR"
        else:
            data.pop("temperature")

    return data


def wait_for_api():
    while True:
        try:
            r = requests.get(f"{API_URL}/health", timeout=2)
            if r.ok:
                return
        except requests.RequestException:
            pass
        print("Waiting for API...")
        time.sleep(2)


def main():
    wait_for_api()
    print("Simulator started with 3 sensors")

    while True:
        for sensor in SENSORS:
            data = measurement(sensor)
            try:
                response = requests.post(
                    f"{API_URL}/measurements",
                    json=data,
                    timeout=3,
                )
                marker = "OK" if response.status_code < 400 else "ERROR"
                print(
                    f"{marker} {data.get('deviceId')} "
                    f"status={response.status_code} data={data}"
                )
            except requests.RequestException as exc:
                print(f"ERROR {sensor['deviceId']} request failed: {exc}")

        time.sleep(5)


if __name__ == "__main__":
    main()
