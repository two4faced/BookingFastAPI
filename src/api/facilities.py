from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix='/rooms', tags=['Удобства'])


@router.get('/facilities')
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()



@router.post('/facilities')
async def add_facility(data: FacilityAdd, db: DBDep):
    result = await db.facilities.add(data)
    await db.commit()

    return {'status': 'OK', 'data': result}

