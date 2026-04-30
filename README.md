# 💠 Core Talent: Intelligent IDP Platform

Core Talent is an enterprise-grade Talent Management and Individual Development Plan (IDP) platform. It leverages predictive analytics, AI-driven coaching, and gamification to bridge the gap between current employee skills and future career aspirations.

---

## 🚀 Key Features

### 🏢 For Admins & HR
*   **🌡️ Workforce Skill Heatmaps**: Visualize skill proficiency and "Knowledge Silos" across different roles.
*   **📦 9-Box Talent Matrix**: Automatically categorize the workforce into Star, Future Star, Expert Professional, etc.
*   **🔮 Succession Planning**: Rank employees by "Readiness Score" for specific future roles.
*   **🤖 Predictive AI**: Monitor Attrition Risk (Flight Risk) and Future Star Probability based on engagement data.
*   **📊 Master Data Sync**: Upload `employees.csv` and `roles.csv` to instantly refresh the organization's talent data.

### 👤 For Employees
*   **🤖 AI Career Coach**: A 24/7 chat partner that provides personalized growth advice based on your skill gaps.
*   **📊 DNA Proficiency Radar**: Visualize your current skills vs. target role requirements in a radar chart.
*   **🚀 Personalized IDP**: Get curated activities, mentorship pairings, and job rotation suggestions.
*   **🏆 Gamified Growth**: Earn levels and badges (e.g., *Leadership Vanguard*, *Technical Architect*) as you complete modules.
*   **📔 Development Journal**: Maintain a collaborative log of reflections and 1-on-1 meeting notes.

---

## 🛠️ Tech Stack
*   **Frontend/UI**: Streamlit (Premium Glassmorphism CSS)
*   **Data Processing**: Pandas, NumPy
*   **Visualizations**: Plotly (Interactive Radar & Heatmaps)
*   **Persistence**: JSON-based local storage for progress, feedback, and journals.

---

## 📥 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Vishal-glitxh/Techathon_IDPs.git
cd Techathon_IDPs
```

### 2. Install Dependencies
Ensure you have Python 3.8+ installed, then run:
```bash
pip install pandas streamlit plotly numpy
```

### 3. Initialize Data
Run the setup script to create the initial data directory and sample CSVs:
```bash
python setup_project.py
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 📂 Project Structure
```text
Techathon_IDPs/
├── app.py                # Main Streamlit UI & Router
├── main.py               # CLI Entry Point
├── setup_project.py      # Environment & Data Initializer
├── data/                 # persistence storage (CSV/JSON)
│   ├── employees.csv     # Master employee data
│   ├── roles.csv         # Target role requirements
│   └── *.json            # Progress, Journal, & Feedback logs
├── src/                  # Core Logic Modules
│   ├── gap_analysis.py   # Skill gap & 9-box calculations
│   ├── predictive.py     # AI Attrition & Potential models
│   └── recommendation.py # Personalized activity engine
└── uploads/              # Evidence files (PDFs/Images)
```

---

## 🔐 Credentials (Demo)
*   **Admin**: User: `admin` | Pass: `admin123`
*   **Employee**: User: `101` (or any ID/Name in CSV) | Pass: `user123`

---

## 🛡️ Robustness Note
The platform is built with **Level 2 Scrutiny** standards:
*   Force-typed string ID handling to prevent mismatch errors.
*   Automatic directory healing for `data/` and `uploads/`.
*   Graceful error boundaries for malformed CSV inputs.

---
Created for the Techathon 2026. Empowering growth, one skill at a time.
