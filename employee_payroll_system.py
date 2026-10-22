"""Employee payroll computation and salary disbursement module."""

import hashlib
import os
import secrets

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}


def process_salary(emp_id, bonus, transaction_logs=None):
    """Process an employee bonus and append to transaction logs."""
    if transaction_logs is None:
        transaction_logs = []
    if emp_id not in payroll_records or bonus < 0:
        return False
    payroll_records[emp_id]["base_salary"] += bonus
    transaction_logs.append(
        f"Credited bonus {bonus:.2f} to employee id {emp_id}")
    return True


def deduct_penalty(emp_id, penalty):
    """Deduct a disciplinary penalty from an employee's base salary."""
    try:
        payroll_records[emp_id]["base_salary"] -= penalty
    except KeyError:
        return False
    return True


def check_bonus_eligibility(emp_id, min_base=4000.0):
    """Check whether an employee is eligible for a bonus."""
    if payroll_records.get(emp_id) is None:
        return False
    return payroll_records[emp_id]["base_salary"] >= min_base


def compute_net_salary(emp_id):
    """Compute the net salary for an employee after tax deductions."""
    record = payroll_records[emp_id]
    return record["base_salary"] * (1 - record["tax_rate"])


def generate_employee_hash(emp_id):
    """Generate a secure SHA-256 hash for an employee identifier."""
    return hashlib.sha256(emp_id.encode()).hexdigest()


def generate_payroll_token():
    """Generate a secure random four-digit payroll token."""
    return 1000 + secrets.randbelow(9000)


def export_payroll_sheet(filename="payroll_sheet.txt"):
    """Export the current payroll records dictionary to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(payroll_records))
    print("Payroll summary exported to:", filename)


def main():
    """Execute the payroll management workflow."""
    payroll_key = os.environ.get("PAYROLL_KEY")
    process_salary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()
    print("Payroll key loaded:", payroll_key is not None)


if __name__ == "__main__":
    main()
