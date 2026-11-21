import math
from hypothesis import given, strategies as st
from scholarship_awards import parse_applicant, marks_average, payable_award


@given(st.text() | st.none())
def test_parse_applicant_no_crash(s):
    try:
        result = parse_applicant(s)
    except Exception as e:
        assert False, f"parse_applicant crashed with: {e}"
    if result is not None:
        category, marks = result
        assert isinstance(category, str) and category
        assert 0 <= marks <= 100


@given(st.text() | st.none())
def test_marks_average_no_crash(s):
    try:
        result = marks_average(s)
    except Exception as e:
        assert False, f"marks_average crashed with: {e}"
    if result is not None:
        assert 0 <= result <= 100


@given(st.text() | st.none())
def test_payable_award_no_crash(s):
    try:
        result = payable_award(s)
    except Exception as e:
        assert False, f"payable_award crashed with: {e}"
    if result is not None:
        assert math.isfinite(result) and result >= 0


# Extra property tests with structured inputs
@given(st.lists(st.integers(0, 100), min_size=1))
def test_marks_average_valid(marks):
    result = marks_average(",".join(map(str, marks)))
    assert min(marks) <= result <= max(marks)


@given(st.floats(0, 1e6), st.floats(0, 1e6))
def test_payable_award_valid(award, deduction):
    result = payable_award(f"{award}|{deduction}")
    assert result is not None and result >= 0
