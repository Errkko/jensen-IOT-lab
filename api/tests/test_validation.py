from validation import validate_measurement


def test_valid_measurement():
    data = {
        "deviceId": "sensor-001",
        "temperature": 21.5,
        "humidity": 45.0,
        "battery": 90,
    }
    assert validate_measurement(data) == []


def test_missing_temperature():
    data = {
        "deviceId": "sensor-001",
        "humidity": 45.0,
        "battery": 90,
    }
    assert "temperature is required" in validate_measurement(data)


def test_invalid_temperature_type():
    data = {
        "deviceId": "sensor-003",
        "temperature": "ERROR",
    }
    assert "temperature must be a number" in validate_measurement(data)
