from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.dependencies import get_locations_collection
from app.schemas.location import LocationCreate, LocationResponse

router = APIRouter(prefix="/locations", tags=["Locations"])


def location_doc_to_response(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "building": doc["building"],
        "floor": doc["floor"],
        "room": doc.get("room", ""),
    }


@router.get("", response_model=list[LocationResponse])
def list_locations(locations_collection=Depends(get_locations_collection)):
    locations = list(locations_collection.find())
    return [location_doc_to_response(l) for l in locations]


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: str, locations_collection=Depends(get_locations_collection)):
    location = locations_collection.find_one({"_id": ObjectId(location_id)})
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location_doc_to_response(location)


@router.post("", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(location: LocationCreate, locations_collection=Depends(get_locations_collection)):
    location_dict = location.model_dump()
    result = locations_collection.insert_one(location_dict)
    created = locations_collection.find_one({"_id": result.inserted_id})
    return location_doc_to_response(created)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: str, locations_collection=Depends(get_locations_collection)):
    result = locations_collection.delete_one({"_id": ObjectId(location_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return None