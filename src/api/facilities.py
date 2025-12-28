from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('')
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post('')
async def add_facility(facility_data: FacilityAdd, db: DBDep):
    result = await db.facilities.add(facility_data)
    await db.commit()

    return {'status': 'OK', 'data': result}

