from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd, UserLogIn
from src.services.auth import AuthService


router = APIRouter(prefix='/auth', tags=['Авторизация и Аутентификация'])


@router.post('/register')
async def register_user(
        user_data: UserRequestAdd,
        db: DBDep
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(
        name=user_data.name,
        nickname=user_data.nickname,
        email=user_data.email,
        hashed_password=hashed_password
    )
    try:
        await db.users.add(new_user_data)
        await db.commit()
    except IntegrityError:
        raise HTTPException(404, 'Этот никнейм или почта уже заняты')

    return {'status': 'OK'}


@router.post('/login')
async def login_user(
        user_data: UserLogIn,
        response: Response,
        db: DBDep
):
    is_user = await db.users.get_one_or_none(email=user_data.email)
    if not is_user:
        raise HTTPException(status_code=401, detail='Такого пользователя не существует.')
    user = await db.users.get_user_with_hashed_pass(email=user_data.email)
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Имя пользователя или пароль неверные.')
    access_token = AuthService().create_access_token({'user_id': user.id})

    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}

@router.get('/me')
async def get_me(
        user_id: UserIdDep,
        db: DBDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post('/logout')
async def logout(
    response: Response
):
    response.delete_cookie('access_token')
    return {'status': 'OK'}
