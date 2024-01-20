# stdlib
import logging
from datetime import date, datetime, time, timedelta

# thirdparty
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.database import get_session
from src.dependencies import client_key_auth, device_key_auth
from src.schemas import MeasurementInputSchema, MeasurementOutputSchema
from src.service import get_last_measurement, get_measurements_by_time, save_measurement

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck():
    return {"success": True}


@router.post(
    "/measurement",
    dependencies=[Depends(device_key_auth)],
)
async def store_measurement(
    data: MeasurementInputSchema, session: AsyncSession = Depends(get_session)
):
    logger.info("Сохранение данных", extra=data.model_dump())
    await save_measurement(session, data)
    return JSONResponse(
        {"status": "ok"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/last",
    dependencies=[Depends(client_key_auth)],
)
async def get_last(
    session: AsyncSession = Depends(get_session),
) -> MeasurementOutputSchema:
    last_measurement = await get_last_measurement(session)
    if not last_measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данные не найдены",
        )
    return last_measurement


@router.get(
    "/measurements-list",
    dependencies=[Depends(client_key_auth)],
)
async def get_measurements_list(
    date_from: date | None = None,
    date_to: date | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[MeasurementOutputSchema]:
    time_from = (
        datetime.combine(date_from, time())
        if date_from
        else datetime.now() - timedelta(days=1)
    )
    time_to = (
        datetime.combine(date_to, time()) + timedelta(days=1)
        if date_to
        else datetime.now()
    )
    return await get_measurements_by_time(session, time_from, time_to)
