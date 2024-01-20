# stdlib
from datetime import datetime

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.repository import MeasureSQLAlchemyRepository
from src.schemas import MeasurementInputSchema, MeasurementOutputSchema


async def save_measurement(session: AsyncSession, data: MeasurementInputSchema) -> None:
    await MeasureSQLAlchemyRepository(session).save_measurement(data)


async def get_last_measurement(session: AsyncSession) -> MeasurementOutputSchema | None:
    return await MeasureSQLAlchemyRepository(session).get_last_measurement()


async def get_measurements_by_time(
    session: AsyncSession, time_from: datetime, time_to: datetime
) -> list[MeasurementOutputSchema]:
    return await MeasureSQLAlchemyRepository(session).get_measurements_list(
        time_from, time_to
    )
