from collections import deque
import statistics

window_size = 5
threshold = 100
sensor_windows = {}

def cal_stats(sensor_id, temperature):
    if sensor_id not in sensor_windows:
        sensor_windows[sensor_id] = deque(maxlen=window_size)

    temp_window = sensor_windows[sensor_id]
    temp_window.append(temperature)

    if len(temp_window) < window_size:
        return {
            "mean": None,
            "z_score": None,
            "status": "INITIALIZING",
            "temp": temperature
        }

    mean = statistics.mean(temp_window)
    std = statistics.stdev(temp_window) if len(temp_window) > 1 else 0
    z = (temperature - mean) / std if std != 0 else 0

    if temperature >= threshold or abs(z) > 3:
        status = "CRITICAL"
    elif abs(z) > 2:
        status = "WARNING"
    else:
        status = "NORMAL"

    return {
        "mean": round(mean, 2),
        "z_score": round(z, 2),
        "status": status,
        "temp": temperature
    }