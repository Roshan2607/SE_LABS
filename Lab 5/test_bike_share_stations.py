"""
Unit tests for Lab 5: Bike Share Stations
Tests functional correctness of all CRUD and rental operations.
"""

import pytest
import bike_share_stations as bss


@pytest.fixture(autouse=True)
def clean_database():
    bss.CONNECTION.execute("DELETE FROM stations")
    bss.CONNECTION.commit()


def test_add_station():
    log = bss.add_station("Metro North", capacity=10, bikes=5)
    assert "Metro North" in log

    row = bss.CONNECTION.execute("SELECT name, capacity, bikes FROM stations WHERE name = ?", ("Metro North",)).fetchone()
    assert row == ("Metro North", 10, 5)


def test_rent_bike_success_and_empty():
    bss.add_station("City Hall", capacity=5, bikes=1)
    station_id = bss.CONNECTION.execute("SELECT id FROM stations WHERE name = 'City Hall'").fetchone()[0]

    # First rental succeeds
    assert bss.rent_bike(station_id) is True
    # Station now has 0 bikes
    assert bss.rent_bike(station_id) is False


def test_unlock_pin():
    pin = bss.unlock_pin()
    assert isinstance(pin, int)
    assert 1000 <= pin < 10000


def test_full_stations():
    bss.add_station("Station A", capacity=5, bikes=5)  # Full
    bss.add_station("Station B", capacity=10, bikes=2) # Not full
    full = bss.full_stations()
    assert "Station A" in full
    assert "Station B" not in full


def test_has_bikes_and_reset():
    bss.add_station("Park View", capacity=8, bikes=4)
    station_id = bss.CONNECTION.execute("SELECT id FROM stations WHERE name = 'Park View'").fetchone()[0]

    assert bss.has_bikes(station_id) is True
    bss.reset_station(station_id)
    assert bss.has_bikes(station_id) is False
