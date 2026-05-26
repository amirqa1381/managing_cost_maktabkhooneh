class ExpenseNotFoundException(Exception):
    def __init__(self, expense_id: int):
        self.expense_id = expense_id


class UnauthorizedException(Exception):
    def __init__(self, message: str = "You don't have permission to access to this part"):
        self.message = message
