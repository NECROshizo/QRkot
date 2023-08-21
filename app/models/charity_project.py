from sqlalchemy import CheckConstraint, Column, String, Text

from .base_model import BaseModel


class CharityProject(BaseModel):
    """
    Представляет проекта в базе данных.
    #### Attributes:
        - id(int): ID проекта в базе данных. PrimaryKey
        - name(str): Название проекта от 1 до 100 символов.*
        - description(str): Описание проекта.*
        - full_amount(int): Общая сумма, необходимая для проекта.*
        - invested_amount(int): Сумма, которая уже была вложена в проект.
        По умолчанию равна 0.
        - fully_invested(bool): Флаг, указывающий, что проект был полностью
        финансирован. По умолчанию False.
        - create_date(datetime): Дата создания проекта.
        - close_date(datetime): Дата закрытия проекта.
    """

    __table_args__ = BaseModel.__table_args__ + (
        CheckConstraint('LENGTH(name) > 0'),
    )

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f'Проект {self.name} от {self.create_date}'
            f'собрал {self.invested_amount} из {self.full_amount}'
        )
