from src.services.base import BaseService


class FacilitiesService(BaseService):
    async def get_all_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, facility_data):
        result = await self.db.facilities.add(facility_data)
        await self.db.commit()

        return result
