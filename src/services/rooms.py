from datetime import date

from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomsAddRequest, RoomsAdd, RoomsPatchRequest, RoomsPatch
from src.services.base import BaseService
from src.services.hotels import HotelsService


class RoomsService(BaseService):
    async def get_rooms(self, date_from: date, date_to: date, hotel_id: int):
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, room_id: int, hotel_id: int):
        result = await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
        return result

    async def add_room(self, room_data: RoomsAddRequest, hotel_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as exc:
            raise HotelNotFoundException from exc

        result = await self.db.rooms.add(RoomsAdd(hotel_id=hotel_id, **room_data.model_dump()))

        if room_data.facilities_ids:
            rooms_facilities_data = [
                RoomFacilityAdd(room_id=result.id, facility_id=f_id)
                for f_id in room_data.facilities_ids
            ]
            await self.db.room_facilities.add_batch(rooms_facilities_data)

        await self.db.commit()
        return result

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelsService(self.db).check_hotel_existence(hotel_id)
        await self.check_room_existence(room_id)

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomsPatchRequest):
        await HotelsService(self.db).check_hotel_existence(hotel_id)
        await self.check_room_existence(room_id)

        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomsPatch(**_room_data_dict)

        await self.db.rooms.edit(_room_data, is_patch=True, id=room_id, hotel_id=hotel_id)
        if room_data.facilities_ids:
            await self.db.room_facilities.change_room_facilities(room_id=room_id, data=room_data)

        await self.db.commit()

    async def change_room(self, hotel_id: int, room_id: int, room_data: RoomsAddRequest):
        await HotelsService(self.db).check_hotel_existence(hotel_id)
        await self.check_room_existence(room_id)

        await self.db.rooms.edit(RoomsAdd(hotel_id=hotel_id, **room_data.model_dump()))
        await self.db.room_facilities.change_room_facilities(room_id=room_id, data=room_data)
        await self.db.commit()

    async def check_room_existence(self, room_id) -> None:
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
