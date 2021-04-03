import requests
from fastapi import HTTPException

class GitApi:
    def __init__(self, username):
      self.__username = username
      self.__url = 'https://api.github.com'
      self.__repo_data = []
    
    def get_user_info(self):
        url = self.__url + '/users/' + self.__username
        response_user = requests.get(url=url)
        if (response_user.status_code == 200):
            response = response_user.json()
            repo_list = self.__get_user_repositories(response["repos_url"])
            return {
                "user_id": response["id"],
                "username": response["login"],
                "repositories": repo_list
            }
        return None

        
    def __get_user_repositories(self, repos_url):
        repos_list = []
        response_url = requests.get(repos_url)
        if (response_url.status_code == 200):
            response = response_url.json()
            self.__save_repository_data(response)
            for repo in response:
                repos_list.append(repo["name"])
        return repos_list
    
    def __save_repository_data(self, data):
        for repo in data:
            self.__repo_data.append({
                "repo_id": repo["id"],
                "url": repo["html_url"],
                "name": repo["name"],
                "access_type": ("public" if repo["private"] == False else "private"),
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"],
                "size": repo["size"],
                "stargazers_count": repo["stargazers_count"],
                "watchers_count": repo["watchers_count"]
            })
        return self.__repo_data
    
    def return_repositories_data(self):
        return self.__repo_data
    
    @classmethod
    def get_repository_info(self, repositories, repository_name):
        for repository in repositories:
            if (repository["name"] == repository_name):
                return repository
        return None
