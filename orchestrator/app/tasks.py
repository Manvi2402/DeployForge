# from app.worker import celery_app
# from app.database import deployments_collection
# from datetime import datetime
# import os
# from git import Repo
# import uuid

# BASE_DIR = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "../../deployments")
# )


# @celery_app.task
# def deploy_repo(repo_url, deployment_id):


#     repo_path = os.path.join(BASE_DIR, deployment_id)

#     os.makedirs(repo_path, exist_ok=True)

#     print("Base dir:", BASE_DIR)
#     print("Repo path:", repo_path)

#     print(f"Cloning repo: {repo_url}")

#     Repo.clone_from(repo_url, repo_path)

#     print(f"Repository cloned to {repo_path}")
#     deployments_collection.update_one(
#         {"deployment_id": deployment_id},
#         {
#             "$set": {
#                 "status": "cloned",
#                 "created_at": datetime.utcnow()
#             }
#         }
#     )


#     return {
#         "status": "repository cloned",
#         "deployment_id": deployment_id,
#         "repo": repo_url
#     }
from app.worker import celery_app
from app.database import deployments_collection
from datetime import datetime
import os
from git import Repo, GitCommandError

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../deployments")
)


@celery_app.task
def deploy_repo(repo_url, deployment_id):

    try:
        repo_path = os.path.join(BASE_DIR, deployment_id)

        os.makedirs(repo_path, exist_ok=True)

        print("Base dir:", BASE_DIR)
        print("Repo path:", repo_path)

        print(f"Cloning repo: {repo_url}")

        Repo.clone_from(repo_url, repo_path)

        print(f"Repository cloned to {repo_path}")

        # ✅ Success update
        deployments_collection.update_one(
            {"deployment_id": deployment_id},
            {
                "$set": {
                    "status": "cloned",
                    "created_at": datetime.utcnow()
                }
            }
        )

        return {
            "status": "repository cloned",
            "deployment_id": deployment_id,
            "repo": repo_url
        }

    except GitCommandError as e:
        print("Git error:", str(e))

        # ❌ Failed update
        deployments_collection.update_one(
            {"deployment_id": deployment_id},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e),
                    "created_at": datetime.utcnow()
                }
            }
        )

        return {
            "status": "failed",
            "deployment_id": deployment_id,
            "error": str(e)
        }

    except Exception as e:
        print("General error:", str(e))

        deployments_collection.update_one(
            {"deployment_id": deployment_id},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e)
                }
            }
        )

        return {
            "status": "failed",
            "deployment_id": deployment_id,
            "error": str(e)
        }