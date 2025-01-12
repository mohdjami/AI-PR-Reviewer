# 🚀 Code Review Agent

> An AI-powered code review system that helps teams ship better code faster

[![GitHub license](https://img.shields.io/github/license/yourusername/code-review-agent)](https://github.com/yourusername/code-review-agent/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/code-review-agent/blob/main/CONTRIBUTING.md)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/code-review-agent)](https://github.com/yourusername/code-review-agent/stargazers)

## 🌟 Overview

Code Review Agent is a powerful, AI-driven code review assistant that helps development teams maintain high code quality standards while saving precious review time. By combining the power of Google's Gemini Pro with sophisticated static analysis, it provides comprehensive, context-aware code reviews automatically.

### 🎯 Key Features

- **Intelligent Code Analysis**: Leverages Gemini Pro to understand code context and provide meaningful insights
- **Automated PR Reviews**: Automatically analyzes pull requests and provides detailed feedback
- **Multiple Analysis Dimensions**:
  - Code Style & Best Practices
  - Potential Bugs & Error Cases
  - Performance Considerations
  - Security Vulnerabilities
  - Test Coverage Suggestions
- **GitHub Integration**: Seamlessly integrates with GitHub workflows
- **Structured Feedback**: Provides clear, actionable feedback with line-specific suggestions
- **Configurable Rules**: Adapt the analysis to your team's coding standards
- **Fast & Scalable**: Built with FastAPI for high performance and scalability
- **Production-Ready Logging**: Enterprise-grade logging with JSON formatting and rotation

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A Gemini API key
- (Optional) GitHub token for higher API limits

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/code-review-agent.git
cd code-review-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### 🔧 Configuration

Create a `.env` file with the following variables:

```env
# Environment
ENVIRONMENT=development
DEBUG=true

# API Settings
HOST=0.0.0.0
PORT=8000

# External Services
GITHUB_API_TOKEN=your_github_token_here
GEMINI_API_KEY=your_gemini_api_key_here

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=json
```

## 📚 API Documentation

### Analyze Pull Request

```http
POST /api/v1/code-review/analyze-pr
```

Request body:
```json
{
  "repo_url": "https://github.com/username/repo",
  "pr_number": 123,
  "github_token": "optional_token"
}
```

Response:
```json
{
  "status": "success",
  "pr_info": {
    "title": "Feature: Add user authentication",
    "url": "https://github.com/username/repo",
    "number": 123,
    "author": "developer",
    "created_at": "2024-01-12T10:00:00Z"
  },
  "analysis": {
    "files": [...],
    "summary": {
      "total_files": 5,
      "total_issues": 12,
      "critical_issues": 2
    }
  }
}
```

## 🛠️ Architecture

The system is built with a modular architecture focusing on extensibility and maintainability:

```
app/
├── api/              # API routes and endpoints
├── core/             # Core functionality and configuration
├── schemas/          # Pydantic models for data validation
├── services/         # Business logic and external service integration
└── utils/            # Utility functions and helpers
```

### Key Components

- **FastAPI Application**: High-performance async web framework
- **Pydantic Models**: Type-safe data validation
- **GitHub Integration**: PR fetching and analysis
- **Gemini AI Service**: Code analysis and suggestion generation
- **Logging Service**: Structured logging with rotation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📋 Roadmap

- [ ] Add support for GitLab and Bitbucket
- [ ] Implement custom rule creation UI
- [ ] Add team collaboration features
- [ ] Integrate with CI/CD pipelines
- [ ] Add support for more programming languages
- [ ] Implement real-time analysis capabilities
- [ ] Add historical analysis and trends
- [ ] Implement team-based configurations

## 🌟 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Gemini](https://blog.google/technology/ai/gemini-api/)
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

## 🤖 Why Code Review Agent?

- **Save Time**: Automated initial review catches common issues
- **Improve Code Quality**: Consistent, thorough reviews every time
- **Reduce Review Fatigue**: Let AI handle the basics while humans focus on architecture and logic
- **Learn & Improve**: Get actionable suggestions to improve your code
- **Scale Your Team**: Maintain code quality as your team grows

## 📬 Contact & Support

- Create an issue for bug reports or feature requests
- Star the repo to show your support
- Follow the project for updates

---

<p align="center">Made with ❤️ by developers, for developers</p>