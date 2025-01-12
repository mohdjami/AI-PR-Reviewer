from pydantic import BaseModel, HttpUrl

class PullRequestAnalysisRequest(BaseModel):
    repo_url: HttpUrl
    pr_number: int
    github_token: str | None = None
    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/mohdjami/transaction-management-system",
                "pr_number": 1,
                "github_token": "optional_github_token"
            }
        }       