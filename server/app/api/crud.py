from app.models.pydantic import SummaryPayloadSchema, SummaryUpdatePayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()
    return summary.id


async def get(id: int) -> dict | None:
    summary = await TextSummary.filter(id=id).first().values()
    return summary


async def get_all() -> list[dict]:
    summaries = await TextSummary.all().values()
    return summaries


async def delete(id: int) -> None:
    summary = await TextSummary.filter(id=id).first().delete()
    return summary


async def put(id: int, payload: SummaryUpdatePayloadSchema) -> dict | None:
    summary = await TextSummary.filter(id=id).update(url=payload.url, summary=payload.summary)

    if summary:
        updated_summary = await TextSummary.filter(id=id).first().values()
        return updated_summary
    return None
