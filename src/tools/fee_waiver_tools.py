import json
import uuid
import os
from typing import Dict, Any, Optional
from langchain_core.tools import tool
from src.database.mock_db import CUSTOMERS, add_waiver

# Load JSON data
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
POLICIES_PATH = os.path.join(BASE_DIR, "skills/fee_waiver/waiver_policies.json")

def _load_json(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)

# Internal Helper Functions
def _check_customer_history(customer_id: str) -> Dict[str, Any]:
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}
    
    return {
        "tenure_months": customer.get("tenure_months", 0),
        "late_payments_last_12m": customer.get("late_payments_last_12m", 0),
        "previous_waivers": customer.get("previous_waivers", 0),
        "days_overdue": customer.get("days_overdue", 0)
    }

# Public Tools
@tool
def check_customer_history(customer_id: str) -> Dict[str, Any]:
    """Retrieves payment and waiver history for a customer."""
    return _check_customer_history(customer_id)

@tool
def evaluate_waiver_eligibility(customer_id: str, hardship_reason: str = "") -> Dict[str, Any]:
    """
    Calculates a score to determine if a fee waiver should be granted.
    Returns the recommended waiver percentage and tier.
    """
    history = _check_customer_history(customer_id)
    if "error" in history:
        return history
        
    policies = _load_json(POLICIES_PATH)
    points = policies["points"]
    thresholds = policies["thresholds"]
    
    score = 0
    
    # 1. Tenure points
    score += (history["tenure_months"] // 12) * points["tenure_per_year"]
    
    # 2. History points
    if history["late_payments_last_12m"] == 0:
        score += points["clean_history_12m"]
    elif history["late_payments_last_12m"] < 3:
        pass 
    else:
        score -= 20 
        
    # 3. Previous waivers
    score += (history["previous_waivers"] * points["previous_waiver_penalty"])
    
    # 4. Reason analysis
    is_valid_reason = any(r in hardship_reason.lower() for r in policies["valid_reasons"])
    is_invalid_reason = any(r in hardship_reason.lower() for r in policies["invalid_reasons"])
    
    if is_valid_reason:
        score += points["hardship_valid"]
    elif is_invalid_reason:
        score += points["hardship_invalid"]
    
    # Determine Tier
    recommendation = {}
    if score >= thresholds["full_waiver_min_score"]:
        recommendation = {"tier": "Tier 1", "waiver_percent": 100, "decision": "APPROVE_FULL"}
    elif score >= thresholds["partial_waiver_min_score"]:
        recommendation = {"tier": "Tier 2", "waiver_percent": 50, "decision": "APPROVE_PARTIAL"}
    else:
        recommendation = {"tier": "Tier 3", "waiver_percent": 0, "decision": "DECLINE"}
        
    return {
        "customer_id": customer_id,
        "eligibility_score": score,
        "recommendation": recommendation,
        "factors": {
            "tenure_months": history["tenure_months"],
            "reason_valid": is_valid_reason
        }
    }

@tool
def process_waiver(customer_id: str, waiver_amount: float, reason: str) -> Dict[str, Any]:
    """
    Applies a fee waiver to the account.
    """
    policies = _load_json(POLICIES_PATH)
    
    # Check max cap
    if waiver_amount > policies["caps"]["max_waiver_amount"]:
        return {"error": f"Waiver amount ${waiver_amount} exceeds cap of ${policies['caps']['max_waiver_amount']}"}
        
    waiver_id = f"WV-{uuid.uuid4().hex[:8].upper()}"
    
    add_waiver(waiver_id, {
        "customer_id": customer_id,
        "amount": waiver_amount,
        "reason": reason,
        "date": "2023-10-27" 
    })
    
    # Mock update customer balance logic
    cust = CUSTOMERS.get(customer_id)
    if cust:
        cust["previous_waivers"] += 1
    
    return {
        "success": True, 
        "waiver_id": waiver_id, 
        "amount_waived": waiver_amount,
        "message": f"Waiver of ${waiver_amount} applied successfully."
    }

@tool
def get_waiver_policy() -> Dict[str, Any]:
    """Returns the current waiver policy rules."""
    return _load_json(POLICIES_PATH)

@tool
def send_waiver_notification(customer_id: str, waiver_id: str, waiver_amount: float) -> Dict[str, Any]:
    """Sends a notification about the approved waiver."""
    return {
         "sent_to_customer": customer_id,
         "content": f"Good news! We have waived ${waiver_amount} from your bill. Reference: {waiver_id}.",
         "status": "sent"
    }

@tool
def recommend_prevention(customer_id: str) -> Dict[str, Any]:
    """Returns suggestions to prevent future late fees."""
    return {
        "suggestions": [
            "Set up AutoPay to never miss a due date.",
            "Enable SMS Payment Reminders.",
            "Switch to Paperless Billing for faster notifications."
        ]
    }

@tool
def escalate_waiver(customer_id: str, reason: str) -> Dict[str, Any]:
    """Escalates a rejected waiver request to a human supervisor."""
    ticket_id = f"ESC-{uuid.uuid4().hex[:6].upper()}"
    return {
        "ticket_id": ticket_id,
        "status": "escalated",
        "sla": "24-48 hours",
        "message": "Your request has been forwarded to a supervisor for manual review."
    }
