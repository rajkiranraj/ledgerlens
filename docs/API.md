# API Documentation

## Base URL
`http://localhost:8000/api`

## Authentication
Most endpoints require token authentication. Use the login endpoint to get a token.

### Login
- **Endpoint**: `POST /auth/login/`
- **Body**: `{ "username": "...", "password": "..." }`
- **Response**: `{ "token": "...", "user": { ... } }`

## Endpoints

### Groups
- `GET /groups/`: List groups
- `POST /groups/`: Create group

### Expenses
- `GET /groups/<group_id>/expenses/`: List expenses
- `POST /groups/<group_id>/expenses/`: Create expense
- `DELETE /groups/<group_id>/expenses/<expense_id>/`: Delete expense

### Settlements
- `GET /groups/<group_id>/settlements/`: List settlements
- `POST /groups/<group_id>/settlements/`: Create settlement
- `DELETE /groups/<group_id>/settlements/<settlement_id>/`: Delete settlement

### Balances
- `GET /groups/<group_id>/balances/`: Get group balances and minimized debts

### Analytics
- `GET /groups/<group_id>/analytics/`: Get group analytics

### Imports
- `POST /groups/<group_id>/import/parse/`: Parse CSV file
- `POST /groups/<group_id>/import/confirm/`: Confirm and complete import
- `GET /groups/<group_id>/imports/`: List import history
- `GET /groups/<group_id>/imports/<import_id>/report/`: Get import report
- `POST /groups/<group_id>/ai/insights/`: Generate AI insights
- `POST /groups/<group_id>/ai/import-summary/<import_id>/`: Generate AI import summary

### Members
- `GET /groups/<group_id>/members/`: List group members
- `POST /groups/<group_id>/members/`: Add group member
