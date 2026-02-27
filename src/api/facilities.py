from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import ObjectAlreadyExistsException, FacilityAlreadyExists
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilitiesService

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('')
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    return await FacilitiesService(db).get_all_facilities()


@router.post('')
async def create_facility(facility_data: FacilityAdd, db: DBDep):
    try:
        result = await FacilitiesService(db).create_facility(facility_data)
        return {'status': 'OK', 'data': result}
    except ObjectAlreadyExistsException:
        raise FacilityAlreadyExists
