from datetime import date

from fastapi import Path, APIRouter, HTTPException, Query
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsAddRequest

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(
    db: DBDep,
    date_from: date = Query(example='2024-08-01'),
    date_to: date = Query(example='2024-08-10'),
    hotel_id: int = Path(),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(
    db: DBDep,
    hotel_id: int = Path(),
    room_id: int = Path()
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post('/{hotel_id}/rooms')
async def add_room(
        room_data: RoomsAddRequest,
        db: DBDep,
        hotel_id: int = Path()
):
    try:
        res = await db.rooms.add(RoomsAdd(hotel_id=hotel_id, **room_data.model_dump()))
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404, detail='Данный отель не существует')

    return {'status': 'OK', 'data': res}


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {'status': 'OK'}


@router.patch('/{hotel_id}/rooms/{room_id}')
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomsPatch
):
    await db.rooms.edit(data, is_patch = True, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {'status': 'OK'}

@router.put("/{hotel_id}/rooms/{room_id}", summary='Изменить номер')
async def change_hotel(hotel_id: int, room_id: int, room_data: RoomsAddRequest, db: DBDep):
    await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK'}
