from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.dependencies import get_comments_collection
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


def comment_doc_to_response(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "request_id": doc["request_id"],
        "author_id": doc["author_id"],
        "message": doc["message"],
    }


@router.get("", response_model=list[CommentResponse])
def list_comments_for_request(request_id: str, comments_collection=Depends(get_comments_collection)):
    comments = list(comments_collection.find({"request_id": request_id}))
    return [comment_doc_to_response(c) for c in comments]


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, comments_collection=Depends(get_comments_collection)):
    comment_dict = comment.model_dump()
    result = comments_collection.insert_one(comment_dict)
    created = comments_collection.find_one({"_id": result.inserted_id})
    return comment_doc_to_response(created)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: str, comments_collection=Depends(get_comments_collection)):
    result = comments_collection.delete_one({"_id": ObjectId(comment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return None