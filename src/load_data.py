import pandas as pd

def load_csv(filepath: str) -> pd.DataFrame:
    """
    Load sensor data from a CSV file into a pandas DataFrame.
    - Lower-case and underscore column names
    - Parse 'timestamp' to datetime if present
    """
    df = pd.read_csv(filepath)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df

