from server.models.model import User, Repositories

def get_repository_user(db, repository_name):
    try:
        return db.query(Repositories).join(User).filter(Repositories.name == repository_name).all()
    except Exception as error:
        return None

def get_user_data(db, username):
    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as error:
        return None

def save_user_data(db, user_data, repositories):
    try:
        new_user = User()
        new_user.user_id = user_data["user_id"]
        new_user.username = user_data["username"]
        new_user.repositories = user_data["repositories"]
        db.add(new_user)
        db.flush()
        db.commit()
        for repo in repositories:
            new_repo = Repositories()
            new_repo.user_id = new_user.id
            new_repo.repo_id = repo["repo_id"]
            new_repo.url = repo["url"]
            new_repo.name = repo["name"]
            new_repo.access_type = repo["access_type"]
            new_repo.created_at = repo["created_at"]
            new_repo.updated_at = repo["updated_at"]
            new_repo.size = repo["size"]
            new_repo.stargazers_count = repo["stargazers_count"]
            new_repo.watchers_count = repo["watchers_count"]
            db.add(new_repo)
        db.flush()
        db.commit()
        return True
    except Exception as error:
        return None
    
def update_user_data(db, user_db, user_data, repositories):
    try:
        db.query(User).filter(User.id == user_db.id).update({
            "username": user_data["username"],
            "repositories": user_data["repositories"]
        })
        db.flush()
        db.commit()
        repositories_db = db.query(Repositories).filter(Repositories.user_id == user_db.id).all()
        repositories_db_list = [repositories_db[i].repo_id for i in range(len(repositories_db))]
        repositories_api_list = [repo_api["repo_id"] for repo_api in repositories]
        for repository_api in repositories:
            for repository_db in repositories_db_list:
                if repository_db == repository_api["repo_id"]:
                    db.query(Repositories).filter(Repositories.user_id == user_db.id, Repositories.repo_id == repository_db).update({
                        "url": repository_api["url"],
                        "name": repository_api["name"],
                        "access_type": repository_api["access_type"],
                        "created_at": repository_api["created_at"],
                        "updated_at": repository_api["updated_at"],
                        "stargazers_count": repository_api["stargazers_count"],
                        "watchers_count": repository_api["watchers_count"]
                        })
                    db.flush()
                    db.commit()
                else:
                    if repository_api["repo_id"] not in repositories_db_list:
                        new_repo = Repositories()
                        new_repo.user_id = user_db.id
                        new_repo.repo_id = repository_api["repo_id"]
                        new_repo.url = repository_api["url"]
                        new_repo.name = repository_api["name"]
                        new_repo.access_type = repository_api["access_type"]
                        new_repo.created_at = repository_api["created_at"]
                        new_repo.updated_at = repository_api["updated_at"]
                        new_repo.size = repository_api["size"]
                        new_repo.stargazers_count = repository_api["stargazers_count"]
                        new_repo.watchers_count = repository_api["watchers_count"]
                        db.add(new_repo)
                        db.flush()
                        db.commit()
                        repositories_db = db.query(Repositories).filter(Repositories.user_id == user_db.id).all()
                        repositories_db_list = [repositories_db[i].repo_id for i in range(len(repositories_db))]
                    elif repository_db not in repositories_api_list:
                        repository_remove = db.query(Repositories).filter(Repositories.repo_id == repository_db).all()
                        db.delete(repository_remove[0])
                        db.flush()
                        db.commit()
                        repositories_db = db.query(Repositories).filter(Repositories.user_id == user_db.id).all()
                        repositories_db_list = [repositories_db[i].repo_id for i in range(len(repositories_db))]
        return True
    except Exception as error:
        return None