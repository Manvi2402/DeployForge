from fastapi import APIRouter
from pydantic import BaseModel,Field 
import uuid
import httpx

from app.database import deployments_collection
router = APIRouter()


class DeployRequest(BaseModel):
    repo_url: str = Field(..., min_length=1)


@router.get("/")
def home():
    return {"message": "DeployForge API Gateway running"}


@router.post("/deploy")
def deploy_repo(request: DeployRequest):
    
    #Step 1: Generate deployment_id (HAR request pe)
    deployment_id = str(uuid.uuid4())

    #Step 2: Save in MongoDB
    deployments_collection.insert_one({
        "deployment_id": deployment_id,
        "repo_url": request.repo_url,
        "status": "queued",
        "container_id": None,
        "port": None
    })

    # ✅ Step 3: Call Orchestrator
    try:
        httpx.post(
            "http://127.0.0.1:8001/orchestrate/deploy",
            json={
                "repo_url": request.repo_url,
                "deployment_id": deployment_id
            },
            timeout=5.0
        )
    except Exception as e:
        return {"status":"error",
                "message" :"Orchestrator not available"}

    # ✅ Step 4: Return response
    return {
        "deployment_id": deployment_id,
        "status": "queued",
        "message":"Deployment started"
    }
@router.get("/deployments")
def get_deployments():
    deployments = list(
        deployments_collection.find({}, {"_id": 0}.sort("created_at",-1))
    )
    return deployments


@router.delete("/deployment/{deployment_id}")
def delete_deployment(deployment_id: str):

    result = deployments_collection.delete_one({
        "deployment_id": deployment_id
    })
    print("Deleting:", deployment_id)
    print("Deleted count:", result.deleted_count)
    

    if result.deleted_count == 0:
        return {"status": "error",
                "error": "Deployment not found"}

    return {"status": "success",
            "message": "Deployment deleted successfully"}