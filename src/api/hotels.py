from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('', summary='Получить отели')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Локация отеля')
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        query = select(HotelsORM)
        if location:
            query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
        if title:
            query = query.filter(HotelsORM.title.ilike(f"%{title}%"))

        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        # print(hotels)
        return hotels


@router.post('', summary='Добавить отель')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель 5 звезд у моря",
            "location": "г. Сочи, ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель У фонтана",
            "location": "Дубай, ул. Шейха, 2",
        }
    }
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
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