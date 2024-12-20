from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from fastapi import HTTPException, status, Header
from app.services.passwd import passwd

# Retrieve user profile information with full timestamp details
def get_user_profile(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {
        "name": user.name,
        "email": user.email,
        "sex": user.sex,
        "created_at": user.created_at,       # Registration timestamp
        "updated_at": user.updated_at,       # Last profile update timestamp
        "last_login_at": user.last_login  # Last login timestamp
    }

# Update user profile information
def update_user_profile(db: Session, user_id: int, name: str = None, sex: str = None, password: str = None):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if name is not None:
        user.name = name
    if sex is not None:
        user.sex = sex
    if password is not None:
        user.password = passwd.encrypt(password)
    db.commit()
    db.refresh(user)
    return user
