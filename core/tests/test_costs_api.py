from fastapi import status
from core.models import Costs

def test_cost_list_response_401(anon_client):
    response = anon_client.get("/costs")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    

def test_cost_list_response_200(auth_client):
    response = auth_client.get("/costs")
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10
    


def test_get_specific_cost_200(auth_client, db_session):
    
    cost = db_session.query(Costs).first()

    response = auth_client.get(f"/costs/{cost.id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == cost.id
    assert data["description"] == cost.description
    assert float(data["amount"]) == float(cost.amount)
    


def test_get_specific_cost_404(auth_client):
    response = auth_client.get("/costs/99999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    

def test_get_specific_cost_401(anon_client):
    response = anon_client.get("/costs/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED