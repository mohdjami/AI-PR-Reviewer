from github import Github
from github.PullRequest import PullRequest
from typing import List

class GithubService:
    def __init__(self, token: str | None = None):
        self.github = Github(token) if token else Github()

    # def get_pull_request(self, repo_url: str, pr_number: int) -> PullRequest:
    #     repo = self.github.get_repo(repo_url)
    #     return repo.get_pull(pr_number)

    # def get_pull_request_files(self, repo_url: str, pr_number: int) -> List[str]:
    #     pr = self.get_pull_request(repo_url, pr_number)
    #     return [file.filename for file in pr.get_files()]
    
    def pull_request_details(self, repo_url: str, pr_number: int) -> dict:
        try:
            # Extract owner and repo from URL
            # Example: https://github.com/mohdjami/transaction-management-system
            # becomes: mohdjami/transaction-management-system
            repo_full_name = repo_url.split("github.com/")[-1]

            # Get the pull request
            repo = self.github.get_repo(repo_full_name)

            pr = repo.get_pull(pr_number)

            files = pr.get_files()

            return {
                "title": pr.title,
                "description": pr.body,
                "files": [
                    {
                        "filename": file.filename,
                        "changes": file.changes,
                        "additions": file.additions,
                        "deletions": file.deletions,
                        "content": file.patch
                    } for file in files
                ]
            }
        except Exception as e:
            return {
                "Error fetching the PR": str(e)
            }