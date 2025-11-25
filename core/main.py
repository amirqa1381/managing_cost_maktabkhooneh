
from typing import Annotated
from fastapi import FastAPI, status, Body, Path

from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from .schemas import CostReadModel, CostCreateModel, CostUpdateModel

app = FastAPI()



costs = [{"id": 1, "description": "Initial cost", "amount": 100.0}]

# GET method for getting specific cost or list of costs


@app.get("/costs/{cost_id}/", status_code=status.HTTP_200_OK, response_model=CostReadModel)
def get_specific_cost(cost_id: int):
    if cost_id:
        for c in costs:
            if c["id"] == cost_id:
                return c
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cost with id {cost_id} was not found")



@app.get("/costs/", status_code=status.HTTP_200_OK, response_model=list[CostReadModel])
def get_all_costs():
    return costs



# POST method for creating the cost

@app.post("/costs/", status_code=status.HTTP_201_CREATED, response_model=CostReadModel)
async def create_cost(cost: CostCreateModel):
    new_id = max(c["id"] for c in costs) + 1 if costs else 1
    new_cost = {"id": new_id, "description": cost.description, "amount": float(cost.amount)}
    costs.append(new_cost)
    print(costs)
    return new_cost

# PUT method for updating the cost

@app.put("/costs/{cost_id}", status_code=status.HTTP_200_OK, response_model=CostReadModel)
async def update_specific_cost(
    cost_id: Annotated[int, Path(description="Cost ID to update")],
    cost: CostUpdateModel
):
    for c in costs:
        if c["id"] == cost_id:
            if cost.description is not None:
                c["description"] = cost.description
            if cost.amount is not None:
                c["amount"] = cost.amount
            return c

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")


# DELETE method for deleting the specific cost

@app.delete("/costs/{cost_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specific_cost(cost_id: int):
    for i, c in enumerate(costs):
        if c["id"] == cost_id:
            costs.pop(i)  # or costs.remove(c)
            return Response(status_code=status.HTTP_204_NO_CONTENT)  # no body!
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")