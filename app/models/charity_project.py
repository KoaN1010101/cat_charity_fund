from sqlalchemy import Column, String, Text

from app.models.base import InvestModel


class CharityProject(InvestModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Название- {self.name}, '
            f'Описание - {self.description}, '
            f' {super().__repr__()}'
        )
