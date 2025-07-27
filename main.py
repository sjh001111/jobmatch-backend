from typing import List, Optional

from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from analyser import analyse
from models import JobAnalysis


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://jobmatch-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return RedirectResponse(url="https://github.com/sjh001111/jobmatch-backend")


@app.post("/analyse", response_model=JobAnalysis)
async def analyse_resume(
    job_posting: str = Form(...),
    expected_salary: Optional[str] = Form(None),
    additional_info: Optional[str] = Form(None),
    response_language: str = Form("korean"),
    resume_files: List[UploadFile] = File(...),
    additional_files: Optional[List[UploadFile]] = File(None),
):
    files = []
    texts = [job_posting]

    for file in resume_files:
        files.append(await file.read())

    if additional_files:
        for file in additional_files:
            files.append(await file.read())

    if expected_salary:
        texts.append(f"Expected salary: {expected_salary}")

    if additional_info:
        texts.append(f"Additional info: {additional_info}")

    job_analysis = await analyse(files, texts, language=response_language)

    return job_analysis


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
