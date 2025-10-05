
# evaluate.py — mark each reading Safe/Unsafe with a reason

import pandas as pd

class WaterQualityEvaluator:
    def __init__(self, ph_range=(6.5, 8.5), turbidity_threshold=1.0):
        self.ph_range = ph_range
        self.turbidity_threshold = turbidity_threshold

    def is_safe(self, row: pd.Series) -> tuple[bool, str]:
        """
        Row is safe if:
          - pH is present and within [ph_range]
          - turbidity is present and <= turbidity_threshold
        Missing values = unsafe, with a reason.
        """
        reasons = []

        ph = row.get("ph")
        turb = row.get("turbidity")

        # missing checks (pd.isna handles NaN/None)
        if pd.isna(ph):
            reasons.append("missing pH")
        if pd.isna(turb):
            reasons.append("missing turbidity")

        # range checks only if present
        if not reasons:
            lo, hi = self.ph_range
            if ph < lo:
                reasons.append("pH too low")
            elif ph > hi:
                reasons.append("pH too high")
            if turb > self.turbidity_threshold:
                reasons.append("turbidity too high")

        ok = len(reasons) == 0
        message = "Safe" if ok else "Unsafe (" + ", ".join(reasons) + ")"
        return ok, message
