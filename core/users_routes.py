from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database_test import get_db
from schemas import UserRegisterSchema, UserLoginSchema
from models import Users, RefreshToken
from jwt_auth import access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up_user(request: UserRegisterSchema, db: Session = Depends(get_db)):
    """
    Method for signing up the user and if the user signed up in the past we bring back the error to it
    """

    user = db.query(Users).filter_by(username=request.username).first()

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is already exists",
        )

    new_user = Users(username=request.username, email=request.email)
    new_user.set_password(request.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(content={"id": new_user.id, "username": new_user.username})


@router.post("/login", status_code=status.HTTP_200_OK)
async def loin(
    response: Response,
    request: OAuth2PasswordRequestForm,
    db: Session = Depends(get_db),
):
    """
    function for login the user
    """

    user = db.query(Users).filter_by(username=request.username).first()

    if not user or not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # create the refresh token
    refresh = create_refresh_token(str(user.username))

    # store refresh token in DB
    db_token = RefreshToken(user_id=user.id, token=refresh)
    db.add(db_token)
    db.commit()

    # set cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    # return access token
    return {"access_token": access_token(str(user.username)), "token_type": "Bearer"}


@router.post("/refresh")
def refresh_token(
    response: Response, refresh_token: str = Cookie(None), db: Session = Depends(get_db)
):
    # if refresh token exists we can handle it and decode it
    # without the refresh token we get the server error
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    # decode and validate
    payload = decode_token(refresh_token, "refresh")
    username = payload["sub"]

    stored = (
        db.query(RefreshToken).filter_by(token=refresh_token, revoked=False).first()
    )
    if not stored:
        raise HTTPException(401, "Refresh token invalid or revoked")

    # here we revoked the old token
    stored.revoked = True  # type: ignore

    # create new refresh token
    new_refresh = create_refresh_token(username)
    db.add(RefreshToken(user_id=stored.user_id, token=new_refresh))
    db.commit()

    # update cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return {"access_token": access_token(username), "token_type": "Bearer"}


@router.post("/logout")
def logout(
    response: Response, refresh_token: str = Cookie(None), db: Session = Depends(get_db)
):
    if refresh_token:
        stored = db.query(RefreshToken).filter_by(token=refresh_token).first()
        if stored:
            stored.revoked = True  # type: ignore
            db.commit()

    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
