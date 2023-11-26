from typing import Any, List

from databases import Database
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app import crud, schemas
from app.api.deps import get_db_pg, get_request_active_superuser

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.BuildingOut],
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_buildings(
    *,
    skip: int = Query(0),
    limit: int = Query(100),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Retrieve buildings.
    """
    return await crud.building.get_multi(db, skip=skip, limit=limit)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.BuildingOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def create_building(
    *,
    building: schemas.BuildingIn = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Create new building.
    """
    db_building = await crud.building.get_by_name(db, name=building.name)
    if db_building:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The building with this international name already exists.",
        )
    return await crud.building.create(db, obj_in=building)


@router.get(
    "/{building_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.BuildingOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_building_by_id(
    *,
    building_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Get a specific building by id.
    """
    building = await crud.building.get(db, model_id=building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The building with this id does not exist",
        )
    return building


@router.patch(
    "/{building_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.BuildingOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def update_building(
    *,
    building_id: int = Path(...),
    building_in: schemas.BuildingUpdate = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Update a building.
    """
    building = await crud.building.get(db, model_id=building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The building with this id does not exist",
        )
    return await crud.building.update(db, db_obj=building, obj_in=building_in)


@router.delete(
    "/{building_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_request_active_superuser)],
)
async def delete_building(
    *,
    building_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> None:
    """
    Delete a building.
    """
    building = await crud.building.get(db, model_id=building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The building with this id does not exist",
        )
    return await crud.building.remove(db, model_id=building_id)
