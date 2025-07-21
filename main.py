from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from analyser import analyse

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://jobmatch-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # FastAPI 앱 생성
# app = FastAPI(
#     title="JobMatch API", description="AI 이력서 매칭 분석 API", version="1.0.0"
# )


# 기본 엔드포인트
@app.get("/")
def read_root():
    return {"message": "JobMatch API가 실행 중입니다!"}


# 요청 데이터 구조
class AnalyseRequest(BaseModel):
    resume: str
    job_posting: str
    salary_expectation: int = None  # 희망연봉 (옵셔널)


# 응답 데이터 구조
class AnalyseResponse(BaseModel):
    overall_score: int
    category_scores: dict
    recommendation: str
    reasons: list[str]
    test: str


@app.post("/analyse", response_model=AnalyseResponse)
async def analyse_resume(request: AnalyseRequest):
    resp = await analyse(request.resume, request.job_posting)
    # 임시 응답
    return AnalyseResponse(
        overall_score=87,
        category_scores={"기술스택": 90, "경력": 85, "학력": 80},
        recommendation="지원 추천",
        reasons=["기술스택이 완벽히 일치합니다", "경력이 적절합니다"],
        test=resp
    )

    # 서버 실행 (개발용)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
