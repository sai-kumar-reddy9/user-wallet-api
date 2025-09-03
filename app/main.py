from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from decimal import Decimal
from typing import List
from .database import Base, engine, get_db
from .models import User, WalletTransaction
from .schemas import UserOut, WalletUpdateIn, WalletUpdateOut, TxnOut
from .seed import seed_users

app = FastAPI(title="Wallet API", version="1.0.0")

# Create tables on startup and seed demo data
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    with next(get_db()) as db:
        seed_users(db)

@app.get("/users", response_model=List[UserOut], summary="List Users")
def list_users(db: Session = Depends(get_db)):
    users = db.execute(select(User)).scalars().all()
    return users

@app.post("/wallet/{user_id}", response_model=WalletUpdateOut, summary="Update Wallet")
def update_wallet(user_id: int = Path(..., ge=1), data: WalletUpdateIn = None, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.mode == "add":
        delta = Decimal(str(data.amount))
        if delta == 0:
            raise HTTPException(status_code=400, detail="Amount cannot be zero for 'add' mode")
        user.wallet_balance = (user.wallet_balance or Decimal("0")) + delta
        kind = "credit" if delta > 0 else "debit"
        txn = WalletTransaction(user_id=user.id, amount=delta, kind=kind, description=data.description)
        db.add(txn)
        db.add(user)
        db.commit()
        db.refresh(txn)
        return {"user_id": user.id, "new_balance": float(user.wallet_balance), "transaction_id": txn.id, "mode": data.mode}

    elif data.mode == "set":
        new_balance = Decimal(str(data.amount))
        old_balance = user.wallet_balance or Decimal("0")
        delta = new_balance - old_balance
        kind = "credit" if delta >= 0 else "debit"
        txn = WalletTransaction(user_id=user.id, amount=delta, kind=kind, description=data.description or "Set balance")
        user.wallet_balance = new_balance
        db.add(txn)
        db.add(user)
        db.commit()
        db.refresh(txn)
        return {"user_id": user.id, "new_balance": float(user.wallet_balance), "transaction_id": txn.id, "mode": data.mode}
    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

@app.get("/users/{user_id}/transactions", response_model=List[TxnOut], summary="Fetch Transactions")
def fetch_transactions(user_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    txns = db.query(WalletTransaction).filter(WalletTransaction.user_id == user_id).order_by(WalletTransaction.created_at.desc()).all()
    return txns
