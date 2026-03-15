# # # # from app.worker import celery_app

# # # # @celery_app.task
# # # # def deploy_repo(repo_url):
# # # #     print(f"Deploying repository: {repo_url}")
# # # #     return {"status": "deployment started", "repo": repo_url}

# # # from app.worker import celery_app
# # # import os
# # # from git import Repo
# # # import uuid

# # # BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../deployments"))

# # # @celery_app.task
# # # def deploy_repo(repo_url):
    
# # #     deployment_id = str(uuid.uuid4())
# # #     repo_path = os.path.join(BASE_DIR, deployment_id)
# # #     os.makedirs(repo_path, exist_ok=True)

# # #     print("Base dir:", BASE_DIR)
# # #     print("Repo path:", repo_path)
# # #     print(f"Cloning repo: {repo_url}")
    
# # #     Repo.clone_from(repo_url, repo_path)

# # #     print(f"Repository cloned to {repo_path}")

# # #     return {
# # #         "status": "repository cloned",
# # #         "repo": repo_url,
# # #         "path": repo_path
# # #     }

# from app.worker import celery_app
# import os
# from git import Repo
# import uuid
# import docker

# # base deployments folder
# BASE_DIR = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "../../deployments")
# )

# # docker client
# docker_client = docker.from_env()


# @celery_app.task
# def deploy_repo(repo_url):

#     # unique deployment id
#     deployment_id = str(uuid.uuid4())

#     # repo path
#     repo_path = os.path.join(BASE_DIR, deployment_id)

#     # create folder
#     os.makedirs(repo_path, exist_ok=True)

#     print("Base dir:", BASE_DIR)
#     print("Repo path:", repo_path)

#     # clone repo
#     print(f"Cloning repo: {repo_url}")
#     Repo.clone_from(repo_url, repo_path)

#     print(f"Repository cloned to {repo_path}")

#     # docker image tag
#     image_tag = f"deployforge:{deployment_id}"

#     print("Building Docker image...")

#     # build docker image
#     image, logs = docker_client.images.build(
#         path=repo_path,
#         tag=image_tag,
#         rm=True,
#         forcerm=True
#     )

#     print("Docker image built successfully")

#     # run container
#     container = docker_client.containers.run(
#         image_tag,
#         detach=True,
#         ports={"3000/tcp": None}
#     )

#     print(f"Container started: {container.id}")

#     return {
#         "status": "deployment started",
#         "deployment_id": deployment_id,
#         "container_id": container.id
#     }
from app.worker import celery_app
from app.database import deployments_collection
from datetime import datetime
import os
from git import Repo
import uuid

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../deployments")
)


@celery_app.task
def deploy_repo(repo_url):

    deployment_id = str(uuid.uuid4())

    repo_path = os.path.join(BASE_DIR, deployment_id)

    os.makedirs(repo_path, exist_ok=True)

    print("Base dir:", BASE_DIR)
    print("Repo path:", repo_path)

    print(f"Cloning repo: {repo_url}")

    Repo.clone_from(repo_url, repo_path)

    print(f"Repository cloned to {repo_path}")
    # Save deployment in MongoDB
    deployments_collection.insert_one({
        "deployment_id": deployment_id,
        "repo_url": repo_url,
        "status": "cloned",
        "container_id": None,
        "port": None,
        "created_at": datetime.utcnow()
    })

    return {
        "status": "repository cloned",
        "deployment_id": deployment_id,
        "repo": repo_url
    }