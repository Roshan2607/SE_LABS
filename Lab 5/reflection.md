
# Lab 5 - Static Code Analysis Reflection

## 1. What did you learn from static code analysis?

I learned that static code analysis helps identify bugs,
security vulnerabilities, and formatting issues without
executing the program.

Tools such as Pylint, Bandit, and Flake8 help improve
code quality, readability, security, and maintainability.

## 2. Which issues were identified, and which were most important?

The analysis identified issues such as SQL injection,
insecure random number generation, mutable default
arguments, unused variables, and inconsistent formatting.

The SQL injection vulnerability was especially important
because constructing SQL queries using string
concatenation can allow unsafe input to change the
meaning of a database query.

## 3. How did the tools help improve the program?

Pylint helped identify code quality issues such as
mutable default arguments and unused variables.

Bandit helped identify security issues such as insecure
random number generation and unsafe SQL construction.

Flake8 helped improve the code's readability by
identifying formatting and PEP 8 style violations.

These tools helped make the program easier to understand,
maintain, and debug.

## 4. What are the limitations of static analysis?

Static analysis cannot guarantee that a program works
correctly under every condition.

It may also report false positives and cannot detect
every logical error.

Therefore, static analysis should be combined with
program execution, testing, and code review to ensure
reliable software.
