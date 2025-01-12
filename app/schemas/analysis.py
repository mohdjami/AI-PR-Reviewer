from pydantic import BaseModel
from typing import List, Optional

class CodeIssue(BaseModel):
    type: str  # "style", "bug", "performance"
    line: int
    description: str
    suggestion: str
    
class FileAnalysis(BaseModel):
    name: str
    issues: List[CodeIssue] = []  # Default to an empty list
    
class AnalysisSummary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int

class CodeAnalysisResult(BaseModel):
    files: List[FileAnalysis]
    summary: AnalysisSummary