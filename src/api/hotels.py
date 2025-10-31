from fastapi import Query, APIRouter, Body

from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix='/hotels', tags=['Отели'])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get('', summary='Получить отели')
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description='ID отеля'),
        title: str | None = Query(None, description='Название отеля')
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)

    offset_min = (pagination.page - 1) * pagination.per_page
    offset_max = pagination.page * pagination.per_page
    return hotels_[offset_min:offset_max]


@router.post('', summary='Добавить отель')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya",
            "location": "ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "name": "dubai_fountain",
            "location": "ул. Шейха, 2",
        }
    }
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status': 'OK'}


@router.delete('/{hotel_id}', summary='Удалить отель')
def del_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.put("/{hotel_id}", summary='Изменить отель')
def change_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotels[hotel_id - 1]['title'] = hotel_data.title
    hotels[hotel_id - 1]['name'] = hotel_data.name
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary='Частично изменить отель')
def edit_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    if hotel_data.name:
        hotels[hotel_id - 1]['name'] = hotel_data.name
    if hotel_data.title:
        hotels[hotel_id - 1]['title'] = hotel_data.title
    return {'status': 'OK'}