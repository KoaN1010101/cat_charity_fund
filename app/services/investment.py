from datetime import datetime
from typing import List

from app.models.base import InvestModel


def investing(
        target: InvestModel,
        sources: List[InvestModel],
) -> List[InvestModel]:
    changed = list()
    if target.invested_amount is None:
        target.invested_amount = 0
    for source in sources:
        amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for invested in (source, target):
            invested.invested_amount += amount
            if invested.full_amount == invested.invested_amount:
                invested.fully_invested = True
                invested.close_date = datetime.now()
        changed.append(source)
        if target.fully_invested:
            break
    return changed
