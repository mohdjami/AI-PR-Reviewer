from github import Github
from github.PullRequest import PullRequest
from typing import List
import logging

logger = logging.getLogger(__name__)

class GithubService:
    def __init__(self, token: str | None = None):
        self.github = Github(token) if token else Github()

    # def get_pull_request(self, repo_url: str, pr_number: int) -> PullRequest:
    #     repo = self.github.get_repo(repo_url)
    #     return repo.get_pull(pr_number)

    # def get_pull_request_files(self, repo_url: str, pr_number: int) -> List[str]:
    #     pr = self.get_pull_request(repo_url, pr_number)
    #     return [file.filename for file in pr.get_files()]
    
    async def pull_request_details(self, repo_url: str, pr_number: int) -> dict:
        """
        Fetches pull request details including files and their content
        """
        try:
            # Extract owner and repo from URL
            # Example: https://github.com/mohdjami/transaction-management-system
            repo_full_name = repo_url.split('github.com/')[-1]
            logger.info(f"Fetching PR #{pr_number} from {repo_full_name}")
            
            repo = self.github.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            
            files = []
            for file in pr.get_files():
                file_data = {
                    "filename": file.filename,
                    "status": file.status,  # added, modified, removed
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch,  # The actual diff
                    "content": None
                }
                
                # Get full file content for modified/added files
                if file.status != "removed":
                    try:
                        content = repo.get_contents(file.filename, ref=pr.head.sha)
                        file_data["content"] = content.decoded_content.decode('utf-8')
                    except Exception as e:
                        logger.warning(f"Could not fetch content for {file.filename}: {e}")
                
                files.append(file_data)

            return {
                "id": pr.number,
                "title": pr.title,
                "description": pr.body,
                "state": pr.state,
                "created_at": pr.created_at.isoformat(),
                "user": pr.user.login,
                "files": files,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files
            }
            
        except Exception as e:
            logger.error(f"Error fetching PR details: {e}")
            raise Exception(f"Failed to fetch PR details: {str(e)}")