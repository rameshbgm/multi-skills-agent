"""
Database MCP - In-Memory Employee Database (No External Dependencies)

This module provides MCP tools for querying an in-memory SQLite employee database.
No external database or API key required.

Tools:
- get_all_employees: List all employees
- get_employee_by_id: Get employee by ID
- search_employees: Search employees by name or department
- get_department_stats: Get department statistics
"""

import json
import logging
import sqlite3
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# In-memory SQLite database connection
_db_connection = None


def _get_db():
    """Get or create the in-memory database connection."""
    global _db_connection
    if _db_connection is None:
        _db_connection = sqlite3.connect(":memory:", check_same_thread=False)
        _db_connection.row_factory = sqlite3.Row
        _init_database(_db_connection)
    return _db_connection


def _init_database(conn):
    """Initialize the employee database with sample data."""
    cursor = conn.cursor()
    
    # Create employee table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            job_title TEXT NOT NULL,
            salary REAL NOT NULL,
            hire_date TEXT NOT NULL,
            phone TEXT,
            city TEXT
        )
    """)
    
    # Insert 15 sample employees
    employees = [
        (1, "John", "Smith", "john.smith@company.com", "Engineering", "Senior Software Engineer", 95000, "2020-03-15", "+1-555-0101", "San Francisco"),
        (2, "Sarah", "Johnson", "sarah.johnson@company.com", "Engineering", "Tech Lead", 120000, "2018-06-20", "+1-555-0102", "San Francisco"),
        (3, "Michael", "Williams", "michael.williams@company.com", "Sales", "Sales Manager", 85000, "2019-01-10", "+1-555-0103", "New York"),
        (4, "Emily", "Brown", "emily.brown@company.com", "Marketing", "Marketing Director", 110000, "2017-09-05", "+1-555-0104", "Chicago"),
        (5, "David", "Jones", "david.jones@company.com", "Engineering", "DevOps Engineer", 90000, "2021-02-28", "+1-555-0105", "Seattle"),
        (6, "Jessica", "Garcia", "jessica.garcia@company.com", "HR", "HR Manager", 75000, "2019-07-15", "+1-555-0106", "Austin"),
        (7, "James", "Miller", "james.miller@company.com", "Finance", "Financial Analyst", 80000, "2020-11-01", "+1-555-0107", "Boston"),
        (8, "Amanda", "Davis", "amanda.davis@company.com", "Engineering", "Frontend Developer", 85000, "2022-01-20", "+1-555-0108", "San Francisco"),
        (9, "Robert", "Martinez", "robert.martinez@company.com", "Sales", "Account Executive", 70000, "2021-05-12", "+1-555-0109", "Los Angeles"),
        (10, "Lisa", "Anderson", "lisa.anderson@company.com", "Marketing", "Content Strategist", 72000, "2020-08-18", "+1-555-0110", "Chicago"),
        (11, "William", "Taylor", "william.taylor@company.com", "Engineering", "Backend Developer", 88000, "2021-09-30", "+1-555-0111", "Seattle"),
        (12, "Jennifer", "Thomas", "jennifer.thomas@company.com", "Finance", "Accountant", 68000, "2019-04-22", "+1-555-0112", "Boston"),
        (13, "Christopher", "Moore", "christopher.moore@company.com", "Sales", "Sales Representative", 62000, "2022-03-14", "+1-555-0113", "New York"),
        (14, "Ashley", "Jackson", "ashley.jackson@company.com", "HR", "Recruiter", 65000, "2021-07-08", "+1-555-0114", "Austin"),
        (15, "Daniel", "White", "daniel.white@company.com", "Engineering", "QA Engineer", 78000, "2020-12-10", "+1-555-0115", "San Francisco"),
    ]
    
    cursor.executemany("""
        INSERT INTO employees (id, first_name, last_name, email, department, job_title, salary, hire_date, phone, city)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, employees)
    
    conn.commit()
    logger.info("Employee database initialized with 15 records")


def _row_to_dict(row):
    """Convert a sqlite3.Row to a dictionary."""
    return dict(row)


@tool
def get_all_employees(limit: int = 10) -> str:
    """
    Get all employees from the database.
    
    Args:
        limit: Maximum number of employees to return (1-15, default: 10)
    
    Returns:
        List of all employees with their details
    """
    try:
        conn = _get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees LIMIT ?", (min(limit, 15),))
        rows = cursor.fetchall()
        
        employees = [_row_to_dict(row) for row in rows]
        
        return json.dumps({
            "total_count": len(employees),
            "employees": employees
        }, indent=2)
    except Exception as e:
        logger.error(f"Database error: {e}")
        return f"Error: {str(e)}"


@tool
def get_employee_by_id(employee_id: int) -> str:
    """
    Get a specific employee by their ID.
    
    Args:
        employee_id: The employee's ID number (1-15)
    
    Returns:
        Employee details if found
    """
    try:
        conn = _get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        row = cursor.fetchone()
        
        if row:
            return json.dumps({
                "found": True,
                "employee": _row_to_dict(row)
            }, indent=2)
        else:
            return json.dumps({
                "found": False,
                "message": f"No employee found with ID {employee_id}"
            }, indent=2)
    except Exception as e:
        logger.error(f"Database error: {e}")
        return f"Error: {str(e)}"


@tool
def search_employees(query: str, search_by: str = "name") -> str:
    """
    Search employees by name or department.
    
    Args:
        query: Search term (e.g., "John", "Engineering", "San Francisco")
        search_by: Field to search - "name", "department", or "city" (default: "name")
    
    Returns:
        List of matching employees
    """
    try:
        conn = _get_db()
        cursor = conn.cursor()
        search_term = f"%{query}%"
        
        if search_by.lower() == "department":
            cursor.execute(
                "SELECT * FROM employees WHERE department LIKE ?",
                (search_term,)
            )
        elif search_by.lower() == "city":
            cursor.execute(
                "SELECT * FROM employees WHERE city LIKE ?",
                (search_term,)
            )
        else:
            cursor.execute(
                "SELECT * FROM employees WHERE first_name LIKE ? OR last_name LIKE ?",
                (search_term, search_term)
            )
        
        rows = cursor.fetchall()
        employees = [_row_to_dict(row) for row in rows]
        
        return json.dumps({
            "query": query,
            "search_by": search_by,
            "results_count": len(employees),
            "employees": employees
        }, indent=2)
    except Exception as e:
        logger.error(f"Database error: {e}")
        return f"Error: {str(e)}"


@tool
def get_department_stats() -> str:
    """
    Get statistics about employees by department.
    
    Returns:
        Department-wise employee count, average salary, and total headcount
    """
    try:
        conn = _get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                department,
                COUNT(*) as employee_count,
                ROUND(AVG(salary), 2) as avg_salary,
                ROUND(MIN(salary), 2) as min_salary,
                ROUND(MAX(salary), 2) as max_salary
            FROM employees
            GROUP BY department
            ORDER BY employee_count DESC
        """)
        
        rows = cursor.fetchall()
        departments = [_row_to_dict(row) for row in rows]
        
        cursor.execute("SELECT COUNT(*) as total FROM employees")
        total = cursor.fetchone()["total"]
        
        cursor.execute("SELECT ROUND(AVG(salary), 2) as avg FROM employees")
        company_avg = cursor.fetchone()["avg"]
        
        return json.dumps({
            "total_employees": total,
            "company_avg_salary": company_avg,
            "departments": departments
        }, indent=2)
    except Exception as e:
        logger.error(f"Database error: {e}")
        return f"Error: {str(e)}"


DATABASE_TOOLS = [
    get_all_employees,
    get_employee_by_id,
    search_employees,
    get_department_stats
]
