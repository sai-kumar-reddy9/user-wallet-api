# User Wallet API 

A simple wallet API built with **FastAPI**.  
It supports listing users, updating wallet balances, and fetching transaction history.  
Swagger and ReDoc docs are auto-generated for easy testing.

##  Features
- **List Users** – Fetch all users with name, email, phone, and wallet balance.
- **Update Wallet** – Add or set an amount for a user’s wallet.
- **Fetch Transactions** – Retrieve all transactions for a specific user.
- **Interactive API Docs** – Available via Swagger UI and ReDoc.

## Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) – Web framework
- [SQLite + SQLAlchemy](https://www.sqlalchemy.org/) – Database & ORM
- [Uvicorn](https://www.uvicorn.org/) – ASGI server
- [Pydantic](https://docs.pydantic.dev/) – Data validation

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/sai-kumar-reddy9/user-wallet-api.git
cd user-wallet-api
````
### 2. Create a virtual environment
```bash
python -m venv .venv
```
Activate it:
* **Windows (PowerShell):**
  ```bash
  .venv\Scripts\activate
  ```
* **Linux/Mac:**
  ```bash
  source .venv/bin/activate
  ```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the app
```bash
uvicorn app.main:app --reload
```
##  API Documentation
* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
---
## Example API Usage
**List Users**
```http
GET /users
```
**Update Wallet**
```http
POST /wallet/1
{
  "mode": "add",
  "amount": 200,
  "description": "Top-up"
}
```
**Fetch Transactions**
```http
GET /users/1/transactions
```
