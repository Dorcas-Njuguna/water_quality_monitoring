# clean_data.py 

import pandas as pd

def clean_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data but keep rows (we'll flag problems later):
      - trim location text
      - convert pH/turbidity/dissolved_oxygen/temperature to numeric
      - set out-of-range values to NaN so we can mark them unsafe
      - drop duplicate readings (same sensor_id + timestamp)
    """
    df = df.copy()

    if "location" in df.columns:
        df["location"] = df["location"].astype(str).str.strip()

    numeric_cols = ["ph", "turbidity", "dissolved_oxygen", "temperature"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ranges
    if "ph" in df.columns:
        df.loc[(df["ph"] < 0) | (df["ph"] > 14), "ph"] = pd.NA
    if "turbidity" in df.columns:
        df.loc[df["turbidity"] < 0, "turbidity"] = pd.NA
    if "temperature" in df.columns:
        df.loc[(df["temperature"] < -5) | (df["temperature"] > 60), "temperature"] = pd.NA

    # drop duplicate readings (keep last)
    dup_subset = [c for c in ["sensor_id", "timestamp"] if c in df.columns]
    if dup_subset:
        df = df.drop_duplicates(subset=dup_subset, keep="last")

    return df





