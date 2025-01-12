from fastapi import APIRouter, HTTPException
from app.schemas.github import PullRequestAnalysisRequest
from app.services.github import GithubService

router = APIRouter(prefix="/code-review", tags=["code-review"])

@router.post("/analyze-pr")
async def analyze_pull_request(request: PullRequestAnalysisRequest):
    try:
        # initiate the github service
        github_service = GithubService(request.github_token)
        # get the pull request details
        pr_details = await github_service.pull_request_details(str(request.repo_url), request.pr_number)
        # return the response
        return {
            "status": "accepted",
            "message": "Analysis started",
            "pr_number": request.pr_number,
            "repo_url": str(request.repo_url),
            "data": pr_details
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.get("/health")
async def health_check():
    return {"status": "ok"}