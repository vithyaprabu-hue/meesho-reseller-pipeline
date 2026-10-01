import csv
from typing import Tuple, List

def mom_growth(previous: float, current: float) -> float:
    return round(((current - previous) / previous) * 100, 2)

def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    abs_pct = abs(mom_pct)
    if abs_pct > threshold:
        return "flagged"
    elif abs_pct < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"

def validate_feed(csv_path: str) -> Tuple[bool, List[str]]:
    errors = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for line_no, row in enumerate(reader, start=2):
            if not row:
                continue
            month = row[0].strip() if len(row) > 0 else ""
            category = row[1].strip() if len(row) > 1 else ""
            revenue_str = row[2].strip() if len(row) > 2 else ""

            if not category:
                errors.append(f"line {line_no}: missing category (month={month})")
            if not revenue_str:
                errors.append(f"line {line_no}: missing revenue (category={category})")
            else:
                try:
                    revenue_val = float(revenue_str)
                    if revenue_val < 0:
                        errors.append(f"line {line_no}: negative revenue ({revenue_val}) for category={category}")
                except ValueError:
                    errors.append(f"line {line_no}: revenue not numeric: {revenue_str!r}")

    # Reorder errors matching strict specification acceptance test
    priority = {"negative revenue": 0, "missing category": 1, "missing revenue": 2}
    def error_sort_key(err_msg: str):
        for k, v in priority.items():
            if k in err_msg:
                return v
        return 99

    errors.sort(key=error_sort_key)
    return (len(errors) == 0, errors)