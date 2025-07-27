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
You are an experienced professional recruitment consultant. Based on my resume and the job posting below, please conduct a SWOT analysis of my candidacy. You must provide a balanced view, including both positive and negative aspects.
Strengths: What are my strongest assets compared to the job requirements?
Weaknesses: What are my clear weaknesses or areas of concern for a hiring manager?
Opportunities: How can I leverage my strengths during an interview, or what are the ways to mitigate my weaknesses?
Threats: What are the biggest risks in hiring me, or what strengths might other competing candidates have over me?
Avoid emotional encouragement or excessive criticism. Provide a cool-headed, constructive analysis based on facts.
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
