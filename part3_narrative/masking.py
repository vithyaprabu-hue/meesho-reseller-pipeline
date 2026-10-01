from typing import List

def alias_for(reseller_id: str) -> str:
    # Converts e.g. RS019 -> ALIAS-19, RS006 -> ALIAS-06
    return f"ALIAS-{reseller_id[3:]}"

def assert_no_raw_names_leak(text: str, reseller_names: List[str]) -> bool:
    for name in reseller_names:
        if name and name in text:
            return False
    return True

if __name__ == "__main__":
    test_alias = alias_for("RS019")
    assert test_alias == "ALIAS-19", f"Expected ALIAS-19 but got {test_alias}"

    raw_names = ["Mumbai Reseller 1", "Jaipur Reseller 5"]
    clean_text = "Top seller ALIAS-19 in West generated strong volume."
    leaky_text = "Top seller Mumbai Reseller 1 in West generated strong volume."

    assert assert_no_raw_names_leak(clean_text, raw_names) is True
    assert assert_no_raw_names_leak(leaky_text, raw_names) is False
    print("Masking validations passed successfully!")