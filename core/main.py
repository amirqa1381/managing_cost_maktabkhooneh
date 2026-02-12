
from typing import Annotated
from fastapi import FastAPI, status, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import CostRead, CostCreate, CostUpdate, UserRead, UserCreate
from models import Costs, Users
from database_test import get_db
app = FastAPI()




# GET method for getting specific cost or list of costs


@app.get("/costs/{cost_id}", status_code=status.HTTP_200_OK, response_model=CostRead)
def get_specific_cost(cost_id: int, db:Session = Depends(get_db)):
    cost = db.query(Costs).filter_by(id=cost_id).first()
    
    if not cost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return cost



@app.get("/costs", status_code=status.HTTP_200_OK, response_model=list[CostRead])
def get_all_costs(db: Session = Depends(get_db)):
    """
    function for getting the list of the Costs
    """
    costs = db.query(Costs).all()
    return costs



# POST method for creating the cost

@app.post("/costs", status_code=status.HTTP_201_CREATED, response_model=CostRead)
async def create_cost(request: CostCreate, db: Session = Depends(get_db)):
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
    db: Session = Depends(get_db)
):
    cost = db.query(Costs).filter_by(id=cost_id).first()
    
    if not cost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the exciting cost does not exist")

    
    # here we update the provided fields
    updated_data = request.model_dump(exclude_unset=True)
    
    for key , value in updated_data.items():
        setattr(cost, key, value)
        
    db.commit()
    db.refresh(cost)
    
    return cost


# DELETE method for deleting the specific cost

@app.delete("/costs/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_specific_cost(cost_id: int, db: Session = Depends(get_db)):
    cost = db.query(Costs).filter_by(id=cost_id).first()
    
    if not cost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="exciting item does not exist")
    
    db.delete(cost)
    db.commit()




# Adding User for creating the Costs


# here password does not hash and it is so simple for getting the user id for creating the costs
@app.post("/user", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db: Session= Depends(get_db)):
    new_user = Users(**request.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user