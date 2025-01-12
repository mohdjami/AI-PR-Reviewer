from fastapi import APIRouter, HTTPException
from app.schemas.github import PullRequestAnalysisRequest

router = APIRouter(prefix="/code-review", tags=["code-review"])

@router.post("/analyze-pr")
async def analyze_pull_request(request: PullRequestAnalysisRequest):
    try:
        return {
            "status": "accepted",
            "message": "Analysis started",
            "pr_number": request.pr_number,
            "repo_url": str(request.repo_url)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.get("/health")
async def health_check():
    return {"status": "ok"}