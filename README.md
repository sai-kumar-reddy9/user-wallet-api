# Wallet API (FastAPI)

A simple FastAPI service with Swagger docs to manage users, their wallet balances, and transactions.

## Features
- **List Users API** – `GET /users`: Returns name, email, phone, and wallet balance for all users.
- **Update Wallet API** – `POST /wallet/{user_id}`: Add to the wallet or set an absolute balance. Records a transaction.
- **Fetch Transactions API** – `GET /users/{user_id}/transactions`: Returns all transactions for a user.
- Auto-creates a SQLite DB and seeds 3 sample users.
- Interactive docs at **`/docs`** (Swagger) and **`/redoc`**.

## Quickstart (Local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open: http://127.0.0.1:8000/docs

## API Examples

### List Users
```bash
curl http://127.0.0.1:8000/users
```

### Update Wallet (add mode)
```bash
curl -X POST "http://127.0.0.1:8000/wallet/1" -H "Content-Type: application/json" -d '{ "mode": "add", "amount": 250.75, "description": "Top-up" }'
```

### Update Wallet (set mode)
```bash
curl -X POST "http://127.0.0.1:8000/wallet/1" -H "Content-Type: application/json" -d '{ "mode": "set", "amount": 1000 }'
```

### Fetch Transactions
```bash
curl http://127.0.0.1:8000/users/1/transactions
```

## Docker
```bash
docker build -t wallet-api .
docker run -p 8000:8000 wallet-api
```

## Project Structure
```
app/
  __init__.py
  config.py
  database.py
  main.py
  models.py
  schemas.py
  seed.py
```

## Notes / Assumptions
- `POST /wallet/{user_id}` supports two modes:
  - `add`: adds (positive) or subtracts (negative) from current balance.
  - `set`: sets the absolute balance; a transaction is recorded for the difference.
- Negative balances are allowed; add validation as needed.
- For production, consider Alembic migrations and a managed database.

## Deployment (Render/railway/EC2 - outline)
1. Set `DATABASE_URL` via env (defaults to `sqlite:///./wallet.db`).
2. Run `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

## Extra Credit (Hosting)
- You can deploy to Render/Railway/Fly.io/EC2. This app needs only Python 3.11+.
- Health check: `GET /users`.
- Swagger UI: `/docs`.
```
