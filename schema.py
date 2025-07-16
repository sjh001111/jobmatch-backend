from pydantic import BaseModel

from pydantic import BaseModel
from typing import Optional, List

VERY_HIGH = "매우 높음"
    HIGH = "높음"
    MEDIUM = "보통"
    LOW = "낮음"
    VERY_LOW = "매우 낮음"
    UNKNOWN = "알 수 없음"


class TechStackMatch(BaseModel):
    hard_skills_match: MatchLevel
    experience_level_match: MatchLevel
    required_vs_preferred_tech: MatchLevel
    overall_score: float

    def __str__(self) -> str:
        return (
            f"TechStackMatch(\n"
            f"  hard_skills_match={self.hard_skills_match.value},\n"
            f"  experience_level_match={self.experience_level_match.value},\n"
            f"  required_vs_preferred_tech={self.required_vs_preferred_tech.value},\n"
            f"  overall_score={self.overall_score}\n"
            f")"
        )


class CareerEducationMatch(BaseModel):
    years_experience_match: MatchLevel
    degree_requirement_match: MatchLevel
    relevant_projects_match: MatchLevel
    overall_score: float

    def __str__(self) -> str:
        return (
            f"CareerEducationMatch(\n"
            f"  years_experience_match={self.years_experience_match.value},\n"
            f"  degree_requirement_match={self.degree_requirement_match.value},\n"
            f"  relevant_projects_match={self.relevant_projects_match.value},\n"
            f"  overall_score={self.overall_score}\n"
            f")"
        )


class RoleFitMatch(BaseModel):
    job_title_alignment: MatchLevel
    job_duties_match: MatchLevel
    team_role_fit: MatchLevel
    overall_score: float

    def __str__(self) -> str:
        return (
            f"RoleFitMatch(\n"
            f"  job_title_alignment={self.job_title_alignment.value},\n"
            f"  job_duties_match={self.job_duties_match.value},\n"
            f"  team_role_fit={self.team_role_fit.value},\n"
            f"  overall_score={self.overall_score}\n"
            f")"
        )


class CompanyCultureMatch(BaseModel):
    company_size_fit: MatchLevel
    work_style_fit: MatchLevel
    mission_vision_alignment: MatchLevel
    overall_score: float

    def __str__(self) -> str:
        return (
            f"CompanyCultureMatch(\n"
            f"  company_size_fit={self.company_size_fit.value},\n"
            f"  work_style_fit={self.work_style_fit.value},\n"
            f"  mission_vision_alignment={self.mission_vision_alignment.value},\n"
            f"  overall_score={self.overall_score}\n"
            f")"
        )


class GrowthPotential(BaseModel):
    learning_opportunities: MatchLevel
    career_path_clarity: MatchLevel
    mentoring_available: MatchLevel
    overall_score: float

    def __str__(self) -> str:
        return (
            f"GrowthPotential(\n"
            f"  learning_opportunities={self.learning_opportunities.value},\n"
            f"  career_path_clarity={self.career_path_clarity.value},\n"
            f"  mentoring_available={self.mentoring_available.value},\n"
            f"  overall_score={self.overall_score}\n"
            f")"
        )


class CompensationBenefits(BaseModel):
    salary_range_fit: MatchLevel
    benefits_quality: MatchLevel
    work_life_balance: MatchLevel
    overall_score: float

    def __str__(self) -> str:
        return (
            f"CompensationBenefits(\n"
            f"  salary_range_fit={self.salary_range_fit.value},\n"
            f"  benefits_quality={self.benefits_quality.value},\n"
            f"  work_life_balance={self.work_life_balance.value},\n"
            f"  overall_score={self.overall_score}\n"
            f")"
        )


class JobEvaluationSchema(BaseModel):
    job_title: str
    company_name: str
    tech_stack_match: TechStackMatch
    career_education_match: CareerEducationMatch
    role_fit_match: RoleFitMatch
    company_culture_match: CompanyCultureMatch
    growth_potential: GrowthPotential
    compensation_benefits: CompensationBenefits
    visa_citizenship_requirements: Optional[str]
    security_clearance_needed: Optional[bool]
    location_match: MatchLevel
    overall_match_score: float
    recommendation: str
    key_strengths: List[str]
    key_concerns: List[str]

    def __str__(self) -> str:
        strengths_str = "\n    ".join([f'"{s}"' for s in self.key_strengths])
        concerns_str = "\n    ".join([f'"{s}"' for s in self.key_concerns])

        return (
            f"JobEvaluationSchema(\n"
            f"  job_title='{self.job_title}',\n"
            f"  company_name='{self.company_name}',\n"
            f"  tech_stack_match={self.tech_stack_match},\n"
            f"  career_education_match={self.career_education_match},\n"
            f"  role_fit_match={self.role_fit_match},\n"
            f"  company_culture_match={self.company_culture_match},\n"
            f"  growth_potential={self.growth_potential},\n"
            f"  compensation_benefits={self.compensation_benefits},\n"
            f"  visa_citizenship_requirements={self.visa_citizenship_requirements},\n"
            f"  security_clearance_needed={self.security_clearance_needed},\n"
            f"  location_match={self.location_match.value},\n"
            f"  overall_match_score={self.overall_match_score},\n"
            f"  recommendation='{self.recommendation}',\n"
            f"  key_strengths=[\n    {strengths_str}\n  ],\n"
            f"  key_concerns=[\n    {concerns_str}\n  ]\n"
            f")"
        )
