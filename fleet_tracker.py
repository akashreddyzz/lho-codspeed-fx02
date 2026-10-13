import math
from datetime import datetime


def parse_log(lines):
    """Parse 'vehicle,ISO_time,lat,lon' lines into dicts sorted by vehicle, time."""
    points = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        vehicle, ts, lat, lon = line.split(",")
        points.append({
            "vehicle": vehicle,
            "time": datetime.fromisoformat(ts),
            "lat": float(lat),
            "lon": float(lon),
        })
    points.sort(key=lambda p: (p["vehicle"], p["time"]))
    return points


def _haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def track_distance(points):
    """Total distance in km per vehicle."""
    totals, last = {}, {}
    for p in points:
        v = p["vehicle"]
        if v in last:
            q = last[v]
            totals[v] = totals.get(v, 0.0) + _haversine_km(
                q["lat"], q["lon"], p["lat"], p["lon"]
            )
        else:
            totals[v] = 0.0
        last[v] = p
    return totals


def speed_alerts(points, limit_kmh=80.0):
    """Return segments where speed exceeded the limit."""
    alerts, last = [], {}
    for p in points:
        v = p["vehicle"]
        if v in last:
            q = last[v]
            hours = (p["time"] - q["time"]).total_seconds() / 3600
            if hours > 0:
                speed = _haversine_km(q["lat"], q["lon"], p["lat"], p["lon"]) / hours
                if speed > limit_kmh:
                    alerts.append(
                        {"vehicle": v, "time": p["time"], "speed_kmh": round(speed, 1)}
                    )
        last[v] = p
    return alerts
