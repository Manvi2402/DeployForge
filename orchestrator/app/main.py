from fastapi import FastAPI
from app.tasks import deploy_repo

app = FastAPI()

@app.post("/deploy")
def deploy(repo_url: str):
    task = deploy_repo.delay(repo_url)

    return {
        "task_id": task.id,
        "status": "deployment queued"
    }