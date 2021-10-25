import json
from typing import Dict, Tuple

import xmltodict

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from src import models
from src.database import engine, SessionLocal
from src.import_microservice import get_marks, ResultModelKey, update_db_with_marks
from src.schema import Import, EmptyResponse, SummaryMarks, McqTestResult

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
MARKR_CONTENT_TYPE = "text/xml+markr"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def xml_to_json(request: Request, call_next):
    if request.headers.get("Content-Type") == MARKR_CONTENT_TYPE:
        # Update request receive function and _json field, as well as associated headers to convert from xml to json
        xml_body = await request.body()
        parse = xmltodict.parse(xml_body, force_list=("mcq-test-result",))
        json_string = json.dumps(parse).encode("utf-8")

        async def receive():
            return {"type": "http.request", "body": json_string}

        scope = request.scope
        scope["headers"] = [
            [b"content-type", b"application/json"]
            if header[0] != "content-type"
            else header
            for header in scope["headers"]
        ]

        # Create a new request object with the modifications
        request = Request(scope, receive, request._send)
        request._json = json.loads(
            json.dumps(xmltodict.parse(xml_body)).encode("utf-8")
        )

    response = await call_next(request)
    return response


@app.post(
    "/import",
    openapi_extra={
        "requestBody": {
            "content": {
                "text/xml+markr": {"schema": EmptyResponse.schema()},
            },
            "required": True,
        },
    },
    response_model=EmptyResponse,
)
def import_microservice(data: Import, db: Session = Depends(get_db)):
    working_results: Dict[ResultModelKey, McqTestResult] = get_marks(data)

    update_db_with_marks(working_results, db)

    return {}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
