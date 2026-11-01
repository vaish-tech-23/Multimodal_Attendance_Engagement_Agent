# 🎓 Multimodal Attendance & Engagement Agent

A modern smart classroom web application that automates student attendance tracking, monitors multimodal engagement indicators (head pose orientation, movement, inactivity), and generates real-time pedagogical AI teaching suggestions.

> [!NOTE]
> **DEMO MODE ACTIVE:** To ensure a stable, reliable, and submission-ready course completion project on Windows 11 with Python 3.13, multimodal computer vision and audio telemetry are demonstrated with realistic classroom data. The application uses a robust, zero-conflict Python Flask and SQLite architecture without external API keys or heavy compilation dependencies.

---

## 📸 Screenshots & Interface Overview

### 1. Classroom Overview Dashboard
Visualizes key classroom metrics at a glance, including total enrollment, real-time attendance rate, average engagement index, and active session status with interactive Chart.js graphs.
```text
+-----------------------------------------------------------------------------------+
| [DEMO MODE ACTIVE] Multimodal computer vision & audio analysis are simulated...   |
+-----------------------------------------------------------------------------------+
|  🎓 Multimodal Agent   [Dashboard]  [Attendance]  [Engagement]  [AI Suggestions]  |
+-----------------------------------------------------------------------------------+
|  [👥 Total: 8]   [✅ Attendance: 100%]   [🎯 Avg Focus: 78.5%]   [⚡ Status: Active] |
|                                                                                   |
|  +------------------------------+     +----------------------------------------+  |
|  | Attendance Distribution      |     | Multimodal Engagement Profile          |  |
|  | (Present / Late / Absent)    |     | (High / Moderate / Low Attention Bars) |  |
|  +------------------------------+     +----------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### 2. Live Attendance Management (`/attendance`)
Interactive student checklist with one-click **Present**, **Late**, and **Absent** buttons, instant search/filtering by student name or roll number, and a student onboarding form.
```text
+-----------------------------------------------------------------------------------+
|  Classroom Attendance Checklist                       [Search Students: ________] |
+-----------------------------------------------------------------------------------+
|  Student Name     Roll No      Department       Status      Duration   Actions    |
|  Aarav Sharma     CS-2024-001  AI & Data Sci    [Present]   58 mins    [P] [L] [A]|
|  Priya Patel      CS-2024-002  Data Science     [Present]   58 mins    [P] [L] [A]|
|  Rohan Mehta      CS-2024-003  Computer Science [Absent]     0 mins    [P] [L] [A]|
+-----------------------------------------------------------------------------------+
```

### 3. Multimodal Engagement Analysis (`/engagement`)
Features a simulated smart classroom camera HUD overlaying detected faces, 3D head orientations (pitch/yaw), movement indicators, and attention scores.

### 4. Rule-Based AI Teaching Suggestions (`/suggestions`)
Automated pedagogical heuristics that detect classroom focus dips or attendance deficits and provide actionable instructional recommendations.

### 5. Historical Reports & CSV Export (`/reports`)
Complete audit history with timestamped entry/exit logs and a one-click **Download Attendance CSV** button.

*(To add your own browser screenshots to GitHub: save your screenshots into a `docs/screenshots/` folder and link them as `![Dashboard](docs/screenshots/dashboard.png)`).*

---

## 🌟 Key Application Features

1. **Automated Attendance & Sustained Presence**
   - Live checklist with instant status toggling (**Present**, **Late**, **Absent**).
   - Sustained presence detection logic (verifying that participants remain present for required intervals, e.g. 45+ minutes).
   - Instant client-side search filter by name or student ID without page reloads.

2. **Multimodal Engagement Analysis**
   - **Simulated Live Vision Monitor:** Simulated classroom camera HUD with real-time clock, bounding boxes, and attention telemetry.
   - **3D Head Orientation Estimation:** Attentive (Forward), Looking Down (Device/Notes), Looking Away.
   - **Movement & Activity Tracking:** Classifies physical motion (Optimal, Normal, Inactive).
   - **Inactivity Alerts:** Flags prolonged static posture.

3. **Rule-Based AI Teaching Suggestions**
   - **Rule #1 (Attendance Deficit):** Triggers when attendance dips below 75%; recommends sharing lecture recordings and recap notes.
   - **Rule #2 (Engagement Dip):** Alerts when attention falls below 70%; suggests a 2-minute quick quiz or breakout prompt.
   - **Rule #3 (Optimal Focus Window):** Identifies peak attention windows (>85%) to deliver complex theoretical syllabus concepts.
   - **Rule #4 (Inactivity Posture):** Detects static or head-down participants and prompts verbal check-ins.
   - **Dynamic Evaluation Button:** Instructor can re-run rule checks at any moment.

4. **Auditing & CSV Data Export**
   - Full date-filtered attendance audit logs.
   - Instant one-click CSV file generation and browser download.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.13.2 & Flask 3.1.3
- **Database:** SQLite3 (thread-safe, built-in, pre-seeded with sample data)
- **Frontend:** HTML5, CSS3 (responsive grid with dark-accented HUD), JavaScript
- **Data Visualization:** Chart.js (CDN-powered Doughnut and Bar charts)
- **Data Export:** Built-in Python `csv` streaming engine
- **Platform:** Windows 11 (64-bit compatible)

---

## 📁 Project Directory Structure

```text
Multimodel_Attendance_Agent/
│
├── .venv/                      # Python 3.13 Virtual Environment (Excluded from Git)
├── .gitignore                  # Git ignore rules for virtualenvs, caches, and secrets
├── app.py                      # Flask entry point and application routes
├── config.py                   # Central settings, database, and folder paths
├── database.py                 # SQLite schema, query helpers, and demo seeder
├── requirements.txt            # Minimal dependency list (Flask>=3.1.0)
├── README.md                   # Complete documentation and setup guide
│
├── static/
│   ├── css/
│   │   └── style.css           # Responsive modern styling & camera HUD design
│   └── js/
│       └── main.js             # Client-side dynamic HUD clock and alerts
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Master layout with navigation and demo banner
│   ├── index.html              # Main dashboard with statistics and Chart.js
│   ├── attendance.html         # Live attendance checklist and student onboarding
│   ├── engagement.html         # Multimodal vision monitor and metrics
│   ├── suggestions.html        # Rule-based AI teaching recommendations
│   └── reports.html            # Historical session logs and CSV export
│
└── tests/
    ├── __init__.py
    └── test_app.py             # Automated test suite (8 passing tests)
```

---

## 🚀 Installation & Setup Instructions (Windows 11)

### 1. Clone or Open the Repository
```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Multimodel_Attendance_Agent
```

### 2. Create and Activate a Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*(If PowerShell displays a script execution policy restriction, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

### 3. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Application
```powershell
python app.py
```

You will see:
```text
============================================================
 Multimodal Attendance & Engagement Agent is running!
 Local URL: http://127.0.0.1:5000
 Press Ctrl+C in this terminal to stop the server.
============================================================
```

### 5. Access the Web Dashboard
Open your web browser (Chrome, Edge, Firefox) and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Running Automated Tests

To run the unit and integration test suite:
```powershell
python -m unittest discover tests
```
*Expected output: `Ran 8 tests in 0.3s — OK`*

---

## 🔒 Security & Privacy

- No passwords, tokens, or external API keys are committed or exposed.
- All database files (`*.db`), virtual environments (`.venv`), and temporary runtime caches are strictly excluded via `.gitignore`.
