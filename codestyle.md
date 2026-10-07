# Backend Code Style Guide

## 1. Code Style References

The Python code in this project mainly follows:

- PEP 8 — Style Guide for Python Code  
  https://peps.python.org/pep-0008/

- PEP 257 — Docstring Conventions  
  https://peps.python.org/pep-0257/

The project follows these standards while making reasonable adjustments according to the scale and requirements of the calculator system.

---

## 2. General Principles

Backend code should remain:

- Secure
- Readable
- Modular
- Testable
- Maintainable
- Clearly separated from frontend responsibilities

---

## 3. Indentation

Use 4 spaces for each indentation level.

Do not use tabs.

Example:

```python
def calculate():
    result = calculate_expression(expression)
    return result
```

---

## 4. Naming Conventions

### Variables and Functions

Use snake_case.

Examples:

```python
calculate_expression
history_id
get_connection
```

### Classes

Use PascalCase.

Example:

```python
ExpressionError
```

### Constants

Use uppercase snake case.

Examples:

```python
DATABASE_PATH
MAX_EXPRESSION_LENGTH
MAX_AST_NODES
```

---

## 5. Module Responsibilities

### `app.py`

Responsible for:

- HTTP routes
- Request validation
- JSON responses
- HTTP status codes
- CORS configuration

### `database.py`

Responsible for:

- SQLite connections
- Database initialization
- History insertion
- History query
- History deletion
- Clear all history

### `services/calculator_service.py`

Responsible for:

- Expression parsing
- Operator validation
- Mathematical calculation
- Calculation exception handling

### `tests/`

Responsible for:

- Automated testing of the calculation module

---

## 6. Expression Security Rules

User mathematical expressions must never be executed using:

```python
eval()
```

or:

```python
exec()
```

The project uses Python AST parsing.

Only explicitly allowed AST node types and operators are evaluated.

Allowed binary operators:

- Addition
- Subtraction
- Multiplication
- Division

Allowed unary operators:

- Unary plus
- Unary minus

Other executable Python syntax is rejected.

---

## 7. Error Handling

Expected user input errors should be converted into controlled exceptions.

Examples:

- Invalid expression
- Empty expression
- Division by zero
- Unsupported operator
- Expression too long
- Expression too complex

The Flask API should return appropriate HTTP status codes.

Examples:

```text
200 OK
400 Bad Request
404 Not Found
405 Method Not Allowed
```

---

## 8. Database Rules

Database operations should:

- Use parameterized SQL queries
- Close database connections
- Commit write operations
- Avoid building SQL statements from raw user input

Example:

```python
connection.execute(
    """
    DELETE FROM calculation_history
    WHERE id = ?
    """,
    (history_id,),
)
```

---

## 9. Documentation

Important functions should include concise docstrings.

Example:

```python
def get_history():
    """Get all calculation history records."""
```

Comments should explain design decisions rather than repeat obvious code.

---

## 10. Testing

Core calculation logic should have automated tests.

Tests should cover:

- Addition
- Subtraction
- Multiplication
- Division
- Operator precedence
- Parentheses
- Decimal numbers
- Unary operators
- Division by zero
- Invalid expressions
- Unsupported operators
- Dangerous function calls

---

## 11. Front-End / Back-End Separation

The backend is responsible for:

- Receiving calculation requests
- Validating input
- Parsing expressions
- Performing calculations
- Handling errors
- Saving calculation history
- Reading calculation history
- Deleting calculation history
- Returning standardized JSON responses

The frontend must not generate the authoritative final calculation result.

---

## 12. API Design

Main APIs:

```text
POST   /api/calculate
GET    /api/history
DELETE /api/history/{id}
DELETE /api/history
GET    /api/health
```

Each API should have a clear responsibility.

---

## 13. File Responsibilities

### `app.py`

Responsible for Flask routes and API responses.

### `database.py`

Responsible for database operations.

### `services/calculator_service.py`

Responsible for safe expression parsing and mathematical calculation.

### `tests/test_calculator_service.py`

Responsible for automated calculation tests.

---

## 14. Summary

The backend follows the principles of:

- PEP 8 style
- Clear naming
- Modular design
- Secure expression parsing
- Parameterized SQL
- Explicit error handling
- Automated testing
- Clear front-end / back-end separation