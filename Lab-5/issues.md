# Issues Found — employee_payroll_system.py

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (Bandit B605, High) | Security | 58 | `os.system()` runs the filename through the shell, so a bad filename could run other commands. | Replace it with a normal `print()`. |
| Weak MD5 hash (Bandit B324, High) | Security | 47 | MD5 is broken and shouldn't be used for hashing. | Use `hashlib.sha256` instead. |
| Use of `eval()` (Bandit B307, Medium) | Security | 42 | `eval` runs any string as Python code. | Remove `eval` and calculate the net salary directly. |
| Wrong net salary (found manually) | Bug | 40–43, 66 | Everyone is taxed a flat 15% even though each employee has their own `tax_rate`. | Use `base * (1 - tax_rate)` from the employee's record. |
| Hardcoded secret key (found manually) | Security | 62, 70 | The secret key is written in the code and printed to the screen. | Read it from an environment variable and don't print it. |
| Mutable default argument (Pylint W0102) | Bug | 15 | `transaction_logs=[]` is shared between every call. | Default to `None` and create a new list inside the function. |
| Bare `except: pass` (Bandit B110, Pylint W0702, Flake8 E722) | Bug | 26–27 | All errors are silently ignored, so a wrong employee ID fails without any message. | Catch only `KeyError` and return `False`. |
| Insecure random token (Bandit B311, Low) | Security | 51 | `random` is predictable, so it's not safe for tokens. | Use the `secrets` module. |
| Style issues (Pylint / Flake8) | Style | 6, 15, 19, 31, 32, 73 | Unused import and variables, camelCase function name, `== None`, line too long, missing docstrings, no final newline. | Remove unused code, rename to `process_salary`, use `is None`, add docstrings, wrap the long line, add the newline. |
