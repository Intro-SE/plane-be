from fastapi import HTTPException, status


class BadRequestHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg if msg else "Bad request",
        )


class AuthFailedHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthTokenExpiredHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=msg if msg else "Requested resource is forbidden",
        )


class NotFoundHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg if msg else "Requested resource is not found",
        )


class ConflictHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=msg if msg else "Conflicting resource request",
        )


class ServiceNotAvailableHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=msg if msg else "Service not available",
        )


class AccessNullObjectError(Exception):
    def __init__(self, ObjectType: str, code: str, message="not found"):
        self.ObjectType = ObjectType
        self.code = code
        self.message = f"{ObjectType} {code} {message}"
        super().__init__(self.message)



class TestSessionExpiredHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=512,
            detail=msg if msg else "Test session expired",
        )
        
class FreePlanTimeLimitReachedHTTPException(HTTPException):
    def __init__(self, required_time_in_seconds: int, wait_time_mins: int):
        msg=f"With free version, you need at least {required_time_in_seconds/60} minutes for this test. Wait {wait_time_mins} minutes for your next free 5-minute session or speak more with Premium package."
        super().__init__(
            status_code=209,
            detail=msg,
        )
        
class OtherPlanTimeLimitReachedHTTPException(HTTPException):
    def __init__(self, plan_detail: str):
        #msg=f"Your {plan_detail} has expired. You are now on the free plan, which includes 5 free minutes daily. Once you have used up these minutes, you can either upgrade to the premium version for unlimited access or wait 24 hours for your free minutes to reset."
        msg = f"You have used your {plan_detail} minutes for this month. Another {plan_detail} minutes will be available in the next subscription cycle. If you want to earn extra minutes, be sure to check out our fan page and group. We regularly run campaigns where Premium users can receive bonus minutes."
        super().__init__(
            status_code=209,
            detail=msg,
        )