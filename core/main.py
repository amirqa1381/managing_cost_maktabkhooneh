from typing import Annotated
from fastapi import FastAPI, status, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_swagger import patch_fastapi
from core.schemas import CostRead, CostCreate, CostUpdate
from core.models import Costs, Users
from core.database import get_db
from core.users_routes import router as user_routes
from core.jwt_auth import get_current_user
from core.exception_handler import register_exception_handlers
from core.exceptions import ExpenseNotFoundException

app = FastAPI(docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, docs_url="/swagger")

app.include_router(user_routes)


register_exception_handlers(app)
# GET method for getting specific cost or list of costs


@app.get("/costs/{cost_id}", status_code=status.HTTP_200_OK, response_model=CostRead)
def get_specific_cost(cost_id: int, user: Users = Depends(get_current_user),db: Session = Depends(get_db)):
    cost = db.query(Costs).filter_by(id=cost_id, user_id=user.id).one_or_none()

    if cost is None:
        raise ExpenseNotFoundException(cost_id)

    return cost


@app.get("/costs", status_code=status.HTTP_200_OK, response_model=list[CostRead])
def get_all_costs(user: Users = Depends(get_current_user),db: Session = Depends(get_db)):
    """
    function for getting the list of the Costs
    """
    costs = db.query(Costs).filter_by(user_id=user.id).all()
    return costs


# POST method for creating the cost


@app.post("/costs", status_code=status.HTTP_201_CREATED, response_model=CostRead)
async def create_cost(request: CostCreate, user: Users = Depends(get_current_user),db: Session = Depends(get_db)):
    if request.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you don't have any access to create the cost for user with id {request.user_id}")
    new_cost = Costs(**request.model_dump())

    db.add(new_cost)
    db.commit()
    db.refresh(new_cost)

    return new_cost


# PUT method for updating the cost


@app.put("/costs/{cost_id}", status_code=status.HTTP_200_OK, response_model=CostRead)
async def update_specific_cost(
    cost_id: Annotated[int, Path(description="Cost ID to update")],
    request: CostUpdate,
    user: Users = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cost = db.query(Costs).filter_by(id=cost_id).first()

    if not cost:
        raise ExpenseNotFoundException(cost_id)

    # here we update the provided fields
    updated_data = request.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(cost, key, value)

    db.commit()
    db.refresh(cost)

    return cost


# DELETE method for deleting the specific cost


@app.delete("/costs/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_specific_cost(cost_id: int,user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    cost = db.query(Costs).filter_by(id=cost_id).first()

    if not cost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="exciting item does not exist"
        )

    db.delete(cost)
    db.commit()
