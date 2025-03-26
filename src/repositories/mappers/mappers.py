from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.schemas.bookings import BookingsDbAddSchema
from src.schemas.facilities import FacilitiesSchema, RoomsFacilitiesSchema
from src.schemas.rooms import RoomsSchema, RoomsWithRel
from src.schemas.users import UserShowSchema
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelSchema
from src.repositories.mappers.base import DataMapper


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = HotelSchema


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsSchema


class RoomsWithRelDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRel


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserShowSchema


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = FacilitiesSchema


class RoomsFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomsFacilitiesSchema


class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = BookingsDbAddSchema
