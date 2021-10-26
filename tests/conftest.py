"""
NOTE: throughout the file, you will see

for db in override_get_db()

this is because override_get_db() is a generator

To call the generator and close it when done, simply call it in a for loop
"""
from src.models import Student, Result
from tests.test_main import override_get_db


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.

    Delete all existing data, populate with some dummy data
    """
    for db in override_get_db():
        db.query(Result).delete()
        db.query(Student).delete()

        students = []
        for i in range(2):
            student = Student(
                student_number=f"1234{i}",
                first_name="Tom",
                last_name="Frantz",
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            students.append(student)

        for index, student in enumerate(students):
            result = Result(
                student=student.student_number,
                test_id="5678",
                available=20,
                obtained=(index + 1) * 5 + 5,  # Convoluted way to get 10, 15
            )
            db.add(result)
            db.commit()


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.

    Delete all existing data
    """
    for db in override_get_db():
        db.query(Result).delete()
        db.query(Student).delete()
