from enum import Enum
from typing import List

from pydantic import BaseModel


class MatchLevel(Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"
    UNKNOWN = "Unknown"


class Criteria(BaseModel):
    name: str
    match_level: MatchLevel
    comment: str


class JobAnalysis(BaseModel):
    company_name: str
    role_name: str
    role_fit: Criteria
    tech_stack: Criteria
    career_education: Criteria
    location_match: Criteria
    compensation_benefits: Criteria
    company_culture: Criteria
    growth_potential: Criteria
    total_match_level: MatchLevel
    key_strengths: List[str]
    key_concerns: List[str]

