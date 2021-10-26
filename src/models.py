from sqlalchemy import Column, ForeignKey, Integer, String

from .database import Base


class Student(Base):
    __tablename__ = "students"

    student_number = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)


class Result(Base):
    __tablename__ = "results"

    student = Column(
        String, ForeignKey("students.student_number"), primary_key=True, index=True
    )
    test_id = Column(String, primary_key=True, index=True)

    available = Column(Integer)
    obtained = Column(Integer)
