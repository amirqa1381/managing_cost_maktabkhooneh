
from typing import Annotated
from fastapi import FastAPI, status, Body, Path

from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

app = FastAPI()



costs = [{"id": 1, "description": "Initial cost", "amount": 100.0}]

# GET method for getting specific cost or list of costs


@app.get("/costs/{cost_id}/", status_code=status.HTTP_200_OK)
def get_specific_cost(cost_id: int):
    if cost_id:
        for c in costs:
            if c["id"] == cost_id:
                return JSONResponse(content={"data": c}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"error": f"The {cost_id} does not found"}, status_code=status.HTTP_404_NOT_FOUND)



@app.get("/costs/", status_code=status.HTTP_200_OK)
def get_all_costs():
    return JSONResponse(content={"data": costs}, status_code=status.HTTP_200_OK)



# POST method for creating the cost

@app.post("/costs/", status_code=status.HTTP_201_CREATED)
async def create_cost(description: Annotated[str, Body(...)], amount: Annotated[float, Body(...)]):
    new_id = max(c["id"] for c in costs) + 1 if costs else 1
    new_cost = {"id": new_id, "description": description, "amount": amount}
    costs.append(new_cost)
    return JSONResponse(content={"data": new_cost}, status_code=status.HTTP_201_CREATED)

# PUT method for updating the cost

@app.put("/costs/{cost_id}", status_code=status.HTTP_200_OK)
async def update_specific_cost(
    cost_id: Annotated[int, Path(description="Cost ID to update")],
    description: Annotated[str | None, Body(embed=True)] = None,
    amount: Annotated[float | None, Body(embed=True)] = None
):
    for c in costs:
        if c["id"] == cost_id:
            if description is not None:
                c["description"] = description
            if amount is not None:
                c["amount"] = amount
            return {"data": c}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")


# DELETE method for deleting the specific cost

@app.delete("/costs/{cost_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specific_cost(cost_id: int):
    if cost_id:
        for c in costs:
            if c["id"] == cost_id:
                costs.remove(c)
                return JSONResponse(content={"message": "object deleted successfully"}, status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")