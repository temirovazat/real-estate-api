from typing import Any, List

from databases import Database
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app import crud, schemas
from app.api.deps import get_db_pg, get_request_active_superuser

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.AmenityOut],
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_amenities(
    *,
    skip: int = Query(0),
    limit: int = Query(100),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Retrieve amenities.
    """
    return await crud.amenity.get_multi(db, skip=skip, limit=limit)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AmenityOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def create_amenity(
    *,
    amenity: schemas.AmenityIn = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Create new amenity.
    """
    db_amenity = await crud.amenity.get_by_name(db, name=amenity.name)
    if db_amenity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The amenity with this name already exists.",
        )
    return await crud.amenity.create(db, obj_in=amenity)


@router.get(
    "/{amenity_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AmenityOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_amenity_by_id(
    *,
    amenity_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Get a specific amenity by id.
    """
    amenity = await crud.amenity.get(db, model_id=amenity_id)
    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The amenity with this id does not exist",
        )
    return amenity


@router.put(
    "/{amenity_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AmenityOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def update_amenity(
    *,
    amenity_id: int = Path(...),
    amenity_in: schemas.AmenityUpdate = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Update an amenity.
    """
    amenity = await crud.amenity.get(db, model_id=amenity_id)
    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The amenity with this id does not exist",
        )
    return await crud.amenity.update(db, db_obj=amenity, obj_in=amenity_in)


@router.delete(
    "/{amenity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_request_active_superuser)],
)
async def delete_amenity(
    *,
    amenity_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> None:
    """
    Delete an amenity.
    """
    amenity = await crud.amenity.get(db, model_id=amenity_id)
    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The amenity with this id does not exist",
        )
    return await crud.amenity.remove(db, model_id=amenity_id)
