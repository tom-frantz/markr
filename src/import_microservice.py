from dataclasses import dataclass

from fastapi import HTTPException
from typing import Dict

from sqlalchemy.orm import Session

from src.database import engine
from src.schema import Import, McqTestResult
from src.models import Student, Result


@dataclass(frozen=True)
class ResultModelKey:
    student_number: str
    test_id: str


def get_marks(values: Import) -> Dict[ResultModelKey, McqTestResult]:
    working_results: Dict[ResultModelKey, McqTestResult] = {}

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
            if (
                marks.obtained > prev_marks.summary_marks.obtained
                or marks.available > prev_marks.summary_marks.available
            ):
                working_results[result_id] = result
        else:
            working_results[result_id] = result

    return working_results


def update_db_with_marks(marks: Dict[ResultModelKey, McqTestResult], db: Session):
    for key, results in marks.items():
        student = db.query(Student).filter_by(student_number=key.student_number).first()

        # Insert the student if not already present.
        if not student:
            student = Student(
                student_number=key.student_number,
                first_name=results.first_name,
                last_name=results.last_name,
            )
            db.add(student)
            db.commit()
            db.refresh(student)

        # See if there's an existing result (case where marked in another /import request)
        prev_result = (
            db.query(Result)
            .filter_by(student=student.student_number, test_id=key.test_id)
            .first()
        )

        # Handle persisting the new results;
        if not prev_result:
            insert_result(results, db)
        elif (
            results.summary_marks.available > prev_result.available
            or results.summary_marks.obtained > prev_result.obtained
        ):
            db.delete(prev_result)
            db.commit()
            insert_result(results, db)


def insert_result(result, db):
    db_result = Result(
        student=result.student_number,
        test_id=result.test_id,
        available=result.summary_marks.available,
        obtained=result.summary_marks.obtained,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
