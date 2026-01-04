from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Bookings
from src.schemas.facilities import Facilities, RoomFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Rooms, RoomsWithRels
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Rooms


class RoomsWithRelsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomsWithRels


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Bookings


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facilities


class RoomFacilitiesDataMapper(DataMapper):
    db_model = RoomFacilitiesORM
    schema = RoomFacility
