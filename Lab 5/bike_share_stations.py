
"""Manage bike-share station records and rentals."""

import secrets
import sqlite3

CONNECTION = sqlite3.connect(":memory:")
CONNECTION.execute(
    "CREATE TABLE stations ("
    "id INTEGER PRIMARY KEY, name TEXT, capacity INTEGER, bikes INTEGER)"
)


def add_station(name, capacity, bikes, log=None):
    """Register a station and log its name."""
    if log is None:
        log = []

    CONNECTION.execute(
        "INSERT INTO stations (name, capacity, bikes) VALUES (?, ?, ?)",
        (name, capacity, bikes),
    )
    log.append(name)
    return log


def rent_bike(station_id):
    """Rent a bike if one is available."""
    row = CONNECTION.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()

    if row and row[0] > 0:
        CONNECTION.execute(
            "UPDATE stations SET bikes = bikes - 1 WHERE id = ?",
            (station_id,),
        )
        return True

    return False


def unlock_pin():
    """Generate a secure four-digit unlock PIN."""
    return 1000 + secrets.randbelow(9000)


def full_stations():
    """Return names of stations whose bike counts equal capacity."""
    rows = CONNECTION.execute(
        "SELECT name FROM stations WHERE bikes = capacity"
    ).fetchall()
    return [row[0] for row in rows]


def reset_station(station_id):
    """Set the station's bike count to zero."""
    CONNECTION.execute(
        "UPDATE stations SET bikes = 0 WHERE id = ?",
        (station_id,),
    )


def has_bikes(station_id):
    """Check whether a station has available bikes."""
    row = CONNECTION.execute(
        "SELECT bikes FROM stations WHERE id = ?",
        (station_id,),
    ).fetchone()
    return row is not None and row[0] is not None and row[0] > 0


def main():
    """Demonstrate station management operations."""
    add_station("Central Park", 10, 10)
    add_station("Metro Gate", 8, 2)

    print(rent_bike(2), rent_bike(9) is False)
    print(unlock_pin(), full_stations(), has_bikes(2))

    reset_station(1)


if __name__ == "__main__":
    main()
