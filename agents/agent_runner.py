# agents/agent_runner.py
import os, re, json, time
from google import genai
from tools import simulated_tools as tools
from tools.policy import estimate_confidence, policy_advice

# client reads GEMINI_API_KEY from env var by default
client = genai.Client()

MODEL = os.getenv("SYNAPSE_MODEL", "gemini-2.0-flash")  # dev-friendly; swap to gemini-2.5-flash if you have access

SYSTEM_INSTRUCTION = """You are Synapse, an agentic last-mile coordinator.
Follow this exact format when responding. Use JSON for tool args.

THOUGHT: <short reasoning>
ACTION: tool_name(<json_args>)
OBSERVATION: <tool output (will be injected by system)>
POLICY: <policy json with fields {confidence, escalate, advice, suggested_action?, suggested_args?}>
... repeat until solved ...
FINAL_PLAN: <human readable plan>

Rules:
- Use POLICY as a safety signal. If POLICY.escalate is true, you must either:
  (a) call a different tool to gather more info, or
  (b) choose a conservative, low-risk step (e.g., notify stakeholders, defer risky actions), or
  (c) if uncertainty remains, end with FINAL_PLAN that includes 'NEED HUMAN REVIEW'.
- If POLICY suggests a concrete next tool (suggested_action), consider using it.

Available tools and signatures:
- check_traffic(origin, destination)
- get_merchant_status(merchant_id)
- get_nearby_merchants(merchant_type, location, radius_km)
- notify_customer(customer_id, message)
- re_route_driver(driver_id, new_route)
- collect_evidence(order_id)
- analyze_evidence(evidence)
- issue_instant_refund(order_id, amount)
- exonerate_driver(driver_id)
- find_nearby_locker(location)
- check_flight_status(flight_number)
- initiate_mediation_flow(order_id)
- log_merchant_packaging_feedback(merchant_id, feedback)
- notify_resolution(order_id, resolution)
- contact_recipient_via_chat(recipient_id, message)
- suggest_safe_drop_off(location)
- calculate_alternative_route(origin, destination)
- notify_passenger_and_driver(passenger_id, driver_id, message)
"""

TOOL_MAP = {
    "check_traffic": tools.check_traffic,
    "get_merchant_status": tools.get_merchant_status,
    "get_nearby_merchants": tools.get_nearby_merchants,
    "notify_customer": tools.notify_customer,
    "re_route_driver": tools.re_route_driver,
    "collect_evidence": tools.collect_evidence,
    "analyze_evidence": tools.analyze_evidence,
    "issue_instant_refund": tools.issue_instant_refund,
    "exonerate_driver": tools.exonerate_driver,
    "find_nearby_locker": tools.find_nearby_locker,
    "check_flight_status": tools.check_flight_status,
    "initiate_mediation_flow": tools.initiate_mediation_flow,
    "log_merchant_packaging_feedback": tools.log_merchant_packaging_feedback,
    "notify_resolution": tools.notify_resolution,
    "contact_recipient_via_chat": tools.contact_recipient_via_chat,
    "suggest_safe_drop_off": tools.suggest_safe_drop_off,
    "calculate_alternative_route": tools.calculate_alternative_route,
    "notify_passenger_and_driver": tools.notify_passenger_and_driver,
}

ACTION_RE = re.compile(r"ACTION:\s*([a-zA-Z_0-9]+)\s*\(\s*(\{.*?\})\s*\)", re.DOTALL)


def run_scenario_text(scenario_text, max_steps=6, model=MODEL):
    trace = SYSTEM_INSTRUCTION + "\nScenario: " + scenario_text + "\n"
    full_trace = ""

    for step in range(max_steps):
        response = client.models.generate_content(
            model=model,
            contents=trace,
            config={"temperature": 0}
        )
        out = getattr(response, "text", None) or str(response)
        out = out.strip()
        full_trace += "\n" + out

        # find actions in the latest model output
        for m in ACTION_RE.finditer(out):
            tool_name = m.group(1)
            args_json = m.group(2)

            try:
                args = json.loads(args_json)
            except Exception:
                args = {}

            fn = TOOL_MAP.get(tool_name)
            if not fn:
                obs = {"error": f"unknown tool {tool_name}"}
            else:
                obs = fn(**args)

            obs_json = json.dumps(obs)

            # Confidence + policy advice
            conf = estimate_confidence(tool_name, args, obs)
            pol = policy_advice(tool_name, args, obs, conf)
            pol_json = json.dumps(pol)

            # Append both to the rolling context
            trace += f"\n{out}\nOBSERVATION: {obs_json}\nPOLICY: {pol_json}\n"

        # check for final plan
        if "FINAL_PLAN:" in out:
            break

        # if model made no ACTION and no FINAL_PLAN, still append model output and continue
        trace += "\n"  # small delimiter
        time.sleep(0.2)

    # extract final plan if present
    final = ""
    m = re.search(r"FINAL_PLAN:\s*(.*)$", full_trace, re.DOTALL)
    if m:
        final = m.group(1).strip()

    return {"trace": full_trace, "final_plan": final}
