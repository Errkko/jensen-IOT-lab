def validate_measurement(data):
    errors = []

    if not data.get("deviceId"):
        errors.append("deviceId is required")

    if "temperature" not in data:
        errors.append("temperature is required")
    elif not isinstance(data["temperature"], (int, float)):
        errors.append("temperature must be a number")

    if "humidity" in data and not isinstance(data["humidity"], (int, float)):
        errors.append("humidity must be a number")

    if "battery" in data and not isinstance(data["battery"], int):
        errors.append("battery must be an integer")

    return errors
