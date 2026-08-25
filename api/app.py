from flask import Flask, jsonify, request, render_template
import os
import socket

from db import (
    device_exists,
    get_devices,
    get_measurements,
    get_latest_measurement,
    get_measurements_for_device,
    insert_measurement,
    get_statistics,
)
from validation import validate_measurement
from cache import get_latest_from_cache, set_latest_in_cache

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "v1")
POD_NAME = socket.gethostname()


@app.get("/")
def dashboard():
    return render_template("index.html", version=APP_VERSION, pod=POD_NAME)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "version": APP_VERSION,
        "pod": POD_NAME,
    }), 200


@app.get("/devices")
def devices():
    return jsonify(get_devices()), 200


@app.get("/measurements")
def measurements():
    return jsonify(get_measurements()), 200


@app.get("/devices/<device_id>/latest")
def latest(device_id):
    # TODO M1: CHECK
    # Läs senaste mätningen från PostgreSQL med get_latest_measurement(...).
    # Returnera 404 om sensorn eller en mätning saknas.

    measurement = get_latest_from_cache(device_id)

    if not measurement:
        measurement = get_latest_measurement(device_id)
        if not measurement:
            return jsonify({"error": "Device or measurement not found"}), 404
        
        set_latest_in_cache(device_id, measurement)

    return jsonify(measurement), 200

    # TODO M2:
    # Utöka M1-lösningen med cache-aside:
    # 1. Försök läsa från Redis.
    # 2. Vid cache miss: läs från PostgreSQL.
    # 3. Spara databasresultatet i Redis.


@app.get("/devices/<device_id>/measurements")
def device_history(device_id):
    # TODO M1: CHECK
    # Hämta sensorhistorik från PostgreSQL.
    # Känd sensor utan mätningar: 200 och []. Okänd sensor: 404.
    if not device_exists(device_id):
        return jsonify({"error": "Unknown sensor"}), 404
    return jsonify(get_measurements_for_device(device_id)), 200


@app.post("/measurements")
def create_measurement():
    data = request.get_json(silent=True) or {}
    errors = validate_measurement(data)

    if errors:
        print(f"INVALID measurement from {data.get('deviceId', 'unknown')}: {errors}")
        return jsonify({"errors": errors}), 400

    # TODO M1: CHECK
    # Kontrollera med device_exists(...) att deviceId tillhör en känd sensor.
    # Okänd sensor ska ge 400 med ett tydligt JSON-fel.
    # Spara till PostgreSQL via insert_measurement(data).
    device_id = data.get("deviceId")
    data["device_id"] = device_id

    if not device_exists(data.get("deviceId")):
        return jsonify({"error": "Device not found"}), 400
        
    measurement = insert_measurement(data)

    # TODO M2:CHECK        
    # Uppdatera latest-cache för sensorn
    set_latest_in_cache(device_id, measurement)
    return jsonify(measurement), 201


@app.get("/statistics")
def statistics():
    # ⭐ Utmaning: CHECK
    # Returnera antal devices, antal measurements, avg temp etc.
    return jsonify(get_statistics()), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
