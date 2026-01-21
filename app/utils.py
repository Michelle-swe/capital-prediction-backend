
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models
from .auth import create_access_token
import os
import hashlib
import base64
import numpy as np
import joblib

# ============================================
# USER LOGIC
# ============================================
def create_user(db: Session, user_data): 
        # Check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    hashed_password = hash_password(user_data.password)
    new_user = models.User(
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "created_at": new_user.created_at
        }
    }

def verify_user(db:Session, user_credentials):
    # Find user
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email
    ).first()
    
    # Verify credentials
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT token
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


# ============================================
# PASSWORD HASHING
# ============================================
def hash_password(password: str) -> str:
    """Hash password using PBKDF2"""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        200_000
    )
    return base64.b64encode(salt + key).decode()


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash"""
    decoded = base64.b64decode(stored_hash.encode())
    salt = decoded[:16]
    stored_key = decoded[16:]

    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        200_000
    )

    return new_key == stored_key

# ============================================
# ENDPOINT LOGIC
# ============================================
def predict_capital(data):
    model = joblib.load("Income_model.pkl.gz")
    try:
        # Convert input to array for model
        features = np.array([[data.year]]) 
        capital = model.predict(features)[0]
        capital= max(0, capital) # Ensure non-negative price
        return {"capital": float(capital)} 
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
    