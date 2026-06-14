# LedgerLens: Flatmates Expense Sharing App

A modern, fully-featured expense sharing application built with Django and React.

## Badges

[![CI](https://github.com/rajkiranraj/ledgerlens/actions/workflows/ci.yml/badge.svg)](https://github.com/rajkiranraj/ledgerlens/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-19-blue.svg)](https://react.dev/)

## Key Features

- Core expense sharing functionality with balance calculation and debt minimization
- Comprehensive CSV import with advanced anomaly detection
- Import report generation and download
- AI-powered insights and summaries using NVIDIA NIM (optional)
- Dashboard with analytics and transaction history
- Glassmorphism UI with polished design
- Zero-config SQLite local setup (PostgreSQL configurable for production)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rajkiranraj/ledgerlens.git
   cd ledgerlens
   ```

2. Backend Setup:

   ```bash
   cd backend
   python -m venv venv2
   source venv2/bin/activate  # On Windows: venv2\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py shell < seed_data.py
   python manage.py runserver
   ```

3. Frontend Setup:

   ```bash
   cd frontend/my-app
   npm install
   npm run dev
   ```

4. Access the app at http://localhost:5174 and log in with:
   - Username: rohan
   - Password: flatmate123

### Optional AI Setup

1. Get an NVIDIA NIM API key
2. Create a `.env` file in the backend directory:
   ```
   NVIDIA_NIM_API_KEY=your_api_key_here
   ```
3. Restart the backend server

### Troubleshooting

- If the backend won't start, ensure you have the correct Python version and virtual environment activated
- If the frontend won't start, check that Node.js is installed and dependencies are installed with `npm install`
- For database issues, try running `python manage.py migrate` again
- If you encounter port conflicts, change the backend port with `python manage.py runserver 8001`

## AI Features (Optional)

The app includes optional AI-powered features using NVIDIA NIM. These are completely optional—if no API key is provided, the app falls back to deterministic rule-based summaries.

- AI Expense Insights: Generates key observations, spending trends, and anomaly summaries
- AI Import Summary: Provides a concise, business-friendly summary of each CSV import

## Documentation

- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Key Decisions](docs/DECISIONS.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Change Log](CHANGELOG.md)
- [TODO List](TODO.md)
- [AI Usage](AI_USAGE.md)
- [Scope](SCOPE.md)

## Roadmap

- [ ] Add visual charts to dashboard (spending by category, monthly trends)
- [ ] Implement user profile management
- [ ] Add email notifications for settlements
- [ ] Support for multiple currencies with automatic conversion
- [ ] Add export functionality to PDF and Excel
- [ ] Implement data backup and restore
- [ ] Add mobile-responsive optimizations
- [ ] Write comprehensive unit and integration tests
- [ ] Add real-time collaboration features

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django REST Framework for the backend API
- React and Vite for the frontend
- NVIDIA NIM for AI features
- The open-source community for various dependencies and inspiration
