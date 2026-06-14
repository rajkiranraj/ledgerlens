# Architecture

## Overview
LedgerLens is a modern, full-stack expense sharing application built with Django (backend) and React + Vite (frontend).

## Backend Architecture
The backend is a Django REST Framework API with the following structure:

### Core Models
1. Group - Manages flatmate groups
2. User - Standard Django user model
3. Member - Group member information
4. Expense - Shared expense data
5. Settlement - Settlement records between members

### New Models Added
1. Category - Expense categories for validation
2. Import - Tracks CSV import sessions
3. Anomaly - Anomalies detected during import
4. ImportReport - Detailed import results

### API Endpoints
- Auth endpoints
- Group management
- Expense and settlement CRUD
- CSV import pipeline
- Analytics and insights
- AI integration endpoints

### Key Utilities
- `utils.py`: CSV parsing, balance calculation, debt minimization
- `ai_utils.py`: AI integration, fallback logic, prompt engineering

## Frontend Architecture
The frontend is a React single-page application:

### Components
1. App - Root component, auth and state management
2. Dashboard - Main UI, analytics, transaction history
3. CSVImportWizard - Multi-step import process
4. ImportReport - Detailed import results

### Styling
- Glassmorphism UI
- CSS custom properties
- Responsive design

## Database Design
The database is fully normalized with proper foreign key relationships and audit timestamps. For local development, SQLite is used; PostgreSQL is recommended for production.

## Security
- Token-based authentication
- Server-side only AI integration (API keys never exposed)
- Input validation and sanitization
- SQL injection protection via Django ORM
