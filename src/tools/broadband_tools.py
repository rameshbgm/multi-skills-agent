import json
import uuid
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from src.database.mock_db import APPOINTMENTS, add_appointment

# Load JSON data
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SLOTS_PATH = os.path.join(BASE_DIR, "skills/broadband_installation/appointment_slots.json")
AREAS_PATH = os.path.join(BASE_DIR, "skills/broadband_installation/service_areas.json")

def _load_json(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)

@tool
def check_service_availability(address: str, zip_code: str) -> Dict[str, Any]:
    """Checks which broadband technologies are available at a given zip code."""
    data = _load_json(AREAS_PATH)
    
    # Simple mock logic matching zip codes
    for area_name, details in data["service_areas"].items():
        if zip_code in details["zip_codes"]:
            return {
                "address": address,
                "zip_code": zip_code,
                "area_type": area_name,
                "available_technologies": details["technologies"],
                "servict_available": True
            }
    
    return {
        "address": address,
        "zip_code": zip_code,
        "service_available": False,
        "message": "Sorry, we do not cover this area yet."
    }

@tool
def get_available_slots(date_from: str, date_to: str, preferred_day: Optional[str] = None, preferred_time: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns available installation slots between two ISO dates (YYYY-MM-DD).
    """
    slots_data = _load_json(SLOTS_PATH)
    available = []
    
    # Mock logic: just generate next 7 days and map to 'Monday', 'Tuesday' etc.
    try:
        start = datetime.strptime(date_from, "%Y-%m-%d")
        end = datetime.strptime(date_to, "%Y-%m-%d")
    except ValueError:
        try:
             # Fallback if user gives informal dates, handle or error. 
             # For robustness, let's assume 'today' logic if parse fails or just return error
            start = datetime.now()
            end = start + timedelta(days=7)
        except Exception:
             return {"error": "Invalid date format. Use YYYY-MM-DD"}

    delta = (end - start).days
    
    for i in range(delta + 1):
        current = start + timedelta(days=i)
        day_name = current.strftime("%A")
        
        # Check against slots_data
        day_slots = slots_data["available_slots"].get(day_name, [])
        if day_slots:
            for slot in day_slots:
                # Filter if preferred
                if preferred_time and preferred_time not in slot:
                    continue
                available.append({
                    "date": current.strftime("%Y-%m-%d"),
                    "day": day_name,
                    "time_window": slot
                })
                
    # Filter by preferred day if set
    if preferred_day:
        available = [s for s in available if s["day"].lower() == preferred_day.lower()]

    return {"available_slots": available[:10], "note": "Showing max 10 slots."}

@tool
def schedule_installation(customer_id: str, address: str, appointment_date: str, appointment_time: str, service_plan: str, contact_phone: str) -> Dict[str, Any]:
    """
    Books an installation appointment.
    """
    # Simply generate ID
    appt_id = f"APPT-{uuid.uuid4().hex[:8].upper()}"
    
    # Validate plan exists in mock
    slots_data = _load_json(SLOTS_PATH)
    plan_details = slots_data["service_plans"].get(service_plan)
    if not plan_details:
        # Fuzzy match for demo
        found = False
        for pname, pdata in slots_data["service_plans"].items():
            if service_plan.lower() in pname.lower():
                service_plan = pname
                plan_details = pdata
                found = True
                break
        if not found:
            return {"error": f"Unknown Service Plan: {service_plan}"}

    booking = {
        "id": appt_id,
        "customer_id": customer_id,
        "address": address,
        "date": appointment_date,
        "time": appointment_time,
        "plan": service_plan,
        "technician_id": "TECH-99",
        "status": "SCHEDULED",
        "fees": plan_details["install_fee"]
    }
    
    add_appointment(appt_id, booking)
    
    return {
        "success": True,
        "appointment_id": appt_id,
        "technician_id": "TECH-99",
        "next_steps": "Ensure someone over 18 is home. Technician will call 30 mins prior.",
        "fee_quoted": plan_details["install_fee"]
    }

@tool
def check_installation_status(appointment_id: str) -> Dict[str, Any]:
    """Checks status of an appointment."""
    from src.database.mock_db import get_appointment
    appt = get_appointment(appointment_id)
    if not appt:
        return {"error": "Appointment not found"}
    return appt

@tool
def reschedule_appointment(appointment_id: str, new_date: str, new_time: str) -> Dict[str, Any]:
    """Reschedules an existing appointment."""
    from src.database.mock_db import get_appointment, update_appointment
    appt = get_appointment(appointment_id)
    if not appt:
        return {"error": "Appointment not found"}
    
    update_appointment(appointment_id, {"date": new_date, "time": new_time, "status": "RESCHEDULED"})
    return {"success": True, "new_date": new_date, "new_time": new_time, "message": "Appointment updated."}

@tool
def cancel_appointment(appointment_id: str, reason: str = "") -> Dict[str, Any]:
    """Cancels an existing appointment."""
    from src.database.mock_db import get_appointment, update_appointment
    appt = get_appointment(appointment_id)
    if not appt:
        return {"error": "Appointment not found"}
    
    update_appointment(appointment_id, {"status": "CANCELLED", "cancellation_reason": reason})
    return {"success": True, "message": "Appointment cancelled."}
