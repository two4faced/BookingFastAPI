from datetime import date

from fastapi import Path, APIRouter, HTTPException, Query
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsAddRequest, RoomsPatchRequest

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
        print(res)

        if room_data.facilities_ids:
            rooms_facilities_data = [RoomFacilityAdd(room_id=res.id, facility_id=f_id) for f_id in room_data.facilities_ids]
            await db.room_facilities.add_batch(rooms_facilities_data)

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
    data: RoomsPatchRequest
):
    await db.rooms.edit(
        RoomsPatch(**data.model_dump()),
        is_patch = True,
        id=room_id,
        hotel_id=hotel_id
    )

    if data.facilities_ids:
        await db.room_facilities.change_room_facilities(room_id=room_id, data=data)

    await db.commit()

    return {'status': 'OK'}

@router.put("/{hotel_id}/rooms/{room_id}", summary='Изменить номер')
async def change_room(hotel_id: int, room_id: int, room_data: RoomsAddRequest, db: DBDep):
    await db.rooms.edit(RoomsAdd(hotel_id=hotel_id, **room_data.model_dump()))
    await db.room_facilities.change_room_facilities(room_id=room_id, data=room_data)
    await db.commit()
    return {'status': 'OK'}
