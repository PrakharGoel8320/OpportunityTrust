# Opportunity Trust Intelligence Network

A beginner-friendly hackathon project to detect scam job/internship messages using:
- simple AI text checks (rule-based)
- live TigerGraph query

This project has:
- Flask backend API
- React frontend with multi-page UI
- TigerGraph live integration for complaint checks

## Project Structure

- `backend/app.py` : Main Flask API (`/analyze`, `/graph`, `/docs`)
- `backend/utils.py` : Extract company name and UPI id from message
- `backend/tigergraph.py` : Calls TigerGraph REST API query `find_complaints_by_upi`
- `backend/logic.py` : Trust score, risk level, explanation logic
- `backend/.env.example` : Sample environment variables
- `frontend/src/App.jsx` : Main router setup
- `frontend/src/pages/Home.jsx` : Landing page
- `frontend/src/pages/HowItWorks.jsx` : System flow page
- `frontend/src/pages/Analyze.jsx` : Message analysis page
- `frontend/src/pages/GraphPreview.jsx` : TigerGraph preview page
- `frontend/src/components/` : Navbar, input, result, graph components
- `frontend/src/App.css` : Dark theme and animations
- `.gitignore` : GitHub-safe ignore rules

## Backend Setup (Flask)

1. Go to backend folder:
```powershell
cd backend
```

2. Create virtual environment:
```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install packages:
```powershell
pip install -r requirements.txt
```

4. Create `.env` from `.env.example` and fill values:
```env
TIGERGRAPH_HOST=https://<host>
TIGERGRAPH_GRAPH_NAME=<graph_name>
TIGERGRAPH_TOKEN=<bearer_token>
TG_UPI_PARAM_NAME=input_upi
```

5. Run backend:
```powershell
python app.py
```

Backend runs at: `http://localhost:5000`

Useful backend routes:
- `GET /docs`
- `POST /analyze`
- `GET /graph?upi=<upi_id>`

## Frontend Setup (React + Vite)

1. Open new terminal and go to frontend:
```powershell
cd frontend
```

2. Install npm packages:
```powershell
npm install
```

3. Start frontend:
```powershell
npm run dev
```

Frontend runs at: `http://localhost:5173`

Frontend routes:
- `/` (Home)
- `/how-it-works`
- `/analyze`
- `/graph`

## API Usage

### Endpoint
`POST /analyze`

### Request Body
```json
{
  "message": "Hello from ABC Technologies. Pay registration fee now to this UPI: fakejob@upi"
}
```

### Example Response
```json
{
  "input": {
    "message": "Hello from ABC Technologies. Pay registration fee now to this UPI: fakejob@upi",
    "company_name": "ABC Technologies",
    "upi_id": "fakejob@upi"
  },
  "graph_data": {
    "complaint_count": 4,
    "linked_companies": ["ABC Technologies"]
  },
  "trust_score": 0,
  "risk_level": "High",
  "explanation": "UPI has high complaints (4). Company is linked with this UPI in graph data. Message contains payment-related words. Message creates urgency pressure."
}
```

### Graph Endpoint
`GET /graph?upi=scam@upi`

Example response:
```json
{
  "upi_id": "scam@upi",
  "complaint_count": 4,
  "linked_companies": ["ABC Technologies"],
  "nodes": [
    {"id": "scam@upi", "type": "UPI", "label": "scam@upi"},
    {"id": "ABC Technologies", "type": "Company", "label": "ABC Technologies"},
    {"id": "complaints_scam@upi", "type": "Complaint", "label": "Complaints: 4"}
  ],
  "connections": [
    {"from": "ABC Technologies", "to": "scam@upi", "label": "linked_to"},
    {"from": "complaints_scam@upi", "to": "scam@upi", "label": "reported_on"}
  ]
}
```

## Example: TigerGraph API Response Handling

The backend tries both endpoint styles:
- `https://<host>/query/<graph_name>/find_complaints_by_upi`
- `https://<host>/restpp/query/<graph_name>/find_complaints_by_upi`

With header:
`Authorization: Bearer <token>`

In `backend/tigergraph.py`, code:
- reads `results` from TigerGraph JSON
- counts complaint nodes or reads `complaint_count` if returned
- collects company names from fields like `company` or `company_name`
- sends the query parameter `input_upi` to `find_complaints_by_upi`

## GitHub Upload Checklist

1. Keep secrets in `backend/.env` only (never commit this file).
2. Confirm `.gitignore` exists (already added in this project).
3. Run app once before pushing:
  - backend: `python app.py`
  - frontend: `npm run dev`
4. Push these folders/files:
  - `backend/` (except local `.env`)
  - `frontend/` (except `node_modules` and `dist`)
  - `README.md`
  - `.gitignore`

## Trust Score Rules

Start from 100:
- complaints count > 2 -> minus 40
- any company linked to same UPI -> minus 30
- job offer words -> minus 5
- secure internship pitch -> minus 5
- basic details request -> minus 5
- resume and details together -> minus 25
- limited-time offer language -> minus 15
- urgency words in text -> minus 5
- money request linked to a handle -> minus 10
- refundable deposit -> minus 20
- background check fee -> minus 35
- payment words in text -> minus 0
- official payment identity or account words -> minus 10
- handle-like payment address used in a scam combo -> minus 5

Risk level:
- 70 or more = Low
- 40 to 69 = Medium
- below 40 = High
