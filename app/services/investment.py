from datetime import datetime
from typing import List, Set

from app.models.base import InvestModel


def investing(
        new_object: InvestModel,
        db_objects: List[InvestModel],
) -> Set:
    changed_db_objects = set()
    if new_object.invested_amount is None:
        new_object.invested_amount = 0
    for db_object in db_objects:
        investment_amount = min(
            db_object.full_amount - db_object.invested_amount,
            new_object.full_amount - new_object.invested_amount
        )
        for changed_object in (db_object, new_object):
            changed_object.invested_amount += investment_amount
            if changed_object.full_amount == changed_object.invested_amount:
                changed_object.fully_invested = True
                changed_object.close_date = datetime.now()
        changed_db_objects.add(db_object)
        if new_object.fully_invested is True:
            break
    return changed_db_objects
