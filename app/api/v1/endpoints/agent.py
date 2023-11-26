from typing import Any, List

from databases import Database
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app import crud, schemas
from app.api.deps import get_db_pg, get_request_active_superuser

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.AgentOut],
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_agents(
    *,
    skip: int = Query(0),
    limit: int = Query(100),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Retrieve agents.
    """
    return await crud.agent.get_multi(db, skip=skip, limit=limit)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AgentOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def create_agent(
    *,
    agent: schemas.AgentIn = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Create new agent.
    """
    db_agent = await crud.agent.get_by_user_id(db, user_id=agent.user_id)
    if db_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The agent with this user id name already exists.",
        )
    return await crud.agent.create(db, obj_in=agent)


@router.get(
    "/{agent_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AgentOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def read_agent_by_id(
    *,
    agent_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Get a specific agent by id.
    """
    agent = await crud.agent.get(db, model_id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The agent with this id does not exist",
        )
    return agent


@router.patch(
    "/{agent_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AgentOut,
    dependencies=[Depends(get_request_active_superuser)],
)
async def update_agent(
    *,
    agent_id: int = Path(...),
    agent_in: schemas.AgentUpdate = Body(...),
    db: Database = Depends(get_db_pg),
) -> Any:
    """
    Update an agent.
    """
    agent = await crud.agent.get(db, model_id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The agent with this id does not exist",
        )
    return await crud.agent.update(db, db_obj=agent, obj_in=agent_in)


@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_request_active_superuser)],
)
async def delete_agent(
    *,
    agent_id: int = Path(...),
    db: Database = Depends(get_db_pg),
) -> None:
    """
    Delete an agent.
    """
    agent = await crud.agent.get(db, model_id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The agent with this id does not exist",
        )
    return await crud.agent.remove(db, model_id=agent_id)
