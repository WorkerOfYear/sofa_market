from fastapi import APIRouter, Depends

from src import schemas
from src.dependencies import get_current_user, get_promotions_service
from src.services import PromotionsService

router = APIRouter(tags=["promotions"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[schemas.PromotionBase])
async def list_promotions(
    promotions_service: PromotionsService = Depends(get_promotions_service),
):
    """List all promotions (admin only)."""
    return await promotions_service.get_promotions()


@router.get("/{promotion_id}", response_model=schemas.PromotionWithProducts)
async def get_promotion(
    promotion_id: int,
    promotions_service: PromotionsService = Depends(get_promotions_service),
):
    """Get promotion with products (admin only)."""
    promotion = await promotions_service.get_promotion(promotion_id)
    products = await promotions_service.get_promotion_products(promotion_id)
    return schemas.PromotionWithProducts(
        **promotion.__dict__, products=[schemas.ProductBase.model_validate(p) for p in products]
    )


@router.post("", response_model=schemas.PromotionBase)
async def create_promotion(
    data: schemas.PromotionCreate,
    promotions_service: PromotionsService = Depends(get_promotions_service),
):
    """Create promotion (admin only)."""
    return await promotions_service.create_promotion(data)


@router.patch("/{promotion_id}", response_model=schemas.PromotionBase)
async def update_promotion(
    promotion_id: int,
    data: schemas.PromotionUpdate,
    promotions_service: PromotionsService = Depends(get_promotions_service),
):
    """Update promotion (admin only)."""
    return await promotions_service.update_promotion(promotion_id, data)


@router.delete("/{promotion_id}")
async def delete_promotion(
    promotion_id: int,
    promotions_service: PromotionsService = Depends(get_promotions_service),
):
    """Delete promotion (admin only)."""
    await promotions_service.delete_promotion(promotion_id)
    return {"message": "Promotion deleted"}


@router.post("/{promotion_id}/products")
async def apply_promotion_to_products(
    promotion_id: int,
    payload: schemas.ApplyProductsPayload,
    promotions_service: PromotionsService = Depends(get_promotions_service),
):
    """Apply promotion to multiple products (admin only)."""
    await promotions_service.apply_to_products(
        promotion_id, payload.product_ids
    )
    return {"message": f"Promotion applied to {len(payload.product_ids)} products"}


@router.delete("/{promotion_id}/products/{product_id}")
async def remove_product_from_promotion(
    promotion_id: int,
    product_id: int,
    promotions_service: PromotionsService = Depends(get_promotions_service),
):
    """Remove product from promotion (admin only)."""
    await promotions_service.remove_from_promotion(promotion_id, product_id)
    return {"message": "Product removed from promotion"}
