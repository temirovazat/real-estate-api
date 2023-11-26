from typing import Any, Dict, List, Union

from databases import Database
from sqlalchemy import delete

from app.crud.base import CRUDBase
from app.models import amenity, unit, unit_amenities
from app.schemas.unit import UnitForm, UnitIn, UnitUpdate


class CRUDUnit(CRUDBase[type(unit), UnitIn, UnitUpdate]):
    async def search(
        self, db: Database, *, form: UnitForm, skip: int = 0, limit: int = 100
    ) -> List[Any]:
        query = (
            self.model.select()
            .offset(skip)
            .limit(limit)
            .where(
                form.min_price <= self.model.c.price,
                self.model.c.price <= form.max_price,
                form.min_square <= self.model.c.square,
                self.model.c.square <= form.max_square,
                form.min_bedrooms <= self.model.c.bedrooms,
                self.model.c.bedrooms <= form.max_bedrooms,
                form.min_bathrooms <= self.model.c.bathrooms,
                self.model.c.bathrooms <= form.max_bathrooms,
            )
        )

        if form.amenities:
            q = unit_amenities.select().where(
                unit_amenities.c.amenity_id.in_(form.amenities)
            )
            amenities = await db.fetch_all(query=q)

            query = query.where(
                self.model.c.id.in_((record.unit_id for record in amenities))
            )

        return await db.fetch_all(query=query)

    async def get_unit_amenities(self, db: Database, *, model_id: int) -> Any:
        amenities = await db.fetch_all(
            unit_amenities.select().where(unit_amenities.c.unit_id == model_id)
        )
        return await db.fetch_all(
            amenity.select().where(
                amenity.c.id.in_([record.amenity_id for record in amenities])
            )
        )

    async def delete_unit_amenities(self, db: Database, *, model_id: int) -> None:
        await db.execute(
            delete(unit_amenities).where(unit_amenities.c.unit_id == model_id)
        )

    async def add_amenities_to_unit(
        self, db: Database, *, model_id: int, amenities: List[int]
    ) -> None:
        values = list()
        for amenity_id in amenities:
            values.append(dict(amenity_id=amenity_id, unit_id=model_id))

        await db.execute_many(unit_amenities.insert(), values=values)

    async def create(self, db: Database, *, obj_in: UnitIn) -> Any:
        obj_in_data = obj_in.dict(exclude_unset=True, exclude={"amenities"})
        db_query = self.model.insert().values(**obj_in_data)
        obj_id = await db.execute(db_query)

        await self.add_amenities_to_unit(
            db, amenities=obj_in.amenities, model_id=obj_id
        )

        return await self.get(db=db, model_id=obj_id)

    async def update(
        self, db: Database, *, db_obj: Any, obj_in: Union[UnitIn, Dict[str, Any]]
    ) -> Any:
        if isinstance(obj_in, dict):
            update_data = obj_in
            del update_data["amenities"]
        else:
            update_data = obj_in.dict(exclude_unset=True, exclude={"amenities"})

        amenities = obj_in.amenities
        if amenities:
            await self.delete_unit_amenities(db, model_id=db_obj.id)
            await self.add_amenities_to_unit(
                db, amenities=amenities, model_id=db_obj.id
            )

        return await super().update(db, db_obj=db_obj, obj_in=update_data)


unit = CRUDUnit(unit)
