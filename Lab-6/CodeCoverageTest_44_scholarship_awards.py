import pytest
from scholarship_awards import award_amount, is_eligible, application_status

# ---------------------------------------------------------------------------
# CodeCoverageTest - targets >= 90% LINE coverage
# ---------------------------------------------------------------------------

# --- award_amount -----------------------------------------------------------

def test_below_cutoff_marks():
    """Marks below cutoff → 0 award."""
    assert award_amount("merit", 70, "low", False) == 0

def test_unknown_category_raises():
    """Unknown category raises ValueError."""
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("dance", 80, "low", False)

def test_negative_marks_raises():
    """Negative marks raises ValueError."""
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -5, "low", False)

def test_above_cutoff_low_income():
    """Marks above cutoff, low income, below bonus threshold."""
    # merit cutoff = 75, above = 85-75 = 10, rate = 100, award = 10*100 = 1000
    assert award_amount("merit", 85, "low", False) == 1000

def test_above_cutoff_high_income():
    """Marks above cutoff, non-low income, below bonus threshold."""
    # above = 10, rate = 60, award = 10*60 = 600
    assert award_amount("merit", 85, "high", False) == 600

def test_above_15_low_income_bonus():
    """above > 15 with low income triggers both bonuses."""
    # merit cutoff=75, above=20, rate=100+40+20=160, award=20*160=3200
    assert award_amount("merit", 95, "low", False) == 3200

def test_above_15_high_income_bonus():
    """above > 15 with non-low income triggers one bonus."""
    # above=20, rate=60+40=100, award=20*100=2000
    assert award_amount("merit", 95, "high", False) == 2000

def test_renewal_merit_lowers_cutoff():
    """Renewal for non-sports category lowers cutoff by 5."""
    # merit cutoff=75-5=70, marks=73, above=3, rate=100, award=300
    assert award_amount("merit", 73, "low", True) == 300

def test_renewal_sports_cutoff_unchanged():
    """Renewal for sports does NOT lower cutoff."""
    # sports cutoff stays at 60, marks=58 → above=-2 → 0
    assert award_amount("sports", 58, "low", True) == 0

def test_sports_category():
    """Sports category uses cutoff 60."""
    # above=65-60=5, rate=100, award=500
    assert award_amount("sports", 65, "low", False) == 500

def test_arts_category():
    """Arts category uses cutoff 65."""
    # above=70-65=5, rate=60, award=300
    assert award_amount("arts", 70, "high", False) == 300

def test_exactly_at_cutoff():
    """Marks exactly at cutoff → above=0 → award=0."""
    assert award_amount("merit", 75, "low", False) == 0


# --- is_eligible -----------------------------------------------------------

def test_is_eligible_normal_pass():
    """Good attendance, 1 backlog → eligible."""
    assert is_eligible(90, 1, False) is True

def test_is_eligible_low_attendance():
    """Attendance < 75 → not eligible (normal quota)."""
    assert is_eligible(70, 0, False) is False

def test_is_eligible_too_many_backlogs():
    """2 backlogs, normal quota → not eligible."""
    assert is_eligible(80, 2, False) is False

def test_is_eligible_special_quota_pass():
    """Special quota: up to 2 backlogs is OK."""
    assert is_eligible(50, 2, True) is True

def test_is_eligible_special_quota_fail():
    """Special quota: 3 backlogs → not eligible."""
    assert is_eligible(50, 3, True) is False


# --- application_status ----------------------------------------------------

def test_status_open_new_non_paper():
    """New application, non-paper, days_left >= 20 → open."""
    assert application_status(25, False, False) == "open"

def test_status_closing_new_non_paper():
    """New application, non-paper, days_left in [5,19] → closing."""
    assert application_status(10, False, False) == "closing"

def test_status_closed_new_non_paper():
    """New application, non-paper, days_left < 5 → closed."""
    assert application_status(2, False, False) == "closed"

def test_status_open_renewal():
    """Renewal application, days_left >= 30 → open."""
    assert application_status(35, True, False) == "open"

def test_status_open_paper():
    """Non-paper deadline +10 days: days_left=30 → open (cutoff=30)."""
    assert application_status(30, False, True) == "open"

def test_status_renewal_paper():
    """Renewal + paper: cutoff = 30+10 = 40, days_left=45 → open."""
    assert application_status(45, True, True) == "open"

