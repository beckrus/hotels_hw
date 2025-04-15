from fastapi import HTTPException


class BaseException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseHttpException(HTTPException):
    status_code = 500
    detail = "Something went wrong"

    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=self.status_code, detail=self.detail, *args, **kwargs
        )


class ItemNotFoundException(BaseException):
    detail = "Object not found"


class FKNotFoundException(BaseException):
    detail = "Rel Object not found"


class TooManyItemFoundException(BaseException):
    detail = "To many objects found"


class DuplicateItemException(BaseException):
    detail = "Duplicate object found"


class NoRoomAvailableException(BaseException):
    detail = "No free room found"


class NoRoomAvailableHttpException(BaseHttpException):
    status_code = 409
    detail = "No free room found"


class FacilityNotFoundException(BaseException):
    detail = "Facility not found"


class FacilityNotFoundHttpException(BaseHttpException):
    status_code = 404
    detail = "Facility not found"


class FacilityDuplicateHTTPException(BaseHttpException):
    status_code = 409
    detail = "Facility already exist"


class FacilityDuplicateException(BaseException):
    detail = "Facility already exist"


class HotelNotFoundException(BaseException):
    detail = "Hotel not found"


class HotelNotFoundHttpException(BaseHttpException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundException(BaseException):
    detail = "Room not found"


class RoomNotFoundHttpException(BaseHttpException):
    status_code = 404
    detail = "Room not found"


class PasswordsNotMatchException(BaseException):
    detail = "Passwords deoes not matched"


class PasswordsNotMatchHttpException(BaseHttpException):
    status_code = 422
    detail = "Passwords deoes not matched"


class UserDuplicateException(BaseException):
    detail = "User with these username, email or phone already exists"


class UserDuplicateHttpException(BaseHttpException):
    status_code = 409
    detail = "User with these username, email or phone already exists"


class UserAuthException(BaseException):
    detail = "Authentication failed"


class UserAuthHttpException(BaseHttpException):
    status_code = 401
    detail = "Authentication failed"

class UserAlreadyAuthanticatedHttpException(BaseHttpException):
    status_code = 200
    detail = "You are already authenticated"


class UserNotFoundException(BaseException):
    detail = "User not found"


class UserNotFoundHttpException(BaseHttpException):
    status_code = 404
    detail = "User not found"


class TokenErrorHttpException(BaseHttpException):
    status_code = 401
    detail = "Could not validate credentials"


class AccessForbiddenHttpException(BaseHttpException):
    status_code = 401
    detail = "Access denied, not enough permissions."


class BookingNotFoundException(BaseException):
    detail = "Booking not found"


class BookingNotFoundHttpException(BaseHttpException):
    status_code = 404
    detail = "Booking not found"

class HotelDumpicateHttpException(BaseHttpException):
    status_code = 409
    detail = "Hotel with these name and location already exist"