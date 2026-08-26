from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated

from app.database.session import get_db
from app.database.models import User
from app.auth.hashing import verify_password
from app.auth.jwt import create_access_token

router = APIRouter(tags=['login'])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

@router.post('/login', response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    verified, updated_pass_hash = verify_password(form_data.password, user.hashed_password)

    if not user or not verified:
        raise HTTPException(status_code=401, detail='Invalid username or password.')

    if updated_pass_hash:
        user.hashed_password=updated_pass_hash
        db.commit()
        db.refresh(user)

    token = create_access_token(user_id=user.id, username=user.username)
    return TokenResponse(access_token=token)

