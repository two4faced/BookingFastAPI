import pytest
from pydantic import EmailStr


@pytest.mark.parametrize(
    'name, nickname, email, password, status_code',
    [
        ('franz', 'franz__', 'fra123@gmail.com', '3838dkmwi03', 200),
        ('qwerty', 'qw2erty', 'fra123@gmail.com', '454gfdsa', 409),
        ('qwerty', 'qw2erty', 'abcde', '454gfdsa', 422),
    ],
)
async def test_register_user(
    ac, name: str, nickname: str, email: EmailStr, password: str, status_code: int
):
    response = await ac.post(
        '/auth/register',
        json={'name': name, 'nickname': nickname, 'email': email, 'password': password},
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    'email, password, status_code',
    [
        ('qwe33@gmail.com', '454gfdsa', 401),
        ('fra123@gmail.com', '12345', 401),
        ('fra123@gmail.com', '3838dkmwi03', 200),
    ],
)
async def test_login_user(ac, email: EmailStr, password: str, status_code: int):
    response = await ac.post('/auth/login', json={'email': email, 'password': password})

    assert response.status_code == status_code
    if response.status_code == 200:
        assert ac.cookies['access_token']


async def test_get_me_login(ac):
    response = await ac.get('/auth/me')
    result = response.json()

    assert 'nickname' in result
    assert result['email'] == 'fra123@gmail.com'
    assert 'password' not in result
    assert 'hashed_password' not in result
    assert isinstance(result, dict)


async def test_logout(ac):
    response = await ac.post('/auth/logout')
    assert not response.cookies


async def test_get_me_logout(ac):
    response = await ac.get('/auth/me')
    assert response.status_code == 401
