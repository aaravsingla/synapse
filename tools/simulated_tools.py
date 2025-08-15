# tools/simulated_tools.py
import json

def check_traffic(origin=None, destination=None):
    return {"severity":"major","delay_minutes":18,"alternatives":[{"route":"A->C->D","extra_mins":6}]}

def get_merchant_status(merchant_id=None):
    return {"merchant_id":merchant_id,"prep_time_min":40,"open_status":"open","backlog":12}

def get_nearby_merchants(merchant_type=None, location=None, radius_km=3):
    return {"nearby": [{"merchant_id":"m_102","name":"QuickBites","prep_time_min":12}]}

def notify_customer(customer_id=None, message=None):
    return {"customer_id":customer_id,"notified":True,"message":message}

def re_route_driver(driver_id=None, new_route=None):
    return {"driver_id":driver_id,"new_route":new_route,"status":"assigned"}

def collect_evidence(order_id=None):
    return {"order_id":order_id,"evidence":["photo_driver.jpg","photo_customer.jpg"],"notes":"images_collected"}

def analyze_evidence(evidence=None):
    return {"likely_cause":"merchant","confidence":0.85}

def issue_instant_refund(order_id=None, amount=0):
    return {"order_id":order_id,"refund_issued":True,"amount":amount}

def exonerate_driver(driver_id=None):
    return {"driver_id":driver_id,"exonerated":True}

def find_nearby_locker(location=None):
    return {"locker_id":"locker_77","distance_m":300,"available":True}

def check_flight_status(flight_number=None):
    return {"flight_number":flight_number,"status":"on_time","delay_minutes":0}



def initiate_mediation_flow(order_id=None):
    # Start a mediation session (simulated)
    return {"order_id": order_id, "mediation_session": f"med_{order_id}", "status": "started"}

def log_merchant_packaging_feedback(merchant_id=None, feedback=None):
    # Log feedback for merchant packaging
    return {"merchant_id": merchant_id, "logged": True, "feedback": feedback or "no_feedback"}

def notify_resolution(order_id=None, resolution=None):
    # Notify both customer and driver about resolution
    return {"order_id": order_id, "notified": True, "resolution": resolution}

def contact_recipient_via_chat(recipient_id=None, message=None):
    # Simulate contacting recipient via chat. Return simulated response.
    # For realism, sometimes recipient replies, sometimes not.
    return {
        "recipient_id": recipient_id,
        "message_sent": True,
        "recipient_response": "no_response",   # or "ok_leave_with_concierge"
    }

def suggest_safe_drop_off(location=None):
    # Suggest a nearby safe drop-off option (concierge / leave with neighbor)
    return {"suggestion": "leave_with_concierge", "details": f"concierge at {location}", "requires_permission": True}

def calculate_alternative_route(origin=None, destination=None):
    # Return a candidate alternate route and ETA change
    return {"route": f"{origin}->{destination} via alt", "eta_change_minutes": 5, "reason": "accident_avoidance"}

def notify_passenger_and_driver(passenger_id=None, driver_id=None, message=None):
    # Notify both passenger and driver
    return {
        "passenger_id": passenger_id,
        "driver_id": driver_id,
        "passenger_notified": True,
        "driver_notified": True,
        "message": message
    }
