from fastapi import APIRouter, Depends

from src.dependencies import get_current_user, get_purchases_service
from src.schemas.purchases import PurchaseResponse
from src.schemas.users import UserBase
from src.services.purchases import PurchasesService

router = APIRouter(tags=["purchases"], dependencies=[Depends(get_current_user)])


@router.post("/checkout", response_model=PurchaseResponse)
async def checkout(
    user: UserBase = Depends(get_current_user),
    purchases_service: PurchasesService = Depends(get_purchases_service),
):
    return await purchases_service.checkout(user.id)


@router.get("", response_model=list[PurchaseResponse])
async def get_my_purchases(
    user: UserBase = Depends(get_current_user),
    purchases_service: PurchasesService = Depends(get_purchases_service),
):
    return await purchases_service.get_my_purchases(user.id)


@router.get("/{purchase_id}", response_model=PurchaseResponse)
async def get_purchase(
    purchase_id: int,
    user: UserBase = Depends(get_current_user),
    purchases_service: PurchasesService = Depends(get_purchases_service),
):
    return await purchases_service.get_purchase(purchase_id, user.id)
