from typing import Any, List

from databases import Database
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app import crud, schemas
from app.api.deps import get_db_pg, get_request_active_superuser
from app.utils.unit import unit_dict

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.UnitOut],
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_units(
    *,
    skip: int = Query(0),
    limit: int = Query(100),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Retrieve units.
    """
    units = list()
    db_units = await crud.unit.get_multi(db, skip=skip, limit=limit)
    for unit in db_units:
        units.append(
            unit_dict(
                unit_record=unit,
                amenities=await crud.unit.get_unit_amenities(db, model_id=unit.id),
            )
        )

    return units


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.UnitOut],
    dependencies=[Depends(get_request_active_superuser)],
)
async def search_units(
    *,
    form: schemas.UnitForm = Body(...),
    skip: int = Query(0),
    limit: int = Query(100),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Retrieve units with filters.
    """
    units = list()
    db_units = await crud.unit.search(db, form=form, skip=skip, limit=limit)
    for unit in db_units:
        units.append(
            unit_dict(
                unit_record=unit,
                amenities=await crud.unit.get_unit_amenities(db, model_id=unit.id),
            )
        )

    return units


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UnitOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def create_unit(
    *,
    unit: schemas.UnitIn = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Create new unit.
    """
    obj = await crud.unit.create(db, obj_in=unit)
    return unit_dict(
        unit_record=obj,
        amenities=await crud.unit.get_unit_amenities(db, model_id=obj.id),
    )


@router.get(
    "/{unit_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UnitOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_unit_by_id(
    *,
    unit_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Get a specific unit by id.
    """
    unit = await crud.unit.get(db, model_id=unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The unit with this id does not exist",
        )
    return unit_dict(
        unit_record=unit,
        amenities=await crud.unit.get_unit_amenities(db, model_id=unit.id),
    )


@router.patch(
    "/{unit_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UnitOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def update_unit(
    *,
    unit_id: int = Path(...),
    unit_in: schemas.UnitUpdate = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Update a unit.
    """
    unit = await crud.unit.get(db, model_id=unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The unit with this id does not exist",
        )
    return unit_dict(
        unit_record=await crud.unit.update(db, db_obj=unit, obj_in=unit_in),
        amenities=await crud.unit.get_unit_amenities(db, model_id=unit.id),
    )


@router.delete(
    "/{unit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_request_active_superuser)],
)
async def delete_unit(
    *,
    unit_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> None:
    """
    Delete a unit.
    """
    unit = await crud.unit.get(db, model_id=unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The unit with this id does not exist",
        )
    return await crud.unit.remove(db, model_id=unit_id)
