from datetime import date

from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_hotels(
        self,
        pagination,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        per_page = pagination.per_page or 5

        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        result = await self.db.hotels.add(hotel_data)
        await self.db.commit()

        return result

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def change_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        await self.db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
        await self.db.commit()

    async def check_hotel_existence(self, hotel_id) -> None:
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
