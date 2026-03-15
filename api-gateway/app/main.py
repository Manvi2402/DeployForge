from fastapi import FastAPI
from app.routes import router

from app.database import deployments_collection
app = FastAPI()

app.include_router(router)
@app.get("/deployments")
def get_deployments():

    deployments = list(deployments_collection.find({}, {"_id": 0}))

    return deployments