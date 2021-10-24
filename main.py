import json
from collections import OrderedDict
from typing import Any, Optional, List

import uvicorn
import xmltodict
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

app = FastAPI()
MARKR_CONTENT_TYPE = "text/xml+markr"


class SummaryMarks(BaseModel):
    available: str = Field(None, alias="@available")
    obtained: str = Field(None, alias="@obtained")


class McqTestResult(BaseModel):
    scanned_on: str = Field(None, alias="@scanned-on")
    first_name: str = Field(None, alias="first-name")
    last_name: str = Field(None, alias="last-name")
    student_number: str = Field(None, alias="student-number")
    test_id: str = Field(None, alias="test-id")
    summary_marks: SummaryMarks = Field(None, alias="summary-marks")


class McqTestResultWrapper(BaseModel):
    mcq_test_result: List[McqTestResult] = Field(None, alias="mcq-test-result")


class Import(BaseModel):
    mcq_test_results: McqTestResultWrapper = Field(None, alias="mcq-test-results")


@app.middleware("http")
async def xml_to_json(request: Request, call_next):
    if request.headers.get("Content-Type") == MARKR_CONTENT_TYPE:
        # Update request receive function and _json field, as well as associated headers to convert from xml to json
        xml_body = await request.body()
        parse = xmltodict.parse(xml_body, force_list=("mcq-test-result",))
        print(parse)
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
                "text/xml+markr": {"schema": Import.schema()},
            },
            "required": True,
        },
    },
)
def read_root(request: Import):
    print(request)
    return request


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
