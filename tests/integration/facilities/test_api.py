

async def test_get_facilities(ac):
    response = await ac.get(
        '/facilities'
    )

    assert response.status_code == 200


async def test_add_facility(ac, db):
    response = await ac.post(
        '/facilities',
        json={
            'title': 'SPA'
        }
    )

    assert response.status_code == 200
    assert db.facilities.get_one_or_none(title='SPA')
