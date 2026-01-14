from httpx import AsyncClient


async def test_get_facilities(ac: AsyncClient):
    response = await ac.get('/facilities')

    assert response.status_code == 200


async def test_post_facilities(ac, db):
    facility_title = 'SPA'
    response = await ac.post('/facilities', json={'title': facility_title})

    assert response.status_code == 200
    assert await db.facilities.get_one_or_none(title=facility_title)

    result = response.json()

    assert 'data' in result
    assert result['data']['title'] == facility_title
