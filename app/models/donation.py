from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestModel


class Donation(InvestModel):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey(
        'user.id', name='fk_donation_user_id_user'
    ))

    def __repr__(self):
        return (
            f'Комментарий- {self.comment}, '
            f'ID юзера - {self.user_id}'
            f' {super().__repr__()}'
        )
