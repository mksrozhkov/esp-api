# stdlib
from abc import ABC, abstractmethod
from datetime import datetime

# thirdparty
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.models import Measurement
from src.schemas import MeasurementInputSchema, MeasurementOutputSchema


class AbstractMeasureRepository(ABC):
    @abstractmethod
    async def save_measurement(self, measurement: MeasurementInputSchema) -> bool:
        pass

    @abstractmethod
    async def get_last_measurement(self) -> MeasurementOutputSchema:
        pass

    @abstractmethod
    async def get_measurements_list(
        self, time_from: datetime, time_to: datetime
    ) -> list[MeasurementOutputSchema]:
        pass


class MeasureSQLAlchemyRepository(AbstractMeasureRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_measurement(self, measurement: MeasurementInputSchema) -> None:
        new_measure = self._object_from_schema(measurement)
        self.session.add(new_measure)
        await self.session.commit()

    async def get_last_measurement(self) -> MeasurementOutputSchema | None:
        stmt = select(Measurement).order_by(Measurement.created_at.desc()).limit(1)
        result = await self.session.scalars(stmt)
        if not result:
            return None
        return self._schema_from_object(result.first())

    async def get_measurements_list(
        self, time_from: datetime, time_to: datetime
    ) -> list[MeasurementOutputSchema]:
        stmt = (
            select(Measurement)
            .where(
                Measurement.created_at >= time_from, Measurement.created_at <= time_to
            )
            .order_by(Measurement.created_at.desc())
        )
        result = await self.session.scalars(stmt)
        return [self._schema_from_object(measurement) for measurement in result]

    @staticmethod
    def _object_from_schema(measurement_schema: MeasurementInputSchema) -> Measurement:
        return Measurement(
            temp=measurement_schema.temp,
            humidity=measurement_schema.humidity,
            pressure=measurement_schema.pressure,
        )

    @staticmethod
    def _schema_from_object(measurement_data: Measurement) -> MeasurementOutputSchema:
        return MeasurementOutputSchema(
            created_at=measurement_data.created_at,
            temp=measurement_data.temp,
            humidity=measurement_data.humidity,
            pressure=measurement_data.pressure,
        )
