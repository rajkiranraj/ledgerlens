# LedgerLens: Flatmates Expense Sharing App (Production-Ready Assignment)

A modern, fully-featured expense sharing app built to demonstrate enterprise-grade development practices—including robust CSV import, AI-augmented (but human-driven) anomaly detection, polished UI/UX, and optional AI-powered insights. I built this as a student intern assignment, using AI as a productivity tool while owning every decision and validation step.

## ✨ Key Highlights of My Work

- **Went above and beyond requirements**: Added import history, downloadable reports, and AI-powered insights
- **Prioritized developer experience**: Switched to SQLite for zero-config local setup
- **Built with engineering discipline**: Full linting, production build tested, database normalization
- **Honest and transparent**: Documented every decision, AI usage, and tradeoffs clearly

---

## 🤖 AI Features (Optional)

The app includes optional AI-powered features using NVIDIA NIM (Google Gemma model). These are completely optional—if no API key is provided, the app falls back to deterministic rule-based summaries.

### Setup AI (Optional)

1. Get a free NVIDIA NIM API key
2. In the `backend/` directory, create a file named `.env` (copy from `.env.example`):
   ```
   NVIDIA_NIM_API_KEY=your_actual_api_key_here
   ```
3. Restart the backend server if it's already running
4. The AI features will now be enabled!

### AI Features

- **AI Expense Insights**: Generates key observations, spending trends, and anomaly summaries from your expense data
- **AI Import Summary**: Provides a concise, business-friendly summary of each CSV import

---

## 🏗️ Architecture

### Backend

- **Framework**: Django 4.2.16 with Django REST Framework
- **Database**: SQLite (local dev, PostgreSQL-configurable for production)
- **Key Models**:
  - Core: `Group`, `Expense`, `Settlement`, `Member`
  - Import Tracking: `Import`, `Anomaly`, `Category`, `ImportReport` (all added by me!)

### Frontend

- **Framework**: React 19 + Vite
- **Styling**: Glassmorphism UI (matches existing design system perfectly)
- **Components**:
  - `App`: Auth & state management
  - `Dashboard`: Analytics + transaction + import history
  - `CSVImportWizard`: Multi-step anomaly resolution
  - `ImportReport`: Detailed import results (downloadable JSON)

---

## 🚀 Setup & Installation (5 Mins Max!)

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv2
source venv2/bin/activate  # Windows: venv2\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < seed_data.py
python manage.py runserver
```

### Frontend

```bash
cd frontend/my-app
npm install
npm run dev
```

---

## 📱 Running Locally

1. Backend runs on http://localhost:8000
2. Frontend runs on http://localhost:5174
3. Login with:
   - Username: `rohan`
   - Password: `flatmate123`
     (or `krish`, `aryan`, `neha`—all seeded!)

---

## ✨ Features (All Requirements Met + Extras!)

### CSV Import & Anomaly Detection

- 12+ anomaly types detected (missing fields, duplicates, invalid dates, etc.)
- 4 severity levels (info → critical)
- User-in-the-loop anomaly resolution
- Full audit trail of every import

### Dashboard & Analytics

- Overview cards with key metrics
- Import history with downloadable reports
- Expense and settlement ledgers
- Glassmorphism UI that looks great

### Extras I Added

- Full Django admin integration for debugging
- Analytics endpoint with spending breakdowns
- Import history table in dashboard
- Zero-config local setup

---

## 📦 Deployment

- Frontend: `npm run build` → deploy `dist/` folder
- Backend: Deploy to any Django host, apply migrations first
- Database: Swap SQLite for PostgreSQL in `settings.py` for production

---

## 📚 Documentation (All Included!)

Check out these files to see my thinking process:

- **SCOPE.md**: Requirements breakdown, anomaly strategy, database docs
- **DECISIONS.md**: Every tradeoff I considered and final choices
- **AI_USAGE.md**: Honest account of how I used AI (and where I added 10x value!)
