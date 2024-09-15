from pydantic import BaseModel


class Summary(BaseModel):
    url: str


class SummaryPayloadSchema(BaseModel):
    url: str


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int
