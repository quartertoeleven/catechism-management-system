from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cms_db_models.study_year import Grade, GradeSchedule, Unit
from cms_common.services.grade_service_interface import GradeServiceInterface


class GradeService(GradeServiceInterface):
    async def list_by_study_year(
        self, session: AsyncSession, study_year_id: UUID
    ) -> list[Grade]:
        result = await session.execute(
            select(Grade)
            .where(Grade.study_year_id == study_year_id)
            .order_by(Grade.code)
        )
        return list(result.scalars().all())

    async def get_by_code(self, session: AsyncSession, code: str) -> Grade | None:
        result = await session.execute(select(Grade).where(Grade.code == code))
        return result.scalar_one_or_none()

    async def get_by_id(self, session: AsyncSession, grade_id: UUID) -> Grade | None:
        result = await session.execute(select(Grade).where(Grade.id == grade_id))
        return result.scalar_one_or_none()

    async def update(
        self,
        session: AsyncSession,
        grade: Grade,
        *,
        name: str,
        leader_catechist_id: UUID | None,
        vice_leader_catechist_id: UUID | None,
        secretary_catechist_id: UUID | None,
        treasurer_catechist_id: UUID | None,
    ) -> Grade:
        grade.name = name
        grade.leader_catechist_id = leader_catechist_id
        grade.vice_leader_catechist_id = vice_leader_catechist_id
        grade.secretary_catechist_id = secretary_catechist_id
        grade.treasurer_catechist_id = treasurer_catechist_id
        return grade

    async def has_dependents(self, session: AsyncSession, grade_id: UUID) -> bool:
        unit_id = await session.execute(
            select(Unit.id).where(Unit.grade_id == grade_id).limit(1)
        )
        if unit_id.first() is not None:
            return True
        schedule_id = await session.execute(
            select(GradeSchedule.id).where(GradeSchedule.grade_id == grade_id).limit(1)
        )
        return schedule_id.first() is not None

    async def delete(self, session: AsyncSession, grade: Grade) -> None:
        await session.delete(grade)

    async def create(
        self,
        session: AsyncSession,
        *,
        study_year_id: UUID,
        code: str,
        name: str,
        leader_catechist_id: UUID | None,
        vice_leader_catechist_id: UUID | None,
        secretary_catechist_id: UUID | None,
        treasurer_catechist_id: UUID | None,
    ) -> Grade:
        grade = Grade(
            study_year_id=study_year_id,
            code=code,
            name=name,
            leader_catechist_id=leader_catechist_id,
            vice_leader_catechist_id=vice_leader_catechist_id,
            secretary_catechist_id=secretary_catechist_id,
            treasurer_catechist_id=treasurer_catechist_id,
        )
        session.add(grade)
        return grade
