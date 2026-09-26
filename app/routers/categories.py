from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.dependencies import get_categories_collection
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


def category_doc_to_response(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "description": doc.get("description", ""),
    }


@router.get("", response_model=list[CategoryResponse])
def list_categories(categories_collection=Depends(get_categories_collection)):
    categories = list(categories_collection.find())
    return [category_doc_to_response(c) for c in categories]


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str, categories_collection=Depends(get_categories_collection)):
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category_doc_to_response(category)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, categories_collection=Depends(get_categories_collection)):
    existing = categories_collection.find_one({"name": category.name})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already exists")
    category_dict = category.model_dump()
    result = categories_collection.insert_one(category_dict)
    created = categories_collection.find_one({"_id": result.inserted_id})
    return category_doc_to_response(created)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, categories_collection=Depends(get_categories_collection)):
    result = categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return None