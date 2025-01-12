# app/services/ai_service.py
import google.generativeai as genai
from typing import List, Dict, Any
import logging
from app.core.config import settings
import json
from app.core.logger import l


class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("Gemini API key is not set")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def analyze_code(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes code using Gemini and returns structured feedback
        """
        l.info(f"Analyzing {file_data['filename']} with Gemini AI")
        prompt = self._create_analysis_prompt(file_data)

        try:
            response = await self._generate_analysis(prompt)

            if not response or not response.strip():
                l.warning("Empty response from Gemini")
                return self._create_empty_analysis(file_data["filename"])

            return self._parse_analysis_response(response, file_data["filename"])
        except Exception as e:
            l.error(f"Error analyzing {file_data['filename']}: {e}")
            return {
                "filename": file_data["filename"],
                "issues": [],
                "error": str(e)
            }
    def _create_empty_analysis(self, filename: str) -> Dict[str, Any]:
        return {
            "filename": filename,
            "issues": [],
            "summary": {
                "total_issues": 0,
                "critical_issues": 0,
                "general_feedback": "Analysis failed"
            }
        }

    def _create_analysis_prompt(self, file_data: Dict[str, Any]) -> str:
        return f"""
        Act as an expert code reviewer. Analyze the following code diff and provide detailed feedback.
        
        File: {file_data['filename']}
        Changes: +{file_data['additions']} -{file_data['deletions']} lines  
        
        Code Changes (diff):
        {file_data['patch']}
        
        Full File Content:
        {file_data.get('content', 'No content available')}
        
        Analyze for:
        1. Code Style and Best Practices
        2. Potential Bugs or Error Cases
        3. Performance Considerations
        4. Security Issues
        5. Test Coverage Suggestions
        
        For each issue found, provide:
        - Category (style/bug/performance/security/test)
        - Line Number
        - Description
        - Suggested Fix
        
        Format your response as a JSON object with the following structure:
        {{
            "issues": [
                {{
                    "category": "style",
                    "line_numbers": [123],
                    "description": "Description of the issue",
                    "suggestion": "How to fix it"
                }}
            ],
            "summary": {{
                "total_issues": 1,
                "critical_issues": 0,
                "general_feedback": "Overall feedback about the code"
            }}
        }}
        
        Make sure to escape any special characters in the JSON and provide valid JSON format.
        """

    async def _generate_analysis(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            if hasattr(response, 'text'):
                l.info("Gemini analysis generated successfully")
                return response.text
            else:
                l.error("Unexpected response format from Gemini")
                return json.dumps(self._create_empty_analysis("unknown"))
        except Exception as e:
            l.error(f"Gemini API error: {e}")
            return json.dumps(self._create_empty_analysis("unknown"))
        
    def _parse_analysis_response(self, response: str, filename: str) -> Dict[str, Any]:
        try:
            # Clean up the response string to ensure it's valid JSON
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            analysis = json.loads(cleaned_response)
            analysis["filename"] = filename
            
            if "issues" not in analysis:
                analysis["issues"] = []
            if "summary" not in analysis:
                analysis["summary"] = {
                    "total_issues": len(analysis["issues"]),
                    "critical_issues": 0,
                    "general_feedback": "Analysis completed"
                }
            l.debug(f"Parsed analysis: {json.dumps(analysis, indent=2)}")

            return analysis
        except json.JSONDecodeError as e:
            l.error(f"Failed to parse Gemini response: {e}\nResponse: {response}")
            return self._create_empty_analysis(filename)