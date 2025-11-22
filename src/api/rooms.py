from fastapi import Path, APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomsAdd, RoomsPatch

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(
    hotel_id: int = Path()
):
    async with async_session_maker() as session:
        async with async_session_maker() as session:
            return await RoomsRepository(session).get_all(id=hotel_id)


@router.post('/{hotel_id}/rooms')
async def add_room(
        room_data: RoomsAdd,
        hotel_id: int = Path()
):
    async with async_session_maker() as session:
        try:
            res = await RoomsRepository(session).add_room(room_data, hotel_id)
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

@router.put("/{hotel_id}/rooms/{room_id}", summary='Изменить отель')
async def change_hotel(hotel_id: int, room_id: int, hotel_data: RoomsAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(hotel_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
