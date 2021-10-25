from dataclasses import dataclass

from fastapi import HTTPException
from typing import Dict

from sqlalchemy.orm import Session

from src.schema import Import, SummaryMarks


@dataclass(frozen=True)
class ResultModelKey:
    student_number: str
    test_id: str


def get_marks(values: Import) -> Dict[ResultModelKey, SummaryMarks]:
    working_results: Dict[ResultModelKey, SummaryMarks] = {}

    for index, result in enumerate(values.test.mcq_test_results):
        result_id = ResultModelKey(result.student_number, result.test_id)

        prev_marks = working_results.get(result_id)
        marks = result.summary_marks

        if result.student_number is None:
            raise HTTPException(
                status_code=400, detail=f"Result {index + 1}: Student number not found"
            )

        if result.test_id is None:
            raise HTTPException(
                status_code=400, detail=f"Result {index + 1}: Test ID not found"
            )

        if marks is None:
            raise HTTPException(
                status_code=400,
                detail=f"Result {index + 1}: Summary marks not found",
            )

        if prev_marks is not None:
            # Handle cases where there's conflicting values in the one document.
            # TODO: will have to handle persisted conflicting results.
            if (
                marks.obtained > prev_marks.obtained
                or marks.available > prev_marks.available
            ):
                working_results[result_id] = marks
        else:
            working_results[result_id] = marks

    return working_results


def update_db_with_marks(marks: Dict[ResultModelKey, SummaryMarks], db: Session):
    print("MARKS", marks)
    pass
