# Synapse: AI Agent for Real-Time Logistics Mediation

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen)](https://synapse-grabhack.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Source%20Code-blue)](https://github.com/aaravsingla/synapse)

---

## 📌 Overview
**Synapse** is an AI-powered coordination agent built with **Google Gemini**, **LangChain-style tool orchestration**, and a **Streamlit frontend**.  
It simulates real-time decision-making for logistics platforms like **Grab** (GrabFood, GrabMart, GrabExpress, GrabCar), handling disruptions such as overloaded restaurants, packaging disputes, unavailable recipients, and traffic incidents.  

The system demonstrates **how LLM-driven agents can mediate, plan, and resolve last-mile delivery conflicts autonomously**, while ensuring **safety via a confidence & policy layer**.

---

## 🚀 Key Features
- ✅ **Streamlit Frontend** – Interactive web UI to run scenarios and visualize outcomes.  
- ✅ **Preprogrammed Issues** – Includes scenarios like *Overloaded Restaurant* and *Damaged Packaging*.  
- ✅ **Custom Issues** – Users can type in new logistics issues (e.g., “traffic jam near airport”, “customer unavailable”) and the agent responds dynamically.  
- ✅ **Policy & Confidence Layer** – Each tool call is evaluated for confidence; risky steps trigger escalation or conservative fallback actions.  
- ✅ **Trace Logging** – Step-by-step agent reasoning, tool calls, observations, and final plan are logged for transparency.  
- ✅ **Deployment Ready** – Runs locally with Python/Streamlit or directly in the cloud via Streamlit Sharing.  

---

## 🖥️ Demo
🔗 Live Streamlit App: [https://synapse-grabhack.streamlit.app/](https://synapse-grabhack.streamlit.app/)  

### Example Scenarios
- **Overloaded Restaurant**  
  - Detects 40-min prep delay  
  - Notifies customer with voucher  
  - Re-routes driver to short task nearby  
  - Suggests alternative merchants  

- **Damaged Packaging**  
  - Triggers mediation flow  
  - Collects photo evidence from customer & driver  
  - Analyzes fault → refund to customer, exoneration for driver  
  - Logs packaging feedback to merchant  

---

## 🏗️ System Architecture
User (Streamlit UI) ─► Scenario (JSON / Custom Text) ─►
Agent Runner ─► Gemini LLM ─► Tools (Simulated APIs) ─► Policy Layer ─► Response

markdown
Copy
Edit

- **Frontend:** Streamlit  
- **Agent Core:** Gemini API (`google-genai`)  
- **Tools:** Python functions simulating logistics APIs  
- **Policy Module:** Confidence estimation, escalation rules  
- **Deployment:** GitHub + Streamlit Cloud  

---

## 📂 Project Structure
synapse/
├─ agents/
│ ├─ agent_runner.py # Core loop, LLM + tools + policy
├─ tools/
│ ├─ simulated_tools.py # Simulated logistics API tools
│ ├─ policy.py # Confidence & escalation logic
├─ scenarios/
│ ├─ overloaded_restaurant.json
│ ├─ damaged_packaging.json
├─ logs/ # Run traces
├─ app.py # Streamlit frontend
├─ cli.py # Command-line interface
├─ requirements.txt
├─ runtime.txt
└─ README.md

yaml
Copy
Edit

---

## ⚙️ Installation & Running Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/aaravsingla/synapse.git
cd synapse
2️⃣ Setup Python Environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # on Windows
# or source venv/bin/activate on Mac/Linux
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Configure API Key
Create a .streamlit/secrets.toml file inside the project folder:

toml
Copy
Edit
GEMINI_API_KEY = "your_api_key_here"
GOOGLE_API_KEY = "your_api_key_here"
5️⃣ Run the App
bash
Copy
Edit
streamlit run app.py
Then open http://localhost:8501 in your browser.

📖 Usage
From the Streamlit UI:

Pick a preprogrammed scenario (Overloaded Restaurant, Damaged Packaging)

OR enter your own Custom Issue in plain English

View the step-by-step reasoning, tool calls, and final resolution plan

From the CLI:

bash
Copy
Edit
python cli.py --scenario scenarios/overloaded_restaurant.json
🔮 Future Improvements
Integration with real APIs (traffic, Grab merchant systems)

Multi-agent coordination (e.g., customer agent + driver agent + merchant agent)

Richer visualizations in Streamlit (timeline view, confidence graphs)

Advanced escalation strategies with reinforcement learning

📎 Links
🌐 Live Demo: https://synapse-grabhack.streamlit.app/

💻 GitHub Repo: https://github.com/aaravsingla/synapse

✨ Acknowledgements
Built with ❤️ using Streamlit + Google Gemini for the Grab Project Synapse Challenge.

yaml
Copy
Edit

---

This README is **submission-ready** (professional, self-contained).  
👉 Do you want me to also generate a **shorter polished 2–3 page 
