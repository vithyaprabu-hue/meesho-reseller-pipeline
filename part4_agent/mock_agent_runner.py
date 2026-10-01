import csv
import json
import sys
import os

# Import Part 2 engine functions directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "part2_engine")))
from growth_engine import mom_growth, is_flagged, validate_feed

def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    # Subtask 1 & 2: Input Guardrail
    valid, errors = validate_feed(current_month_csv)
    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }

    # Helper to load category revenue
    def load_revenues(csv_path: str, target_month: str) -> dict:
        revs = {}
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["month"] == target_month:
                    revs[row["category"]] = float(row["revenue"])
        return revs

    # Map previous month names
    prev_month_map = {"May": "April", "June": "May"}
    prev_month_name = prev_month_map.get(month, "Previous")

    prev_data = load_revenues(previous_month_csv, prev_month_name)
    curr_data = load_revenues(current_month_csv, month)

    flagged_list = []
    escalated_categories = []

    # Subtask 3, 4, 7b: Compute MoM and classify
    for cat, curr_rev in curr_data.items():
        if cat in prev_data:
            prev_rev = prev_data[cat]
            growth = mom_growth(prev_rev, curr_rev)
            status = is_flagged(growth)

            if status == "flagged":
                flagged_list.append({
                    "category": cat,
                    "mom_pct": growth,
                    "previous_revenue": prev_rev,
                    "current_revenue": curr_rev
                })
            elif status == "escalate_exact_boundary":
                escalated_categories.append(cat)

    # Subtask 5: Sort flagged categories by abs(mom_pct) descending
    flagged_list.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)

    # Subtask 6 & 7: Top 3 drafting cap & suppression
    drafted_flagged_categories = []
    suppressed_categories = []

    for idx, item in enumerate(flagged_list):
        if idx < 3:
            # Subtask 6: Deterministic Part 3 template fill
            msg = (
                f"Context: {item['category']} performance for {month} vs. {prev_month_name}. "
                f"Insight (Fact): Revenue moved from INR {item['previous_revenue']} to INR {item['current_revenue']} "
                f"({item['mom_pct']}% MoM). "
                f"Implication (Action): Ops team to audit regional inventory and reseller allocation."
            )
            drafted_flagged_categories.append({
                "category": item["category"],
                "mom_pct": item["mom_pct"],
                "previous_revenue": item["previous_revenue"],
                "current_revenue": item["current_revenue"],
                "drafted": True,
                "message": msg
            })
        else:
            suppressed_categories.append(item["category"])

    # Subtask 8: Structured JSON schema
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_flagged_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval"
    }

if __name__ == "__main__":
    feed_path = os.path.join(os.path.dirname(__file__), "..", "part1_sql", "output", "monthly_category_revenue.csv")
    corrupted_path = os.path.join(os.path.dirname(__file__), "..", "part2_engine", "fixtures", "corrupted_feed.csv")

    print("\n--- MAY RUN ---")
    may_res = run("May", feed_path, feed_path)
    print(json.dumps(may_res, indent=2))

    print("\n--- JUNE RUN ---")
    june_res = run("June", feed_path, feed_path)
    print(json.dumps(june_res, indent=2))

    print("\n--- CORRUPTED FEED RUN ---")
    err_res = run("July", feed_path, corrupted_path)
    print(json.dumps(err_res, indent=2))