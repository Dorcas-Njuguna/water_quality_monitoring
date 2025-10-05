# sensor.py — a tiny class to model one sensor reading

from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class SensorReading:
    sensor_id: Optional[str]
    location: str
    ph: Optional[float]
    turbidity: Optional[float]
    temperature: Optional[float] = None

    @classmethod
    def from_row(cls, row) -> "SensorReading":
        """Build a SensorReading from a pandas row (Series)."""
        def val(col):
            return row[col] if col in row else None

        def num(col):
            v = val(col)
            # Treat NaN as None (NaN != NaN)
            return None if v is None or v != v else float(v)

        # sensor IDs keeps as str
        sensor = val("sensor_id")
        sensor = str(sensor) if sensor is not None and sensor == sensor else None

        return cls(
            sensor_id=sensor,
            location=str(val("location") or ""),
            ph=num("ph"),
            turbidity=num("turbidity"),
            temperature=num("temperature"),
        )

    def to_dict(self) -> dict:
        """Plain dict (handy for JSON/CSV or debugging)."""
        return asdict(self)
