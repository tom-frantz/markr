import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from main import app, get_db, MARKR_CONTENT_TYPE
from src.schema import Analytics

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

# In production, this would most definitely point to a test database.
# TODO change this to a test database in production
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{POSTGRES_HOST}/stile"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_aggregate():
    res = client.get("/results/5678/aggregate")
    assert res.status_code == 200
    assert res.json() == Analytics(count=2, max=75, mean=62.5, min=50, p25=50, p50=50, p75=75, stddev=17.67766952966369)


def test_empty_aggregate():
    res = client.get("/results/5679/aggregate")
    assert res.status_code == 200
    assert res.json() == Analytics(count=0, max=0, mean=0, min=0, p25=0, p50=0, p75=0, stddev=0)


def test_import():
    with open("sample_results.xml") as fp:
        data = fp.read()

    res = client.post("/import", headers={"Content-Type": MARKR_CONTENT_TYPE}, data=data)

    assert res.status_code == 200


def test_import_broken_xml():
    # First tag is broken, deleted a bunch of stuff
    data = """
     <mcq-tes
   <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
     <first-name>Jane</first-name>
     <last-name>Austen</last-name>
     <student-number>521585128</student-number>
     <test-id>1234</test-id>
     <summary-marks available="20" obtained="13" />
   </mcq-test-result>
 </mcq-test-results>
    """
    res = client.post("/import", headers={"Content-Type": MARKR_CONTENT_TYPE}, data=data)
    assert res.status_code == 400
    assert res.json() == 'Malformed XML: Line: 3, Column: 3'


def test_import_missing_student_number():
    # delete student number
    data = """
     <mcq-test-results>
   <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
     <first-name>Jane</first-name>
     <last-name>Austen</last-name>
     <test-id>1234</test-id>
     <summary-marks available="20" obtained="13" />
   </mcq-test-result>
 </mcq-test-results>
    """
    res = client.post("/import", headers={"Content-Type": MARKR_CONTENT_TYPE}, data=data)
    assert res.status_code == 400
    assert res.json() == {'detail': 'Result 1: Student number not found'}


def test_import_missing_test_id():
    # delete student number
    data = """
     <mcq-test-results>
   <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
     <first-name>Jane</first-name>
     <last-name>Austen</last-name>
     <student-number>521585128</student-number>
     <summary-marks available="20" obtained="13" />
   </mcq-test-result>
 </mcq-test-results>
    """
    res = client.post("/import", headers={"Content-Type": MARKR_CONTENT_TYPE}, data=data)
    assert res.status_code == 400
    assert res.json() == {'detail': 'Result 1: Test ID not found'}


def test_import_missing_marks():
    # delete student number
    data = """
     <mcq-test-results>
   <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
     <first-name>Jane</first-name>
     <last-name>Austen</last-name>
     <student-number>521585128</student-number>
     <test-id>1234</test-id>
   </mcq-test-result>
 </mcq-test-results>
    """
    res = client.post("/import", headers={"Content-Type": MARKR_CONTENT_TYPE}, data=data)
    assert res.status_code == 400
    assert res.json() == {'detail': 'Result 1: Summary marks not found'}
