import asyncio
import os
import pathlib

from dotenv import load_dotenv
from google.genai import types

from gemini import Gemini

from schema import JobEvaluationSchema

prompt = """
나에 대한 자료와 job description을 보고 적합성을 평가하고 지원할지 말지 결정해봐
"""
job_description = """                   
Software engineer
Atlassian
3.0
9 reviews
·
View all jobs


Sydney NSW
Developers/Programmers (Information & Communication Technology)
Full time
Posted 32m ago

How you match
4 skills and credentials match your profile
 JavaScript Programming
 CSS
 Computer Science
+1 more⁠
Working at Atlassian

Atlassians can choose where they work – whether in an office, from home, or a combination of the two. That way, Atlassians have more control over supporting their family, personal goals, and other priorities. We can hire people in any country where we have a legal entity. Interviews and onboarding are conducted virtually, a part of being a distributed-first company.

In this role, you will:

Build high-performing client code that is fast, testable, scalable, and high quality

Drive strong collaboration with other engineers, designers and managers to understand user pain points and iterate on great solutions

Contribute to code reviews and documentation, and take on complex bug fixes

Lead projects, from the technical design, implementation and launch to operation

Onboard and mentor junior engineers

Your background:

2+ years experience with Javascript (ES6), HTML5, and CSS, as well as experience with modern Javascript frameworks (e.g., React, AngularJS, Vue).

Bachelor's or Master's degree (preferably a Computer Science degree or equivalent experience).

Understanding of modern frontend ecosystem, including but not limited to bundling, linting, testing and releasing.

Experience with modern testing frameworks (e.g., Jest, Cypress, Mocha, Chai).

Familiarity with the JavaScript language and ecosystem.

Experience building frontend applications at scale.

Experience in Agile software development methodologies.

You strive to write code that lasts for years, not months.

Experience engineering software systems of medium-to-large scope and complexity.

Atlassian offers a wide range of perks and benefits designed to support you, your family and to help you engage with your local community. Our offerings include health and wellbeing resources, paid volunteer days, and so much more. To learn more, visit go.atlassian.com/perksandbenefits.

About Atlassian

At Atlassian, we're motivated by a common goal: to unleash the potential of every team. Our software products help teams all over the planet and our solutions are designed for all types of work. Team collaboration through our tools makes what may be impossible alone, possible together.

We believe that the unique contributions of all Atlassians create our success. To ensure that our products and culture continue to incorporate everyone's perspectives and experience, we never discriminate based on race, religion, national origin, gender identity or expression, sexual orientation, age, or marital, veteran, or disability status. All your information will be kept confidential according to EEO guidelines.

To provide you the best experience, we can support with accommodations or adjustments at any stage of the recruitment process. Simply inform our Recruitment team during your conversation with them.

To learn more about our culture and hiring process, visit go.atlassian.com/crh.
"""


async def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    model = "gemini-2.5-flash"
    gemini = Gemini(api_key, model)

    about_me_dir = pathlib.Path("about_me")
    pdf_files = list(about_me_dir.glob("*.pdf"))

    contents = []

    for filepath in pdf_files:
        contents.append(
            types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type="application/pdf",
            )
        )

    contents.append(prompt)
    contents.append(job_description)

    test = await gemini.query(contents, schema=JobEvaluationSchema)
    print(test)


if __name__ == "__main__":
    asyncio.run(main())
