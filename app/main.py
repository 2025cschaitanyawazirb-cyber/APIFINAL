from fastapi import FastAPI

from app.routers import users, categories, requests, comments, attachments, audit_logs, locations

app = FastAPI(title="Corporate Facility Desk API")

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(requests.router)
app.include_router(comments.router)
app.include_router(attachments.router)
app.include_router(audit_logs.router)
app.include_router(locations.router)


@app.get("/")
def root():
    return {"message": "Corporate Facility Desk API is running"}