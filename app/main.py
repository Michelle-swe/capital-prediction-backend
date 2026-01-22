from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .utils import create_user,verify_user,predict_capital
from .auth import get_current_user
import warnings
from dotenv import load_dotenv
load_dotenv()
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')



# Create database tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Noble Apartments API")



@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "Noble Apartments API",
        "version": "1.0.0",
        
    }


# Jwt authentication


@app.post("/user/register", status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    email:  unique
    password: hashed)
    """
    return create_user(db, user_data)

@app.post("/user/login", response_model=schemas.LoginResponse, status_code=status.HTTP_200_OK)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login and receive JWT token
    JWT token valid for 24 hours
    """
    return verify_user(db,user_credentials)


@app.post("/predict-capital", response_model=schemas.CapitalResponse, status_code=status.HTTP_200_OK)
def capital_prediction(data: schemas.CapitalInput, 
                  current_user: models.User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    """ predict capital based on year""" 
    return predict_capital(data)
        
        