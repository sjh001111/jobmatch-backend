from typing import List, Optional

from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from analyser import analyse
from models import JobAnalysis

# class AnalyseResponse(BaseModel):
#     overall_score: int
#     category_scores: dict
#     recommendation: str
#     reasons: list[str]
#     test: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://jobmatch-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
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

    # 업로드된 파일들 처리
    resume_contents = []
    for file in resume_files:
        files.append(await file.read())
        # resume_contents.append(
        #     {
        #         "filename": file.filename,
        #         "content": content,
        #         "content_type": file.content_type,
        #     }
        # )

    if additional_files:
        for file in additional_files:
            files.append(await file.read())


    # 분석 함수 호출
    job_analysis = await analyse(files, texts)

    return job_analysis
    # return AnalyseResponse(
    #     overall_score=87,
    #     category_scores={
    #         "Technical Skills": 90,
    #         "Experience": 85,
    #         "Education": 80,
    #         "Salary Match": 75,
    #     },
    #     recommendation="Recommended to Apply",
    #     reasons=[
    #         "Technical skills perfectly match job requirements",
    #         "Experience level is appropriate",
    #         f"Analysis language: {response_language}",
    #         (
    #             f"Expected salary: {expected_salary}"
    #             if expected_salary
    #             else "No salary specified"
    #         ),
    #     ],
    #     test=resp,
    # )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
