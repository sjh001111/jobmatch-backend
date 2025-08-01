# JobMatch AI - Backend

AI-powered resume and job posting matching analysis API.

## Overview

This backend service analyzes the compatibility between resumes and job postings using AI to provide matching scores and recommendations across multiple evaluation categories.

## Tech Stack

- **Framework**: FastAPI
- **AI Model**: Google Gemini 2.5 Flash
- **Language**: Python 3.x
- **Data Validation**: Pydantic
- **Server**: Uvicorn

## Features

- Resume-job posting compatibility analysis
- Multi-dimensional evaluation (tech stack, experience, education, company culture, etc.)
- AI-powered matching using Google Gemini API
- RESTful API endpoints with CORS support

## Installation & Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file
GEMINI_API_KEY=your_gemini_api_key
```

3. Run the server:
```bash
python main.py
```

The server will be available at `http://localhost:8000`.

## Project Structure

```
backend/
├── main.py              # FastAPI app and routing
├── analyser.py          # Resume analysis logic
├── gemini.py            # Gemini API client
├── schema.py            # Data models and schemas
├── requirements.txt     # Python dependencies
└── README.md
```

## API Status

The API is currently under active development with endpoints and data structures subject to change.