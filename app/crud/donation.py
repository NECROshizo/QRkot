from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
    DonationUpdate
]):
    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> List[Donation]:
        """
        Получает все пожертвования, сделанные пользователем из базы данных.
        #### Args:
        - user(User): Пользователь, для которого нужно получить пожертвования.
        - session(AsyncSession): Асинхронная сессия для работы с базой данных.
        #### Returns:
        - List[Donation]: Список пожертвований, сделанных пользователем.
        """
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)