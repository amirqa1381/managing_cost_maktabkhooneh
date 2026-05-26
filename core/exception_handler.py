from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi import FastAPI

from exceptions import ExpenseNotFoundException, UnauthorizedException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ExpenseNotFoundException)
    async def expense_not_found_handler(request: Request, exc: ExpenseNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": status.HTTP_404_NOT_FOUND,
                "message": f"The Cost with this ID {exc.expense_id} was not found",
            },
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": status.HTTP_401_UNAUTHORIZED,
                "error_type": "UNAUTHORIZED_ACCESS",
                "message": exc.message,
            },
        )
