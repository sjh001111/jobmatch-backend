import asyncio
import os
from typing import List

from dotenv import load_dotenv
from google.genai import types

from gemini import Gemini
# from schema import JobEvaluationSchema

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
prompt = """
나에 대한 자료와 job description을 보고 적합성을 평가하고 지원할지 말지 결정해봐
"""


async def analyse(files: List, texts=List):
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

    res = await gemini.query(contents) # schema=None
    print(res.response)
    return res.response

async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())
