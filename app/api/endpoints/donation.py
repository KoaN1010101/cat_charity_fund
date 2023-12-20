from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationView
from app.services.investment import investing

router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(session: AsyncSession = Depends(get_async_session)):
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=list[DonationView])
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_user_donations(user, session)


@router.post(
    '/',
    response_model_exclude_none=True,
    response_model=DonationDB,
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested', 'close_date',
    },
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        obj_in=donation,
        session=session,
        user=user,
        commit=False,
    )
    charity_projects = await charity_project_crud.get_uninvested(session)
    if charity_projects:
        calculated_investments = investing(
            target=new_donation,
            sources=charity_projects,
        )
        session.add_all(calculated_investments)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
