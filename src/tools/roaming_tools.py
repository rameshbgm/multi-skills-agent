import json
import uuid
import os
from typing import Dict, Any, Optional
from langchain_core.tools import tool
from src.database.mock_db import CUSTOMERS

# Load JSON data
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RATES_PATH = os.path.join(BASE_DIR, "skills/roaming_activation/roaming_rates.json")
COUNTRY_CODES_PATH = os.path.join(BASE_DIR, "skills/roaming_activation/country_codes.json")

def _load_json(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)

# Internal Helper Functions
def _verify_customer_account(customer_id: str) -> Dict[str, Any]:
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return {"error": "Customer not found", "customer_id": customer_id}
    return customer

def _check_roaming_eligibility(customer_id: str) -> Dict[str, Any]:
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}
    
    if customer["status"] != "ACTIVE":
        return {"eligible": False, "reason": f"Account status is {customer['status']}"}
    
    if customer["account_type"] == "POSTPAID" and customer["balance"] < -customer["credit_limit"]:
         return {"eligible": False, "reason": "Credit limit exceeded"}
    
    if customer["account_type"] == "PREPAID" and customer["balance"] < 10.0:
         return {"eligible": False, "reason": "Insufficient prepaid balance"}
         
    return {"eligible": True, "current_roaming_status": customer["roaming_enabled"]}

def _get_roaming_rates(destination_country: str, package_type: str = "weekly_pass") -> Dict[str, Any]:
    try:
        rates_data = _load_json(RATES_PATH)
        country_codes = _load_json(COUNTRY_CODES_PATH)
    except Exception as e:
        return {"error": f"Failed to load rate data: {str(e)}"}

    country_code = destination_country.upper()
    if len(country_code) > 2:
        code = country_codes.get(destination_country)
        if code:
            country_code = code
    
    if country_code in rates_data["restricted_countries"]:
        return {"restricted": True, "message": f"Roaming is not available in {destination_country}."}
    
    country_info = rates_data["country_rates"].get(country_code)
    if not country_info:
        country_info = {"name": destination_country, "price_multiplier": 1.5, "network_quality": "3G/4G"}

    package = rates_data["roaming_packages"].get(package_type)
    if not package:
        return {"error": f"Invalid package type: {package_type}. Options: daily_pass, weekly_pass, monthly_plan"}

    final_price = package["base_price"] * country_info["price_multiplier"]
    
    return {
        "destination": country_info["name"],
        "package": package["name"],
        "duration_days": package["duration_days"],
        "data_gb": package["data_gb"],
        "total_price": round(final_price, 2),
        "network_quality": country_info["network_quality"]
    }

# Public Tools

@tool
def verify_customer_account(customer_id: str) -> Dict[str, Any]:
    """Retrieves customer account details like status, balance, and roaming flags."""
    return _verify_customer_account(customer_id)

@tool
def check_roaming_eligibility(customer_id: str) -> Dict[str, Any]:
    """Checks if the customer is eligible for roaming services."""
    return _check_roaming_eligibility(customer_id)

@tool
def get_roaming_rates(destination_country: str, package_type: str = "weekly_pass") -> Dict[str, Any]:
    """
    Looks up roaming rates for a specific country and package type.
    package_type options: 'daily_pass', 'weekly_pass', 'monthly_plan'
    """
    return _get_roaming_rates(destination_country, package_type)

@tool
def activate_roaming_service(customer_id: str, destination_country: str, package_type: str) -> Dict[str, Any]:
    """Activates a specific roaming package for a customer."""
    check = _check_roaming_eligibility(customer_id)
    if not check.get("eligible"):
        return {"error": "Activation failed", "details": check}

    rates = _get_roaming_rates(destination_country, package_type)
    if rates.get("error") or rates.get("restricted"):
        return {"error": "Activation failed", "details": rates}

    ref_num = f"ROAM-{uuid.uuid4().hex[:8].upper()}"
    
    db_cust = CUSTOMERS.get(customer_id)
    if db_cust:
        db_cust["roaming_enabled"] = True
    
    return {
        "success": True, 
        "reference_number": ref_num,
        "message": f"Roaming activated for {rates['destination']}. Package: {rates['package']}.",
        "activation_code": "Enter *123# when you arrive."
    }

@tool
def get_customer_balance(customer_id: str) -> Dict[str, Any]:
    """Returns the customer's current balance."""
    cust = _verify_customer_account(customer_id)
    if "error" in cust:
        return cust
    return {"customer_id": customer_id, "balance": cust["balance"], "currency": "USD"}

@tool
def send_activation_confirmation(customer_id: str, reference_number: str, phone_number: str) -> Dict[str, Any]:
    """Sends a confirmation SMS to the customer."""
    return {
        "sent_to": phone_number,
        "content": f"TelecomAgent: Your roaming plan is active. Ref: {reference_number}. Safe travels!",
        "status": "delivered"
    }
