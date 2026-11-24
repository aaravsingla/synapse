import os
import streamlit as st

# ✅ Set env vars from Streamlit secrets BEFORE importing agent_runner
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
# set GOOGLE_API_KEY too, for compatibility with google-genai
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
elif "GEMINI_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]

import json
from agents.agent_runner import run_scenario_text, DEFAULT_MODEL

st.set_page_config(page_title="Synapse Agent Demo", layout="wide")

st.title("🤖 Project Synapse Demo")
st.write("Interactive demo of the Synapse agent. Choose a scenario or enter your own.")

# Sidebar Configuration
st.sidebar.header("Configuration")
api_key_from_env = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
user_api_key = st.sidebar.text_input(
    "Gemini API Key:",
    type="password",
    value=api_key_from_env,
    help="Loaded automatically from Streamlit secrets or environment if configured."
)
if user_api_key:
    os.environ["GEMINI_API_KEY"] = user_api_key
    os.environ["GOOGLE_API_KEY"] = user_api_key

available_models = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-pro"]
selected_model = st.sidebar.selectbox(
    "Gemini Model:",
    available_models,
    index=0,
    help="Default is gemini-2.5-flash (gemini-2.0-flash has been retired by Google)."
)

# Sidebar for inputs
st.sidebar.header("Scenario Selection")
scenario_choice = st.sidebar.radio(
    "Pick a scenario:",
    ["Overloaded Restaurant", "Damaged Packaging Dispute", "Recipient Unavailable", "Traffic Obstruction", "Custom"]
)

scenario_text = ""
if scenario_choice == "Overloaded Restaurant":
    scenario_text = "Order #A123: merchant m_22 reports prep_time_min=40, driver d_9 is idle nearby, customer c_55 expects food in 20 minutes. Resolve with minimal wait and minimal driver idle time."
elif scenario_choice == "Damaged Packaging Dispute":
    scenario_text = "At delivery, dispute arises over spilled drink; unclear if merchant packaging or driver fault."
elif scenario_choice == "Recipient Unavailable":
    scenario_text = "Driver arrives at destination but recipient is unavailable to receive package."
elif scenario_choice == "Traffic Obstruction":
    scenario_text = "Passenger is on urgent trip; check_traffic() detects major accident on planned route."
else:
    scenario_text = st.sidebar.text_area("Describe your scenario:")

# Run agent button
if st.sidebar.button("Run Scenario"):
    effective_key = user_api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not effective_key:
        st.error("⚠️ Gemini API Key not found! Please set `GEMINI_API_KEY` in your Streamlit secrets or enter it in the sidebar.")
    elif scenario_text.strip() == "":
        st.warning("Please enter a scenario.")
    else:
        try:
            with st.spinner("Running Synapse agent..."):
                result = run_scenario_text(scenario_text, model=selected_model, api_key=effective_key)
            
            # ✅ SHOW FINAL PLAN FIRST
            st.subheader("✅ Final Plan")
            if result["final_plan"]:
                st.success(result["final_plan"])
            else:
                st.info("No final plan generated.")
            
            # ✅ SHOW AGENT TRACE SECOND (with expander for better UX)
            with st.expander("🔍 View Detailed Agent Trace", expanded=False):
                steps = result["trace"].splitlines()
                for line in steps:
                    if line.startswith("THOUGHT:"):
                        st.markdown(f"🧠 **{line}**")
                    elif line.startswith("ACTION:"):
                        st.markdown(f"🔧 `{line}`")
                    elif line.startswith("OBSERVATION:"):
                        try:
                            obs = json.loads(line.replace("OBSERVATION:", "").strip())
                            st.json(obs)
                        except:
                            st.write(line)
                    elif line.startswith("POLICY:"):
                        try:
                            pol = json.loads(line.replace("POLICY:", "").strip())
                            color = "red" if pol.get("escalate") else "green"
                            st.markdown(f"🛡️ **POLICY (conf {pol['confidence']})**")
                            st.json(pol)
                        except:
                            st.write(line)
                    elif line.startswith("FINAL_PLAN:"):
                        st.success(line)
        except Exception as e:
            st.error(f"❌ Error running agent: {e}")
            err_msg = str(e)
            if any(term in err_msg for term in ["API_KEY", "UNAUTHENTICATED", "401", "403"]):
                st.info("💡 **Tip**: Check that your Gemini API key is valid. You can generate a free key at [Google AI Studio](https://aistudio.google.com/).")
            elif "404" in err_msg or "not found" in err_msg.lower():
                st.info("💡 **Tip**: The selected model may no longer be available. Try selecting `gemini-2.5-flash` in the sidebar.")
            elif "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                st.info("💡 **Tip**: API rate limit or quota exceeded. Please wait a moment before trying again.")
