from typing import Optional, List
from pydantic import BaseModel, Field


# pydantic's BaseModel's should handle extra fields with grace.
class SummaryMarks(BaseModel):
    available: int = Field(None, alias="@available")
    obtained: int = Field(None, alias="@obtained")


class McqTestResult(BaseModel):
    student_number: str = Field(None, alias="student-number")
    test_id: str = Field(None, alias="test-id")
    summary_marks: SummaryMarks = Field(None, alias="summary-marks")

    # Add these as optional, good to have but not necessary.
    scanned_on: Optional[str] = Field(None, alias="@scanned-on")
    first_name: Optional[str] = Field(None, alias="first-name")
    last_name: Optional[str] = Field(None, alias="last-name")


class McqTestResultWrapper(BaseModel):
    mcq_test_results: List[McqTestResult] = Field(None, alias="mcq-test-result")


class Import(BaseModel):
    test: McqTestResultWrapper = Field(None, alias="mcq-test-results")


class EmptyResponse(BaseModel):
    class Config:
        orm_mode = True


# ANALYTICS
class Analytics(BaseModel):
    mean: float
    count: float

    p25: float
    p50: float
    p75: float

    stddev: float
    min: float
    max: float
