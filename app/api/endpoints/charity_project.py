from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_exists, check_name_duplicate, check_project_start,
    check_full_amount, check_project_close)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services import StringCharityProject as const
from app.services import invest_process
from app.schemas import (
    CharityProjectCreate, CharityProjectRead, CharityProjectUpdate)
router = APIRouter()


@router.get(
    '/',
    summary=const.GET_ALL,
    response_model=List[CharityProjectRead],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectRead]:
    """
    Получение списка всех благотворительных проектов
    #### Args:
        - session (AsyncSession) асинхронная сессия базы данных.
    Добавлена через Depends.
    #### Returns:
        - List[CharityProjectRead]: список объектов типа CharityProjectRead
    """
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    summary=const.CREATE,
    description=const.CREATE_DESCRIPTION,
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_projects(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectRead:
    """
    Создает новый благотворительный проект.
    #### Args:
        - project (CharityProjectCreate): Данные для нового благотворительного проекта.
        - session (AsyncSession): Асинхронная сессия базы данных.
        Добавлена через Depends.
    #### Returns:
        - CharityProjectRead: Созданный благотворительный проект.
    """
    await check_name_duplicate(project.name, session)
    new_projects = await charity_project_crud.create(project)
    await invest_process(new_projects, session)
    return new_projects


@router.delete(
    '/{project_id}',
    summary=const.DELETE,
    description=const.DELETE_DESCRIPTION,
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_projects(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectRead:
    """
    Удаляет благотворительный проект по его ID.
    #### Args:
        - project_id (int): ID благотворительного проекта, который нужно удалить.
        - session (AsyncSession): Асинхронная сессия базы данных. Добавлена через Depends.
    #### Returns:
        - CharityProjectRead: Удаленный благотворительный проект.
    """
    project = await check_project_exists(project_id, session)
    await check_project_start(project)
    await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    summary=const.UPDATE,
    description=const.UPDATE_DESCRIPTION,
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_projects(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectRead:
    """
    Обновляет благотворительный проект.
    #### Args:
        - project_id  (int): ID проекта, который нужно обновить.
        - project_in (CharityProjectUpdate): Обновленные данные для проекта.
        - session (AsyncSession): Асинхронная сессия базы данных.
        Добавлена через Depends.
    #### Returns:
        - CharityProjectRead: Обновленный благотворительный проект.
    """
    project = await check_project_exists(project_id, session)
    await check_project_close(project)

    if project_in.name is not None:
        await check_name_duplicate(project_in.name, session)
    if project_in.full_amount is not None:
        project_in = await check_full_amount(project_in, project)
    project = await charity_project_crud.update(
        project, project_in, session
    )
    return project