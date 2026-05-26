from fastapi import status
from core.models import Users, RefreshToken


# -----------------------------
# SIGN UP TESTS
# -----------------------------

def test_sign_up_user_201(anon_client, db_session):
    payload = {
        "username": "newuser",
        "email": "newuser@test.com",
        "password": "123456",
        "confirm_password": "123456"
    }

    response = anon_client.post("/user/sign-up", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["username"] == payload["username"]
    assert "id" in data

    # verify user exists in db
    user = db_session.query(Users).filter_by(
        username=payload["username"]
    ).first()

    assert user is not None
    assert user.email == payload["email"]


def test_sign_up_existing_user_409(anon_client):
    payload = {
        "username": "testuser",  # already exists from fixture
        "email": "test@test.com",
        "password": "123456",
        "confirm_password": "123456"
    }

    response = anon_client.post("/user/sign-up", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "This username is already exists"


# -----------------------------
# LOGIN TESTS
# -----------------------------

def test_login_200(anon_client, db_session):
    payload = {
        "username": "testuser",
        "password": "12345"
    }

    response = anon_client.post(
        "/user/login",
        data=payload  # IMPORTANT: OAuth2PasswordRequestForm uses form-data
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "Bearer"

    # verify refresh token stored in DB
    user = db_session.query(Users).filter_by(
        username="testuser"
    ).first()

    refresh_token = db_session.query(RefreshToken).filter_by(
        user_id=user.id
    ).first()

    assert refresh_token is not None

    # verify cookie exists
    assert "refresh_token" in response.cookies


def test_login_invalid_password_401(anon_client):
    payload = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    response = anon_client.post(
        "/user/login",
        data=payload
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_invalid_username_401(anon_client):
    payload = {
        "username": "unknownuser",
        "password": "12345"
    }

    response = anon_client.post(
        "/user/login",
        data=payload
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED