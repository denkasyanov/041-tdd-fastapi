from pydantic import AnyHttpUrl, BaseModel


class Summary(BaseModel):
    url: str


class SummaryPayloadSchema(BaseModel):
    url: AnyHttpUrl


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int
