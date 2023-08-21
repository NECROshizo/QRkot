from sqlalchemy import Column, ForeignKey, Integer, Text

from .base_model import BaseModel


class Donation(BaseModel):
    """
    Представляет пожертвований в базе данных.
    #### Attributes:
        - id (int): ID пожертвования в базе данных. PrimaryKey
        - user_id (int): ID пользователя, который сделал пожертвование.
        ForeignKey
        - comment (str): Комментарий, связанный с пожертвованием.
        - full_amount (int): Сумма пожертвования.*
        - invested_amount (int): Cумма из пожертвования, которая распределена
        по проектам. По умолчанию равна 0.
        - fully_invested (bool): Флаг, указывающее на то, все ли деньги из
        пожертвования были переведены в тот или иной проект. По умолчанию False.
        - create_date (datetime): Дата пожертвования.
        - close_date (datetime): Дата, когда вся сумма пожертвования была распределена по
        проектам
    """

    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)

    def __repr__(self) -> str:
        return (
            f'Пожертвование {self.fully_invested}'
            f'от {self.create_date}'
            f'из которых распределено{self.invested_amount}'
        )
