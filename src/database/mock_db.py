from typing import Dict, Any

# Mock Customer Database
CUSTOMERS: Dict[str, Dict[str, Any]] = {
    "CUST001": {
        "id": "CUST001",
        "name": "Alice Smith",
        "account_type": "PREPAID",
        "status": "ACTIVE",
        "balance": 25.50,
        "credit_limit": 0.0,
        "roaming_enabled": False,
        "tenure_months": 36,
        "late_payments_last_12m": 0,
        "previous_waivers": 0,
        "current_bill_amount": 45.00,
        "days_overdue": 0,
        "contact_phone": "+15550101"
    },
    "CUST002": {
        "id": "CUST002",
        "name": "Bob Jones",
        "account_type": "POSTPAID",
        "status": "ACTIVE",
        "balance": -120.00, # Owing amount
        "credit_limit": 500.0,
        "roaming_enabled": True,
        "tenure_months": 12,
        "late_payments_last_12m": 2,
        "previous_waivers": 1,
        "current_bill_amount": 120.00,
        "days_overdue": 5,
        "contact_phone": "+15550102"
    },
    "CUST003": {
        "id": "CUST003",
        "name": "Charlie Brown",
        "account_type": "POSTPAID",
        "status": "SUSPENDED",
        "balance": -300.00,
        "credit_limit": 300.0,
        "roaming_enabled": False,
        "tenure_months": 60,
        "late_payments_last_12m": 5,
        "previous_waivers": 3,
        "current_bill_amount": 300.00,
        "days_overdue": 45,
         "contact_phone": "+15550103"
    }
}

APPOINTMENTS: Dict[str, Dict[str, Any]] = {}
WAIVERS: Dict[str, Dict[str, Any]] = {}

def get_customer(customer_id: str) -> Dict[str, Any] | None:
    return CUSTOMERS.get(customer_id)

def update_customer(customer_id: str, data: Dict[str, Any]) -> None:
    if customer_id in CUSTOMERS:
        CUSTOMERS[customer_id].update(data)

def add_appointment(appointment_id: str, data: Dict[str, Any]) -> None:
    APPOINTMENTS[appointment_id] = data

def get_appointment(appointment_id: str) -> Dict[str, Any] | None:
    return APPOINTMENTS.get(appointment_id)

def update_appointment(appointment_id: str, data: Dict[str, Any]) -> None:
    if appointment_id in APPOINTMENTS:
        APPOINTMENTS[appointment_id].update(data)

def add_waiver(waiver_id: str, data: Dict[str, Any]) -> None:
    WAIVERS[waiver_id] = data
