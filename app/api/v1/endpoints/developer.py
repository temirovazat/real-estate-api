from typing import Any, List

from databases import Database
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app import crud, schemas
from app.api.deps import get_db_pg, get_request_active_superuser

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.DeveloperOut],
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_developers(
    *,
    skip: int = Query(0),
    limit: int = Query(100),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Retrieve developers.
    """
    return await crud.developer.get_multi(db, skip=skip, limit=limit)


@router.get(
    "/agents/{developer_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.AgentOut],
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_developer_agents(
    *,
    skip: int = Query(0),
    limit: int = Query(100),
    developer_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Retrieve developer agents.
    """
    return await crud.developer.get_agents(
        db, model_id=developer_id, skip=skip, limit=limit
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DeveloperOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def create_developer(
    *,
    developer: schemas.DeveloperIn = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Create new developer.
    """
    db_developer = await crud.developer.get_by_international_name(
        db, international_name=developer.international_name
    )
    if db_developer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The developer with this international name already exists.",
        )
    return await crud.developer.create(db, obj_in=developer)


@router.get(
    "/{developer_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DeveloperOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_developer_by_id(
    *,
    developer_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Get a specific developer by id.
    """
    developer = await crud.developer.get(db, model_id=developer_id)
    if not developer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The developer with this id does not exist",
        )
    return developer


@router.patch(
    "/{developer_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DeveloperOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def update_developer(
    *,
    developer_id: int = Path(...),
    developer_in: schemas.DeveloperUpdate = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Update a developer.
    """
    developer = await crud.developer.get(db, model_id=developer_id)
    if not developer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The developer with this id does not exist",
        )
    return await crud.developer.update(db, db_obj=developer, obj_in=developer_in)


@router.delete(
    "/{developer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_request_active_superuser)],
)
async def delete_developer(
    *,
    developer_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> None:
    """
    Delete a developer.
    """
    developer = await crud.developer.get(db, model_id=developer_id)
    if not developer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The developer with this id does not exist",
        )
    return await crud.developer.remove(db, model_id=developer_id)
