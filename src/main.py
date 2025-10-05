# main.py — run the water quality pipeline using sensor_id (dataset has no location)

from load_data import load_csv
from clean_data import clean_sensor_data
from evaluate import WaterQualityEvaluator
from sensor import SensorReading

def display_sensor_id(raw):
    """Make IDs like 'SENSOR_005' print as 5. If no digits, return the original."""
    s = str(raw)
    digits = "".join(ch for ch in s if ch.isdigit())
    return int(digits) if digits else s

def main():
    # 1) load
    df = load_csv("../data/sensor_data.csv")

    # 2) clean
    df = clean_sensor_data(df)

    # Ensure sensor_id is present and printable
    if "sensor_id" not in df.columns:
        raise ValueError("CSV must contain 'sensor_id' when there is no 'location' column.")
    df["sensor_id"] = df["sensor_id"].astype(str).str.strip()

    # 2b) user input: filter by sensor_id (press Enter for all)
    print("Enter a sensor_id to filter (e.g., SENSOR_005).")
    print("Press Enter to use ALL sensors.")
    user_sensor = input("sensor_id: ").strip()
    if user_sensor:
        df = df[df["sensor_id"] == user_sensor]
        if df.empty:
            print(f"No rows found for sensor_id: {user_sensor}")
            return

    # 3) evaluate each row and build SensorReading objects
    evaluator = WaterQualityEvaluator(ph_range=(6.5, 8.5), turbidity_threshold=1.0)

    is_safe_list = []
    status_text_list = []
    sample_readings = []

    for i, (_, row) in enumerate(df.iterrows(), start=1):
        # class usage
        reading = SensorReading.from_row(row)
        if i <= 2:
            sample_readings.append(reading)

        # evaluator is_safe might return (ok, text) or just ok
        result = evaluator.is_safe(row)
        if isinstance(result, tuple):
            ok, text = result
        else:
            ok = bool(result)
            text = "Safe" if ok else "Unsafe"

        is_safe_list.append(ok)
        status_text_list.append(text)

    df["is_safe"] = is_safe_list
    df["status_text"] = status_text_list

    # 4) use the class
    if sample_readings:
        print("\n(example SensorReading objects)")
        for r in sample_readings:
            print(" ", r)

    # 5) report
    print("\n=== Water Quality Report (first 10 rows) ===")
    for _, r in df.head(10).iterrows():
        sid_num = display_sensor_id(r.get("sensor_id", ""))
        ok = bool(r.get("is_safe", False))
        text = r.get("status_text", "Safe" if ok else "Unsafe")
        pretty = "Safe" if ok else (text if text.startswith(" X ") else f" X {text}")
        print(f"Sensor {sid_num}: {pretty}")

    # 6) row-level counts
    total = len(df)
    safe_count = int(df["is_safe"].sum())
    unsafe_count = total - safe_count
    print(f"\nSummary: {safe_count} safe, {unsafe_count} unsafe (out of {total})")

    # 7) save results
    out_path = "../data/results.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved detailed results to {out_path}")

if __name__ == "__main__":
    main()


