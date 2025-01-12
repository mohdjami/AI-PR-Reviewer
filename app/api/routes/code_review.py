# app/api/routes/code_review.py
from fastapi import APIRouter, HTTPException
from app.schemas.github import PullRequestAnalysisRequest
from app.services.github import GithubService
from app.services.analyzer import CodeAnalyzer
from typing import Dict, Any
import logging
from app.core.logger import l


router = APIRouter(prefix="/code-review", tags=["code-review"])

@router.post("/analyze-pr")
async def analyze_pull_request(request: PullRequestAnalysisRequest):
    try:
        # Initialize services
        github_service = GithubService(request.github_token)
        code_analyzer = CodeAnalyzer()
        
        # Get PR details
        l.info(f"Fetching PR details for {request.repo_url} #{request.pr_number}")
        pr_details = await github_service.pull_request_details(
            str(request.repo_url),
            request.pr_number
        )
        
        # Analyze each file
        analysis_results = []
        for file_data in pr_details["files"]:
            # Skip deleted files
            if file_data["status"] != "removed":
                try:
                    analysis = await code_analyzer.analyze_file(file_data)
                    analysis_results.append(analysis)
                except Exception as e:
                    l.error(f"Failed to analyze {file_data['filename']}: {e}")
                    analysis_results.append({
                        "name": file_data["filename"],
                        "issues": [],
                        "error": str(e)
                    })

        # Compile summary
        total_issues = sum(len(analysis.issues) for analysis in analysis_results)
        critical_issues = sum(
            len([issue for issue in analysis.issues if issue.type in ["bug", "security"]])
            for analysis in analysis_results
        )

        return {
            "status": "success",
            "pr_info": {
                "title": pr_details["title"],
                "url": request.repo_url,
                "number": request.pr_number,
                "author": pr_details["user"],
                "created_at": pr_details["created_at"]
            },
            "analysis": {
                "files": analysis_results,
                "summary": {
                    "total_files": len(analysis_results),
                    "total_issues": total_issues,
                    "critical_issues": critical_issues,
                }
            }
        }
        
    except Exception as e:
        l.error(f"PR analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/status/{task_id}")
async def get_analysis_status(task_id: str):
    """
    This will be implemented when we add Celery for background processing
    """
    return {
        "task_id": task_id,
        "status": "not_implemented"
    }

@router.get("/results/{task_id}")
async def get_analysis_results(task_id: str):
    """
    This will be implemented when we add Celery for background processing
    """
    return {
        "task_id": task_id,
        "status": "not_implemented"
    }