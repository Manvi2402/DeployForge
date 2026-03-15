from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {"message": "DeployForge API Gateway running"}

@router.post("/deploy")
def deploy_repo(repo_url: str):
    return {
        "status": "received",
        "repo_url": repo_url
    }