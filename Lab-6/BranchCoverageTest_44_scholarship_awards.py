import pytest
from scholarship_awards import award_amount, is_eligible, application_status

# ---------------------------------------------------------------------------
# BranchCoverageTest - targets >= 90% BRANCH coverage
# Every if/else branch is exercised in both directions.
# ---------------------------------------------------------------------------

# === award_amount ===========================================================
# Branches:
#  B1: category not in CUTOFF_MARKS  → True / False
#  B2: marks < 0                     → True / False
#  B3: is_renewal and category != "sports" → True / False (all combos)
#  B4: above <= 0                    → True / False
#  B5: income_level == "low"         → True / False
#  B6: above > 15                    → True / False
#  B7: income_level == "low" (inner) → True / False

def test_b1_true_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("dance", 80, "low", False)

def test_b2_true_negative_marks():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)

def test_b2_false_valid_marks():
    """marks >= 0 → no error on that branch."""
    award_amount("merit", 0, "low", False)  # no exception

# B3: is_renewal=True AND category != "sports" → cutoff reduced
def test_b3_true_renewal_not_sports():
    # merit cutoff 75→70, marks=72, above=2, rate=100, award=200
    assert award_amount("merit", 72, "low", True) == 200

# B3: is_renewal=True BUT category == "sports" → cutoff NOT reduced
def test_b3_false_renewal_is_sports():
    # sports cutoff stays 60, marks=62, above=2, rate=100, award=200
    assert award_amount("sports", 62, "low", True) == 200

# B3: is_renewal=False → cutoff NOT reduced
def test_b3_false_not_renewal():
    # merit cutoff stays 75, marks=78, above=3, rate=60, award=180
    assert award_amount("merit", 78, "high", False) == 180

# B4: above <= 0 → return 0
def test_b4_true_at_or_below_cutoff():
    assert award_amount("merit", 75, "low", False) == 0
    assert award_amount("merit", 60, "low", False) == 0

# B4: above > 0 → continue
def test_b4_false_above_cutoff():
    assert award_amount("merit", 80, "low", False) == 500

# B5: income_level == "low" → rate = 100
def test_b5_true_low_income():
    # above=5, rate=100, award=500
    assert award_amount("merit", 80, "low", False) == 500

# B5: income_level != "low" → rate = 60
def test_b5_false_high_income():
    # above=5, rate=60, award=300
    assert award_amount("merit", 80, "high", False) == 300

# B6: above > 15 → rate += 40
def test_b6_true_above_15_high_income():
    # merit, above=20, rate=60+40=100, award=2000
    assert award_amount("merit", 95, "high", False) == 2000

# B6: above <= 15 → no bonus
def test_b6_false_at_15_low_income():
    # merit, above=15, rate=100, award=1500
    assert award_amount("merit", 90, "low", False) == 1500

# B7: inner low income bonus (above>15 AND low)
def test_b7_true_above15_low_income_double_bonus():
    # above=20, rate=100+40+20=160, award=3200
    assert award_amount("merit", 95, "low", False) == 3200

# B7: inner low income bonus FALSE (above>15 AND NOT low)
def test_b7_false_above15_high_income_single_bonus():
    # above=20, rate=60+40=100, award=2000
    assert award_amount("merit", 95, "high", False) == 2000

# Arts + renewal branch
def test_arts_renewal_lowers_cutoff():
    # arts cutoff 65→60, marks=63, above=3, rate=100, award=300
    assert award_amount("arts", 63, "low", True) == 300

# Sports with above > 15
def test_sports_above_15_high():
    # sports cutoff=60, marks=80, above=20, rate=60+40=100, award=2000
    assert award_amount("sports", 80, "high", False) == 2000


# === is_eligible ===========================================================
# Branches:
#  B1: is_special_quota → True / False
#  B2 (special): backlogs <= 2 → True / False
#  B3 (normal): attendance < 75 → True / False
#  B4 (normal): backlogs <= 1 → True / False

def test_special_quota_backlogs_ok():
    assert is_eligible(40, 2, True) is True

def test_special_quota_backlogs_too_many():
    assert is_eligible(40, 3, True) is False

def test_normal_low_attendance():
    assert is_eligible(74, 0, False) is False

def test_normal_good_attendance_backlogs_ok():
    assert is_eligible(80, 1, False) is True

def test_normal_good_attendance_backlogs_fail():
    assert is_eligible(80, 2, False) is False


# === application_status ====================================================
# Branches:
#  B1: is_renewal → True / False
#  B2: is_paper   → True / False
#  B3: days_left >= cutoff → True / False
#  B4: days_left >= cutoff-15 → True / False  (the elif)

# B1=False, B2=False → cutoff=20
def test_new_nonpaper_open():
    assert application_status(20, False, False) == "open"

def test_new_nonpaper_closing():
    # cutoff=20, closing range [5,19]
    assert application_status(7, False, False) == "closing"

def test_new_nonpaper_closed():
    # cutoff=20, days_left=4 < 5 → closed
    assert application_status(4, False, False) == "closed"

# B1=True, B2=False → cutoff=30
def test_renewal_nonpaper_open():
    assert application_status(30, True, False) == "open"

def test_renewal_nonpaper_closing():
    # closing range [15, 29]
    assert application_status(20, True, False) == "closing"

def test_renewal_nonpaper_closed():
    # days_left < 15 → closed
    assert application_status(10, True, False) == "closed"

# B1=False, B2=True → cutoff=30
def test_new_paper_open():
    assert application_status(30, False, True) == "open"

def test_new_paper_closing():
    # closing range [15,29]
    assert application_status(20, False, True) == "closing"

def test_new_paper_closed():
    assert application_status(5, False, True) == "closed"

# B1=True, B2=True → cutoff=40
def test_renewal_paper_open():
    assert application_status(40, True, True) == "open"

def test_renewal_paper_closing():
    # closing range [25,39]
    assert application_status(30, True, True) == "closing"

def test_renewal_paper_closed():
    assert application_status(10, True, True) == "closed"

