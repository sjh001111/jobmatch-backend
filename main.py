from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from analyser import analyse


    # 응답 데이터 구조만 Pydantic 사용
class AnalyseResponse(BaseModel):
    overall_score: int
    category_scores: dict
    recommendation: str
    reasons: list[str]
    test: str


app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://jobmatch-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 기본 엔드포인트
@app.get("/")
def read_root():
    return {"message": "https://github.com/sjh001111"}


@app.post("/analyse", response_model=AnalyseResponse)
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
    resp = await analyse(files, texts)

    return AnalyseResponse(
        overall_score=87,
        category_scores={
            "Technical Skills": 90,
            "Experience": 85,
            "Education": 80,
            "Salary Match": 75,
        },
        recommendation="Recommended to Apply",
        reasons=[
            "Technical skills perfectly match job requirements",
            "Experience level is appropriate",
            f"Analysis language: {response_language}",
            (
                f"Expected salary: {expected_salary}"
                if expected_salary
                else "No salary specified"
            ),
        ],
        test=resp,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
