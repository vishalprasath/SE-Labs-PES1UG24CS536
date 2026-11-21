import math

GST_RATE = 1.18


def _to_finite_float(value):
    """Convert a string to a finite float, or return None if not possible."""
    try:
        number = float(value)
    except (ValueError, TypeError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def parse_applicant(text):
    """Parse 'category:marks' -> (Category, marks). Returns None on invalid input."""
    if not isinstance(text, str) or text.count(':') != 1:
        return None
    category, marks = text.split(':')
    category = category.strip()
    marks = _to_finite_float(marks)
    if not category or marks is None or not (0 <= marks <= 100):
        return None
    return category.title(), marks


def marks_average(marks_csv):
    """Average of comma-separated integer marks (0-100). Returns None on invalid input."""
    if not isinstance(marks_csv, str) or not marks_csv.strip():
        return None
    values = []
    for item in marks_csv.split(','):
        try:
            mark = int(item.strip())
        except (ValueError, TypeError):
            return None
        if not (0 <= mark <= 100):
            return None
        values.append(mark)
    return sum(values) / len(values)


def payable_award(text):
    """Parse 'award|deduction' -> award*1.18 - deduction, never below 0. None on invalid input."""
    if not isinstance(text, str) or text.count('|') != 1:
        return None
    award, deduction = text.split('|')
    award = _to_finite_float(award)
    deduction = _to_finite_float(deduction)
    if award is None or deduction is None or award < 0 or deduction < 0:
        return None
    total = award * GST_RATE - deduction
    if not math.isfinite(total):
        return None
    return max(total, 0)


def main():
    print("==== Running parse_applicant ====")
    user_input = input("Enter category:marks (e.g. merit:82): ")
    result = parse_applicant(user_input)
    print("Category and Marks:", result if result is not None else "Invalid input")

    print("\n==== Running marks_average ====")
    user_input = input("Enter marks as CSV (e.g. 72,85,90): ")
    result = marks_average(user_input)
    print("Average Marks:", result if result is not None else "Invalid input")

    print("\n==== Running payable_award ====")
    user_input = input("Enter award|deduction (e.g. 5000|500): ")
    result = payable_award(user_input)
    print("Payable Award:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
