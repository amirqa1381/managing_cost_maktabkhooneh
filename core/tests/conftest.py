import pytest
from faker import Faker
from fastapi.testclient import TestClient
from core.database_test import Base, create_engine, sessionmaker, get_db
from sqlalchemy.pool import StaticPool
from core.main import app
from core.models import Users, Costs
from core.jwt_auth import create_access_token


fake = Faker()


SQLALCHEMY_DATABASE_URL =  "sqlite:///:memory"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

testSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="package")
def db_session():
    db = testSessionLocal()
    try:
        yield db

    finally:
        db.close()


@pytest.fixture(scope="session") 
def tear_up_and_down_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    
    
    
@pytest.fixture(scope="function")
def override_dependencies(db_session, tear_up_and_down_database):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)
    

@pytest.fixture(scope="function")
def anon_client(override_dependencies):
    client = TestClient(app)
    yield client
    

@pytest.fixture(scope="function")
def auth_client(db_session,override_dependencies):
    client = TestClient(app)
    # here we retrieve the user from the DB
    user = db_session.query(Users).filter_by(username="testuser").one()
    # here we create a access token base on the user that we get
    access_token = create_access_token(user.username)
    # here we update the headers base on the access token that we created
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client


@pytest.fixture(scope="package", autouse=True)
def generate_mock_data(db_session):
    # Clear tables before populating
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
    
    # creating the user 
    user = Users(username="testuser", email="testuser@example.com")
    user.set_password("12345")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    print(f"user was created with username: {user.username} and ID: {user.id}")
    
    costs_list = []
    for _ in range(10):
        costs_list.append(
            Costs(
                user_id=user.id,
                description=fake.text(),
                amount=fake.pydecimal(left_digits=4, right_digits=2, positive=True)
            )
        )
    
    db_session.add_all(costs_list)
    db_session.commit()
    print(f"added 10 task for user_id : {user.id}")
    
    


