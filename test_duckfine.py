# test_duckfine.py
import unittest
from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def setUp(self):
        self.duck_fine = DuckFine("member_123")

    def test_initialization_sets_member_id_and_zero_total_owed(self):
        fine = DuckFine("member_456")
        self.assertEqual(fine.member_id, "member_456")
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_negative_days_late_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.duck_fine.charge(-1)

    def test_charge_within_grace_period_incurs_no_fee(self):
        # Days late <= GRACE_DAYS (2) should result in 0.0 fee[cite: 1]
        fee = self.duck_fine.charge(2)
        self.assertEqual(fee, 0.0)

    def test_charge_beyond_grace_period_calculates_standard_daily_fee(self):
        # 4 days late = 2 chargeable days * $0.50 daily fee = $1.00[cite: 1]
        fee = self.duck_fine.charge(4)
        self.assertEqual(fee, 1.00)

    def test_charge_deluxe_doubles_daily_fee(self):
        # 4 days late deluxe = 2 chargeable days * $0.50 * 2 = $2.00[cite: 1]
        fee = self.duck_fine.charge(4, deluxe=True)
        self.assertEqual(fee, 2.00)

    def test_charge_caps_standard_fee_at_maximum(self):
        # 20 days late = 18 chargeable days * $0.50 = $9.00, capped at MAX_FEE ($5.00)[cite: 1]
        fee = self.duck_fine.charge(20)
        self.assertEqual(fee, 5.00)

    def test_charge_caps_deluxe_fee_at_maximum(self):
        # 10 days late deluxe = 8 chargeable days * $0.50 * 2 = $8.00, capped at MAX_FEE ($5.00)[cite: 1]
        fee = self.duck_fine.charge(10, deluxe=True)
        self.assertEqual(fee, 5.00)

    def test_charge_accumulates_total_owed_across_multiple_charges(self):
        self.duck_fine.charge(4)  # $1.00[cite: 1]
        self.duck_fine.charge(5)  # $1.50[cite: 1]
        self.assertEqual(self.duck_fine.total_owed, 2.50)


if __name__ == "__main__":
    unittest.main()