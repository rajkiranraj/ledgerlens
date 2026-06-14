# Contributing to LedgerLens

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `cd backend && python manage.py test && cd ../frontend/my-app && npm run lint`
5. Commit your changes: `git commit -m "feat: add amazing feature"`
6. Push to your branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Code Style

- Backend: Follow PEP 8 guidelines
- Frontend: Use ESLint configured in frontend/my-app/eslint.config.js
- Use meaningful commit messages following conventional commits:
  - feat: new feature
  - fix: bug fix
  - docs: documentation changes
  - refactor: code refactor
  - test: test additions
  - chore: maintenance tasks

## Development Setup

Follow the setup instructions in README.md.

## Pull Request Process

1. Ensure your changes don't break any existing functionality
2. Update documentation as needed
3. Link your PR to any related issues
4. Request a review from a maintainer
