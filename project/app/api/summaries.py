import sys
import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("summaries")

from typing import List

from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import ( # isort:skip
    SummaryPayloadSchema, 
    SummaryResponseSchema, 
    SummaryUpdatePayloadSchema
)
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    logger.info('Creating new summary ...')
    summary_id = await crud.post(payload)
    logger.info(f'New summary id {summary_id} created')
    response_object = {"id": summary_id, "url": payload.url}
    logger.debug(f'returning response: {response_object}')
    return response_object


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int) -> SummarySchema:
    logger.info(f'Trying to get the summary {id}')
    summary = await crud.get(id)
    logger.info(f'summary: {summary}')
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()


@router.delete("/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(id: int) -> SummaryResponseSchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    await crud.delete(id)
    return summary


@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(id: int, payload: SummaryUpdatePayloadSchema) -> SummarySchema:
    summary = await crud.put(id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


