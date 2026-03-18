from fastapi import FastAPI
from app.tasks import deploy_repo
from pydantic import BaseModel
app = FastAPI()
class DeployRequest(BaseModel):
    repo_url: str
    deployment_id: str
@app.post("/orchestrate/deploy")
def deploy(request: DeployRequest):
    task = deploy_repo.delay(
        request.repo_url, 
        request.deployment_id)

    return {
        "task_id": task.id,
        "status": "deployment queued"
    }