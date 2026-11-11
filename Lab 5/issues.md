
# Lab 5 - Static Code Analysis
## Issues Identified and Fixed

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL Injection | Security | 9 | SQL query was constructed using string concatenation, allowing unsafe input to alter the query. | Replaced string concatenation with parameterized queries using placeholders. |
| Insecure Random Number Generation | Security | 21 | random.randint() generated predictable unlock PINs. | Replaced random.randint() with secrets.randbelow(). |
| Broad Exception Handling | Security/Quality | 30-33 | The program caught all exceptions and ignored them using pass. | Removed unnecessary exception handling so errors are not silently ignored. |
| Mutable Default Argument | Bug | 8 | A shared list was used as a default parameter, causing unintended data persistence. | Replaced the default list with None and initialized it inside the function. |
| Unused Variable | Code Quality | 26 | The variable summary was assigned but never used. | Removed the unused variable. |
| Missing Return Value | Bug | 13-17 | rentBike() returned None when renting failed. | Added an explicit return False. |
| Unsafe None Handling | Bug | 36-40 | The program accessed row[0] without verifying that a database result existed. | Added checks for None before accessing results. |
| Naming Convention | Style | Multiple | Function names were written in camelCase instead of snake_case. | Renamed functions to follow PEP 8 naming conventions. |
| Line Length | Style | Multiple | Several lines exceeded the recommended length. | Split long statements into multiple lines. |
| Missing Documentation | Quality | Multiple | Functions and the module lacked docstrings. | Added descriptive module and function docstrings. |

## Tools Used

- Pylint: Analyzed Python code quality and potential bugs.
- Bandit: Identified common security vulnerabilities.
- Flake8: Checked formatting and PEP 8 compliance.

## Conclusion

The identified issues were addressed by improving SQL query
security, random number generation, exception handling,
return values, database result validation, naming conventions,
and formatting.

The final program preserves the original functionality while
improving security, readability, and maintainability.
