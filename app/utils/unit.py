from typing import Any, Dict, List


def unit_dict(unit_record: Any, amenities: List[Any]) -> Dict[str, Any]:
    return dict(
        id=unit_record.id,
        description=unit_record.description,
        price=unit_record.price,
        square=unit_record.square,
        bedrooms=unit_record.bedrooms,
        bathrooms=unit_record.bathrooms,
        building_id=unit_record.building_id,
        amenities=[dict(id=amenity.id, name=amenity.name) for amenity in amenities],
    )
