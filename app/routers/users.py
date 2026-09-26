from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.dependencies import get_users_collection
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


def user_doc_to_response(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "role": doc["role"],
    }


@router.get("", response_model=list[UserResponse])
def list_users(users_collection=Depends(get_users_collection)):
    users = list(users_collection.find())
    return [user_doc_to_response(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, users_collection=Depends(get_users_collection)):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_doc_to_response(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, users_collection=Depends(get_users_collection)):
    user_dict = user.model_dump()
    result = users_collection.insert_one(user_dict)
    created_user = users_collection.find_one({"_id": result.inserted_id})
    return user_doc_to_response(created_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, users_collection=Depends(get_users_collection)):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None