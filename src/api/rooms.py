from fastapi import Path, APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsAddRequest, Rooms

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(
    hotel_id: int = Path()
):
    async with async_session_maker() as session:
            return await RoomsRepository(session).get_all(hotel_id=hotel_id)

@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(
    hotel_id: int = Path(),
    room_id: int = Path()
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post('/{hotel_id}/rooms')
async def add_room(
        room_data: RoomsAddRequest,
        hotel_id: int = Path()
):
    async with async_session_maker() as session:
        try:
            res = await RoomsRepository(session).add(RoomsAdd(hotel_id=hotel_id, **room_data.model_dump()))
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=404, detail='Данный отель не существует')

    return {'status': 'OK', 'data': res}


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {'status': 'OK'}


@router.patch('/{hotel_id}/rooms/{room_id}')
async def edit_room(
    hotel_id: int,
    room_id: int,
    data: RoomsPatch
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data, is_patch = True, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {'status': 'OK'}

@router.put("/{hotel_id}/rooms/{room_id}", summary='Изменить номер')
async def change_hotel(hotel_id: int, room_id: int, room_data: RoomsAddRequest):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
