# app/services/analyzer.py
from typing import List, Dict, Any
from app.services.ai_service import GeminiService
from app.schemas.analysis import FileAnalysis, CodeIssue
from app.core.logger import l
class CodeAnalyzer:
    def __init__(self):
        self.ai_service = GeminiService()

    async def analyze_file(self, file_data: Dict[str, Any]) -> FileAnalysis:
        """
        Analyzes a single file using the Gemini service
        """
        try:
            # Get analysis from AI service
            raw_analysis = await self.ai_service.analyze_code(file_data)
            issues = []
            if isinstance(raw_analysis, dict) and 'issues' in raw_analysis:
                for issue in raw_analysis['issues']:
                    issues.append(CodeIssue(
                        type=issue.get('category', 'unknown'),
                        line=issue.get('line_numbers', [0])[0],  # Take first line number
                        description=issue.get('description', ''),
                        suggestion=issue.get('suggestion', '')
                    ))

            return FileAnalysis(
                name=file_data['filename'],
                issues=issues
            )

        except Exception as e:
            l.error(f"Error analyzing file {file_data.get('filename')}: {e}")
            raise Exception(f"Error in code analysis: {str(e)}")