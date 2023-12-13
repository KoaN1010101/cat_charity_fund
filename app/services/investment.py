from datetime import datetime
from typing import Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import InvestModel


async def investing(
    obj_in: InvestModel,
    model_db: InvestModel,
    session: AsyncSession
) -> InvestModel:
    source_db_all = await session.execute(select(model_db).where(
       model_db.fully_invested == False  # noqa
    ).order_by(model_db.create_date))
    source_db_all = source_db_all.scalars().all()
    for source_db in source_db_all:
        obj_in, source_db = await distribution(obj_in,
                                                     source_db)
        session.add(obj_in)
        session.add(source_db)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in


async def closed_for_investment(obj_db: InvestModel) -> InvestModel:
    obj_db.invested_amount = obj_db.full_amount
    obj_db.fully_invested = True
    obj_db.close_date = datetime.now()
    return obj_db


async def distribution(
    obj_in: InvestModel,
    obj_db: InvestModel
) -> Set[InvestModel]:
    rem_obj_in = obj_in.full_amount - obj_in.invested_amount
    rem_obj_db = obj_db.full_amount - obj_db.invested_amount
    if rem_obj_in > rem_obj_db:
        obj_in.invested_amount += rem_obj_db
        obj_db = await closed_for_investment(obj_db)
    elif rem_obj_in == rem_obj_db:
        obj_in = await closed_for_investment(obj_in)
        obj_db = await closed_for_investment(obj_db)
    else:
        obj_db.invested_amount += rem_obj_in
        obj_in = await closed_for_investment(obj_in)
    return obj_in, obj_db