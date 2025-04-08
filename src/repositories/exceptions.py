class HotelsBaseExceptions(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ItemNotFoundException(HotelsBaseExceptions):
    detail = "Object not found"


class FKNotFoundException(HotelsBaseExceptions):
    detail = "Object not found"


class TooManyItemFoundException(HotelsBaseExceptions):
    detail = "To many objects found"


class DuplicateItemException(HotelsBaseExceptions):
    detail = "Duplicate object found"


class NoRoomAvailableException(HotelsBaseExceptions):
    detail = "No free room found"
