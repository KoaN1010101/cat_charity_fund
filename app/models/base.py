from datetime import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core.db import Base


class InvestModel(Base):
    __abstract__ = True

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint('invested_amount >= 0', name='check_invested_amount_positive'),
        CheckConstraint('invested_amount <= full_amount', name='check_invested_amount_not_exceed_full_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return ('Дата создания - {self.create_date}, '
                'Общая сумма - {self.full_amount}, '
                'Инвестировано - {self.invested_amount}, '
                'Дата закрытия - {self.close_date}. ')
