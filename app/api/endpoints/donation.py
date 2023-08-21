from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.services import StringDonation as const
from app.services import invest_process
from app.schemas import (
    DonationCreate, DonationRead)

router = APIRouter()


@router.get(
    '/',
    summary=const.GET,
    description=const.GET_DESCRIPTION,
    response_model=List[DonationRead],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_donation(
        session: AsyncSession = Depends(get_async_session),
) -> List[DonationRead]:
    """
    Получение данных из базы данных о всех пожертвованиях.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    summary=const.CREATE,
    description=const.CREATE_DESCRIPTION,
    response_model=DonationRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested', 'close_date'},
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> DonationRead:
    """
    Создание новой пожертвования.
    #### Args:
        - donation (DonationCreate): Модель данных для создания пожертвования.
        - session (AsyncSession): Асинхронная сессия базы данных.
          Добавлена через Depends.
        - user (User): Модель данных для пользователя.
          Добавлена через Depends.
    #### Returns:
        - DonationRead: Созданная модель пожертвования.
    """
    new_donate = await donation_crud.create(donation, user=user)
    await invest_process(new_donate, session)
    return new_donate


@router.get(
    '/my',
    summary=const.GET_ALL,
    description=const.GET_ALL_DESCRIPTION,
    response_model=List[DonationRead],
    dependencies=[Depends(current_user)],
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested', 'close_date'},
)
async def get_all_donation(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> List[DonationRead]:
    """
    Получение списка пожертвований пользователя.
    #### Args:
        - user (User): Модель данных для пользователя.
          Добавлена через Depends.
        - session (AsyncSession): Асинхронная сессия базы данных.
          Добавлена через Depends.
    #### Returns:
        - List[DonationRead]: Список моделей пожертвований пользователя.
    """
    donations = await donation_crud.get_by_user(user, session)
    return donations