from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectCreate, CharityProjectUpdate


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        """
        Получает все закрытые проекты.
        #### Args:
        - session(AsyncSession): Асинхронная сессия для работы с базой данных.
        #### Returns:
        - List[CharityProject]: Список закрытых проектов.
        """
        сollection_rate = (
            func.julianday(CharityProject.close_date) -
            func.julianday(CharityProject.create_date)).label('сollection_rate')
        query_close_obj = await session.execute(
            select(
                CharityProject.name,
                сollection_rate,
                CharityProject.description,
            )
            .where(CharityProject.fully_invested == 1)
            .order_by(сollection_rate)
        )
        projects = query_close_obj.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)