from sqlalchemy.orm import Session
from .models import User

SAMPLE_USERS = [
    {"name": "Sai Kumar", "email": "sai@example.com", "phone": "9876543210"},
    {"name": "Bob Singh", "email": "bob@example.com", "phone": "9123456780"},
    {"name": "Chitra Rao", "email": "chitra@example.com", "phone": "9000012345"},
]

def seed_users(db: Session):
    if db.query(User).count() == 0:
        for u in SAMPLE_USERS:
            db.add(User(name=u["name"], email=u["email"], phone=u["phone"], wallet_balance=0))
        db.commit()
