class AppError(Exception):
    def __init__(self, message, status_code=500):
        super().__init__()
        self.message = message
        self.status_code = status_code

class ValidationError(AppError):
    def __init__(self, message):
        super().__init__(message, status_code=400)

class NotFoundError(AppError):
    def __init__(self, message):
        super().__init__(message, status_code=404)

class ClientInvocationError(AppError):
    def __init__(self, message):
        super().__init__(message, status_code=500)