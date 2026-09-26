from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.dependencies import get_attachments_collection
from app.schemas.attachment import AttachmentCreate, AttachmentResponse

router = APIRouter(prefix="/attachments", tags=["Attachments"])


def attachment_doc_to_response(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "request_id": doc["request_id"],
        "file_name": doc["file_name"],
        "file_url": doc["file_url"],
        "file_size": doc["file_size"],
    }


@router.get("", response_model=list[AttachmentResponse])
def list_attachments_for_request(request_id: str, attachments_collection=Depends(get_attachments_collection)):
    attachments = list(attachments_collection.find({"request_id": request_id}))
    return [attachment_doc_to_response(a) for a in attachments]


@router.post("", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
def create_attachment(attachment: AttachmentCreate, attachments_collection=Depends(get_attachments_collection)):
    attachment_dict = attachment.model_dump()
    result = attachments_collection.insert_one(attachment_dict)
    created = attachments_collection.find_one({"_id": result.inserted_id})
    return attachment_doc_to_response(created)


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attachment(attachment_id: str, attachments_collection=Depends(get_attachments_collection)):
    result = attachments_collection.delete_one({"_id": ObjectId(attachment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    return None