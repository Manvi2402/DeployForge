from fastapi import FastAPI
from app.routes import router
from app.database import deployments_collection
from pydantic import BaseModel
import httpx
import uuid
from datetime import datetime

app = FastAPI()

app.include_router(router)


class DeployRequest(BaseModel):
    repo_url: str


@app.get("/deployments")
def get_deployments():
    deployments = list(deployments_collection.find({}, {"_id": 0}))
    return deployments


@app.post("/deploy")
def deploy(request: DeployRequest):

    deployment_id = str(uuid.uuid4())

    deployments_collection.insert_one({
        "deployment_id": deployment_id,
        "repo_url": request.repo_url,
        "status": "queued",
        "container_id": None,
        "port": None,
        "created_at": datetime.utcnow()
    })

    httpx.post(
        "http://127.0.0.1:8001/orchestrate/deploy",
        params={"repo_url": request.repo_url}
    )

    return {
        "deployment_id": deployment_id,
        "status": "queued"
    }