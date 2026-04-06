# 🧠 Opportunity Trust Intelligence Network

### A smart helper that reads suspicious job messages and warns you before you lose money.

---

## 👋 Hello! What is this project?
Imagine your friend gets a message like this:

"Congratulations! You got selected for an internship. Pay a registration fee now."

It sounds exciting, but it may be a scam.

This project helps people check such messages quickly. It gives a **Trust Score** from 0 to 100:
- **Higher score** = message looks safer
- **Lower score** = message looks risky

---

## 🚨 Problem Statement
Today many students and job seekers receive fake messages like:
- "Pay fee now to confirm interview"
- "Send money to this UPI to join internship"
- "Urgent! Last chance!"

These scams can:
- steal money
- steal personal details
- waste time and confidence

Many people, especially beginners, cannot easily identify these fake messages.

So the real problem is:
**How can we quickly detect scam-like job/internship messages in a simple way?**

---

## 💡 Solution (Our Idea)
We built a simple web app where a user:
1. pastes a suspicious message
2. clicks analyze
3. sees a trust score, risk level, and explanation
4. sees graph-based complaint connection data from TigerGraph

In very simple words:
- We check risky words in text
- We detect UPI IDs
- We check complaint links from a graph database
- We combine all clues and generate a final score

This makes scam detection easier even for a beginner.

---

## 🎯 Key Features
- **Simple message input**
: Paste any job/internship text and analyze instantly.

- **Trust Score (0-100)**
: Easy number that tells how safe or risky a message looks.

- **Risk label (Low / Medium / High)**
: Quick decision help for non-technical users.

- **UPI extraction**
: Detects UPI IDs like `name@upi` directly from text.

- **TigerGraph complaint check**
: Checks if that UPI is connected with complaint records.

- **Visual graph preview**
: Shows node connections so users can understand risk relationships.

- **Beginner-friendly UI**
: Clean pages for Home, How It Works, Analyze, and Graph Preview.

---

## 🖼️ Screenshots

### Landing Page
![Landing Page](Screenshot 2026-04-06 125449.png)

*Figure 1: Home screen where the user starts analysis.*

### How It Works Page
![How It Works](Screenshot 2026-04-06 125852.png)

*Figure 2: Simple flow of input -> processing -> graph check -> trust score output.*

### Analyze + Result Page
![Analyze Result](Screenshot 2026-04-06 130051.png)

*Figure 3: User enters suspicious message and gets trust score, risk, and explanation.*

### Risk Explanation + Graph Section
![Risk and Graph Section](Screenshot 2026-04-06 130112.png)

*Figure 4: Detailed risk reasons and graph preview for the detected UPI.*

### Graph Preview Page
![Graph Preview](Screenshot 2026-04-06 130022.png)

*Figure 5: Graph data card with UPI-centered connection summary.*

### TigerGraph Explore View (Backend Graph Source)
![TigerGraph Explore](Screenshot 2026-03-31 225250.png)

*Figure 6: Actual graph structure in TigerGraph used by the project.*

---

## 🏗️ How It Works (Step-by-Step)

### Step 1: User inputs message
The user pastes a suspicious job or internship message.

Example:
"Urgent! Pay registration fee now to confirm internship slot."

### Step 2: AI-like text processing
Backend checks risky clues such as:
- urgency words (urgent, now, immediately)
- payment words (fee, deposit, transfer)
- suspicious offer patterns
- UPI handles

### Step 3: Graph relationship check
If a UPI is found, backend asks TigerGraph:
- How many complaints are linked to this UPI?
- Which companies are connected with this UPI?

### Step 4: Trust score generation
All signals are combined.
Then app shows:
- Trust Score
- Risk Level
- Explanation bullets
- Graph Preview

---

## 🧩 System Architecture

### Components in simple words
- **Frontend (React + Vite)**
: What user sees and clicks.

- **Backend (Flask API)**
: Brain of the app, receives message and calculates score.

- **AI logic (Rule-based scoring)**
: Detects suspicious patterns from text.

- **Graph Database (TigerGraph)**
: Stores complaint links between UPI and company nodes.

### Architecture Diagram (Simple)
```text
User Message
    |
    v
Frontend (React)
    |
    v
Backend API (Flask)
    |            \
    |             \--> Text Risk Analyzer (rules)
    |
    +--> TigerGraph Query (complaints + links)
                    |
                    v
         Combined Trust Score + Explanation
                    |
                    v
           UI Result + Graph Preview
```

---

## 📊 Graph Explanation (VERY IMPORTANT)
Think of graph like a **social network**, but for scam signals.

### Node types
- **Company node**
: A company name appearing in suspicious messages.

- **UPI node**
: Payment handle used in messages, like `scam@upi`.

- **Complaint node**
: A complaint record raised by victims.

### Edge (connection) meaning
- **Complaint -> UPI**
: This UPI was reported in a complaint.

- **Complaint -> Company**
: This company name appeared in that complaint.

- **Company -> UPI (derived/linked)**
: The app can show possible relation if found in graph response.

### Easy analogy
Like Instagram friends graph:
- people are nodes
- follows are edges

Here:
- company / upi / complaint are nodes
- suspicious links are edges

More links + more complaints = more risk.

---

## 🛠️ Tech Stack
- **React**
: Builds webpage screens.

- **Vite**
: Runs React fast during development.

- **Flask (Python)**
: Backend API server.

- **Python regex + logic rules**
: Finds UPI and suspicious patterns.

- **TigerGraph**
: Graph database for relationship checks.

- **REST API**
: Backend talks to TigerGraph using HTTP calls.

- **CSS**
: Styling for dark modern UI.

---

## ⚙️ Installation Guide (VERY SIMPLE)

## 0) Things you need first
- Python installed
- Node.js installed
- Git installed

## 1) Clone the project
```powershell
git clone <your-repo-url>
cd "Opportunity Trust"
```

## 2) Backend setup
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file inside `backend/` using this template:
```env
TIGERGRAPH_HOST=https://<your-tigergraph-host>
TIGERGRAPH_GRAPH_NAME=OpportunityTrust_Graph
TIGERGRAPH_TOKEN=<your-token>
TIGERGRAPH_QUERY_NAME=find_complaints_by_upi
TG_UPI_PARAM_NAME=input_upi
```

Run backend:
```powershell
python app.py
```
Backend starts at: `http://127.0.0.1:5000`

## 3) Frontend setup
Open a new terminal:
```powershell
cd frontend
npm install
npm run dev
```
Frontend starts at: `http://localhost:5173`

## 4) Use app
- Open browser at frontend URL
- Go to Analyze page
- Paste message
- Click Analyze Message

---

## 🧪 Example Inputs & Outputs

### Example 1 (High Risk)
**Input**
```text
Urgent requirement! Congratulations on your selection for internship.
Pay registration fee immediately to scam@upi.
```

**Expected Output (approx)**
- Trust Score: 10-30
- Risk: High
- Reason: urgency + money request + suspicious UPI

### Example 2 (Medium Risk)
**Input**
```text
SkillGrow training program. Refundable deposit required to begin.
Send it to fake@upi.
```

**Expected Output (approx)**
- Trust Score: 40-55
- Risk: Medium/High boundary
- Reason: deposit + payment handle + scam-like onboarding

### Example 3 (Safer Message)
**Input**
```text
We are hiring interns. Apply through official careers portal.
No payment is required.
```

**Expected Output (approx)**
- Trust Score: 75-95
- Risk: Low
- Reason: no payment demand, normal hiring flow

---

## 🚀 Future Improvements
- Add real NLP/LLM model for smarter language understanding
- Real-time complaint feed integration
- Multi-language scam detection (Hindi + English + regional)
- One-click report button for suspicious messages
- Auto-learning from user feedback
- Stronger visual graph with interactive nodes and filters

---

## 🏆 Why This Project is Powerful
- Protects students and freshers from fake internships
- Converts confusing text into simple risk score
- Uses graph intelligence, not only keyword matching
- Beginner-friendly design makes cybersecurity awareness easy
- Can be expanded into a real public safety product

In one line:
**This project turns scam confusion into clear action.**

---

## 🙌 Team / Credits
Built as a hackathon project by the Opportunity Trust team.

Special thanks:
- TigerGraph platform for graph infrastructure
- Open-source ecosystem (React, Flask, Python)

---

## 📁 Project Structure (Quick View)
```text
Opportunity Trust/
├── backend/
│   ├── app.py
│   ├── logic.py
│   ├── tigergraph.py
│   ├── utils.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── README.md
├── LICENSE
└── .gitignore
```

---

## ✅ License
This project uses the MIT License.
See the `LICENSE` file for details.
