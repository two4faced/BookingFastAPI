from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService


router = APIRouter(prefix='/auth', tags=['Авторизация и Аутентификация'])


@router.post('/register')
async def register_user(
        user_data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(
        name=user_data.name,
        nickname=user_data.nickname,
        email=user_data.email,
        hashed_password=hashed_password
    )
    try:
        async with async_session_maker() as session:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
    except IntegrityError as exception:
        return {'error': {str(exception.orig)}}

    return {'status': 'OK'}


@router.post('/login')
async def login_user(
        user_data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_pass(email=user_data.email)
        if not user:
            raise HTTPException(status_code=401, detail='Такого пользователя не существует.')
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Имя пользователя или пароль неверные.')
        access_token = AuthService().create_access_token({'user_id': user.id})

    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}
