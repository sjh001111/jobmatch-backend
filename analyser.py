import asyncio
import os
from typing import List

from dotenv import load_dotenv
from google.genai import types

from gemini import Gemini
from models import JobAnalysis

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

prompt = """
당신은 지원자의 약점을 찾아내는 데 특화된, 매우 냉소적이고 비판적인 채용 컨설턴트입니다. 당신의 목표는 지원자에게 헛된 희망을 주지 않고, 현실적인 약점을 정확히 짚어주는 것입니다.
아래의 채용 공고와 제 이력서를 비교하여 다음을 분석해주세요:
1. 레드 플래그(Red Flags): 채용 담당자가 이력서를 보고 즉시 우려할 만한 가장 큰 위험 요소는 무엇인가?
2. 핵심 불일치(Key Mismatches): 공고의 핵심 요구사항 중 내 이력서가 명백히 충족시키지 못하는 부분은 무엇인가?
3. 부족한 점 보완 전략: 위에서 지적된 약점들을 자기소개서나 면접에서 어떻게 방어하거나 보완해야 할지에 대한 현실적인 조언.
평가 시, 긍정적이거나 격려하는 어조는 완전히 배제하고, 오직 사실에 기반한 차갑고 직설적인 분석만 제공해주세요.
"""


async def analyse(files: List, texts=List, language="Korean"):
    model = "gemini-2.5-flash"
    gemini = Gemini(api_key, model)
    contents = [prompt]
    contents.extend(texts)
    for file in files:
        contents.append(
            types.Part.from_bytes(
                data=file,
                mime_type="application/pdf",
            )
        )

    res = await gemini.query(contents, schema=JobAnalysis, language=language)
    print(res)
    return res


async def main():
    resume_path = os.path.join("about_me", "Resume.pdf")
    job_posting_path = os.path.join("about_me", "sample_job_posting.txt")

    # Read resume file as bytes
    with open(resume_path, "rb") as f:
        resume_bytes = f.read()

    # Read job posting text
    with open(job_posting_path, "r", encoding="utf-8") as f:
        job_posting_text = f.read()

    # Test analysis
    files = [resume_bytes]
    texts = [job_posting_text]

    print("Testing with sample data...")

    result = await analyse(files, texts)
    print("Analysis result:", result)

    return result


if __name__ == "__main__":
    asyncio.run(main())
