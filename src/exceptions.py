from fastapi import HTTPException


class BookingException(Exception):
    detail = 'Непредвиденная ошибка'

    def __init__(self, *args):
        super().__init__(self.detail, *args)


class ObjectNotFoundException(BookingException):
    detail = 'Объект не найден'


class HotelNotFoundException(ObjectNotFoundException):
    detail = 'Отель не найден'


class RoomNotFoundException(ObjectNotFoundException):
    detail = 'Номер не найден'


class ObjectAlreadyExistsException(BookingException):
    detail = 'Объект уже существует'


class AllRoomsBookedException(BookingException):
    detail = 'Не осталось свободных номеров'


class DateFromLaterThenOrEQDateToException(BookingException):
    detail = 'Дата заезда позже или равна дате выезда'


class BookingHTTPException(HTTPException):
    status_code = 500
    detail = 'Непредвиденная ошибка'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = 'Данный отель не найден'


class RoomNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = 'Данный номер не найден'
