# Front-End and Back-End Separation Calculator — Backend

## 1. Project Introduction

This repository contains the backend of the Front-End and Back-End Separation Calculator System.

The backend is responsible for:

- Receiving calculation requests
- Validating user input
- Parsing mathematical expressions
- Performing calculations
- Handling calculation errors
- Saving calculation history
- Querying calculation history
- Deleting calculation history
- Returning standardized JSON responses

The final mathematical calculation is performed entirely by the backend.

---

## 2. GitHub Repository

Backend Repository:

https://github.com/hodden2026/832401221_calculator_backend

Frontend Repository:

https://github.com/hodden2026/832401221_calculator_frontend

---

## 3. Technology Stack

- Python 3.12
- Flask
- SQLite
- Python AST
- unittest
- Gunicorn for production deployment

---

## 4. Main Features

### Basic Calculation

Supports:

- Addition
- Subtraction
- Multiplication
- Division

### Compound Expressions

Supports:

- Operator precedence
- Parentheses
- Decimal numbers
- Unary positive numbers
- Unary negative numbers

Examples:

```text
1+2*3
(1+2)*3
-5+8
3*-2
1.5+2.3
```

### Error Handling

Handles:

- Invalid expressions
- Empty expressions
- Division by zero
- Unsupported operators
- Excessively long expressions
- Excessively complex expressions

### Calculation History

Each successful calculation is stored in an SQLite database.

Stored information includes:

- ID
- Expression
- Result
- Calculation time

### History Management

Supports:

- Query all history
- Delete specified history
- Clear all history

---

## 5. Security Design

The backend does NOT use:

```python
eval()
```

or:

```python
exec()
```

to execute user expressions.

Instead, the project uses Python's Abstract Syntax Tree module:

```python
ast
```

The expression is parsed first and only explicitly allowed mathematical nodes and operators are evaluated.

Allowed binary operators:

```text
+
-
*
/
```

Allowed unary operators:

```text
+
-
```

Function calls, arbitrary Python code, unsupported operators, and other unsafe syntax are rejected.

---

## 6. Project Structure

```text
calculator_backend/
├── services/
│   ├── __init__.py
│   └── calculator_service.py
├── tests/
│   ├── __init__.py
│   └── test_calculator_service.py
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── codestyle.md
└── .gitignore
```

---

## 7. File Responsibilities

### `app.py`

Responsible for:

- Flask application
- HTTP APIs
- Input validation
- JSON responses
- CORS configuration

### `database.py`

Responsible for:

- SQLite connection
- Database initialization
- Insert history
- Query history
- Delete history
- Clear all history

### `services/calculator_service.py`

Responsible for:

- Safe expression parsing
- Mathematical calculation
- Operator validation
- Calculation exceptions

### `tests/test_calculator_service.py`

Contains automated tests for the calculation module.

---

## 8. Runtime Environment

Recommended:

```text
Python 3.12+
```

The project was developed using Python 3.12.

---

## 9. Installation

Clone or download the repository.

Enter the backend directory:

```bash
cd calculator_backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows CMD

Activate:

```cmd
.venv\Scripts\activate.bat
```

### Windows PowerShell Alternative

If PowerShell execution policy prevents activation, use the virtual environment Python directly:

```powershell
.\.venv\Scripts\python.exe
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## 10. Database Initialization

The project uses SQLite.

The database file is:

```text
calculator.db
```

The database is initialized automatically when the backend starts.

The main table is:

```text
calculation_history
```

Fields:

```text
id
expression
result
created_at
```

No manual SQL initialization is required.

---

## 11. Local Startup

### Using an activated virtual environment

```bash
python app.py
```

### Windows PowerShell

You can also run:

```powershell
.\.venv\Scripts\python.exe app.py
```

The backend starts at:

```text
http://127.0.0.1:5000
```

---

## 12. API Design

### Health Check

```http
GET /api/health
```

Example:

```json
{
    "success": true,
    "status": "online"
}
```

---

### Calculate Expression

```http
POST /api/calculate
```

Request:

```json
{
    "expression": "(1+2)*3"
}
```

Successful response:

```json
{
    "success": true,
    "expression": "(1+2)*3",
    "result": 9,
    "history_id": 1
}
```

Error example:

```json
{
    "success": false,
    "message": "Division by zero"
}
```

---

### Get Calculation History

```http
GET /api/history
```

The endpoint returns calculation records stored in SQLite.

---

### Delete Specified History

```http
DELETE /api/history/{id}
```

Example:

```http
DELETE /api/history/1
```

---

### Clear All History

```http
DELETE /api/history
```

---

## 13. HTTP Status Codes

The API uses appropriate HTTP status codes.

Examples:

```text
200 OK
400 Bad Request
404 Not Found
405 Method Not Allowed
```

---

## 14. Automated Tests

Run:

```bash
python -m unittest discover -s tests -v
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests cover:

- Addition
- Subtraction
- Multiplication
- Division
- Operator precedence
- Parentheses
- Decimal numbers
- Unary positive and negative values
- Division by zero
- Invalid expressions
- Unsupported operators
- Rejection of unsafe function calls

A successful test run ends with:

```text
OK
```

---

## 15. Front-End / Back-End Communication

The frontend sends only the mathematical expression.

Example:

```json
{
    "expression": "1+2*3"
}
```

The backend process is:

```text
Receive expression
        ↓
Validate input
        ↓
Parse AST
        ↓
Calculate result
        ↓
Store successful calculation
        ↓
Return JSON result
```

The frontend does not calculate the final result independently.

---

## 16. Production Deployment

The project includes:

```text
gunicorn
```

in `requirements.txt`.

A production deployment can use:

```bash
gunicorn app:app
```

The final public deployment configuration depends on the hosting platform.

---

## 17. Code Style

See:

```text
codestyle.md
```

Python coding conventions mainly follow:

- PEP 8
- PEP 257