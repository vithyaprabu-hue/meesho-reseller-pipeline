import unittest
import os
from growth_engine import mom_growth, is_flagged, validate_feed

class TestGrowthEngine(unittest.TestCase):

    def test_case_1_ethnic_wear_flagged(self):
        # April to May Ethnic Wear
        pct = mom_growth(104520.77, 185107.61)
        status = is_flagged(pct)
        self.assertEqual(pct, 77.1)
        self.assertEqual(status, "flagged")

    def test_case_2_beauty_not_flagged(self):
        # May to June Beauty & Personal Care
        pct = mom_growth(35542.11, 37559.07)
        status = is_flagged(pct)
        self.assertEqual(pct, 5.67)
        self.assertEqual(status, "not_flagged")

    def test_case_3_exact_boundary(self):
        # Synthetic boundary case
        pct = mom_growth(100000.0, 108000.0)
        status = is_flagged(pct)
        self.assertEqual(pct, 8.0)
        self.assertEqual(status, "escalate_exact_boundary")

    def test_case_4_corrupted_feed(self):
        corrupted_path = os.path.join(os.path.dirname(__file__), "fixtures", "corrupted_feed.csv")
        valid, errors = validate_feed(corrupted_path)
        self.assertFalse(valid)
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[0], "line 3: negative revenue (-4200.0) for category=Western Wear")
        self.assertEqual(errors[1], "line 4: missing category (month=July)")
        self.assertEqual(errors[2], "line 6: missing revenue (category=Home & Kitchen)")

    def test_case_5_clean_feed(self):
        clean_path = os.path.join(os.path.dirname(__file__), "fixtures", "monthly_category_revenue.csv")
        valid, errors = validate_feed(clean_path)
        self.assertTrue(valid)
        self.assertEqual(errors, [])

if __name__ == "__main__":
    unittest.main()