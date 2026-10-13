import pytest
from fleet_tracker import parse_log, track_distance, speed_alerts

LOG = [
    "# vehicle,time,lat,lon",
    "truck1,2026-01-01T10:00:00,0.0,0.0",
    "truck1,2026-01-01T11:00:00,1.0,0.0",
    "truck2,2026-01-01T10:00:00,0.0,0.0",
    "truck2,2026-01-01T12:00:00,0.5,0.0",
]


def test_parse_log_skips_comments_and_sorts():
    points = parse_log(LOG)
    assert len(points) == 4
    assert points[0]["vehicle"] == "truck1"


def test_track_distance_one_degree_latitude():
    totals = track_distance(parse_log(LOG))
    assert totals["truck1"] == pytest.approx(111.19, abs=0.1)


def test_speed_alerts_flags_only_fast_segment():
    alerts = speed_alerts(parse_log(LOG), limit_kmh=80)
    assert len(alerts) == 1
    assert alerts[0]["vehicle"] == "truck1"
