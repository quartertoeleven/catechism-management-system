from cms_common.services.grade_schedule_service_interface import (
    GradeScheduleServiceInterface,
)
from cms_common.services.grade_service_interface import GradeServiceInterface
from cms_common.services.general_schedule_service_interface import (
    GeneralScheduleServiceInterface,
)
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.sync_grade_schedule_request import SyncGradeScheduleRequest
from models.sync_grade_schedule_response import SyncGradeScheduleResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SyncGradeScheduleHandler(BaseAsyncHandler):
    def __init__(
        self,
        grade_schedule_service: GradeScheduleServiceInterface,
        grade_service: GradeServiceInterface,
        general_schedule_service: GeneralScheduleServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._grade_schedule_service = grade_schedule_service
        self._grade_service = grade_service
        self._general_schedule_service = general_schedule_service
        self._session_factory = session_factory

    async def handle(
        self, body: SyncGradeScheduleRequest, translator: Translator
    ) -> SyncGradeScheduleResponse:
        async with self._session_factory() as session:
            grade = await self._grade_service.get_by_id(session, body.grade_id)
            if grade is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.grade_not_found"),
                )

            sources = await self._general_schedule_service.list_by_study_year(
                session, grade.study_year_id
            )

            # Filter the source set: activity type + optional date range.
            type_ids = set(body.schedule_activity_type_ids)
            filtered = []
            for source in sources:
                if source.schedule_activity_type_id not in type_ids:
                    continue
                source_date = source.start_at.date()
                if body.date_from is not None and source_date < body.date_from:
                    continue
                if body.date_to is not None and source_date > body.date_to:
                    continue
                filtered.append(source)

            existing = await self._grade_schedule_service.list_linked_by_general_ids(
                session,
                body.grade_id,
                [source.id for source in filtered],
            )

            created = 0
            updated = 0
            for source in filtered:
                schedule = existing.get(source.id)
                if schedule is None:
                    # Unmatched source rows create a fully-copied linked row;
                    # the info checkboxes only gate updates.
                    await self._grade_schedule_service.create(
                        session,
                        study_year_id=grade.study_year_id,
                        grade_id=grade.id,
                        general_schedule_id=source.id,
                        schedule_activity_type_id=source.schedule_activity_type_id,
                        name=source.name,
                        start_at=source.start_at,
                        end_at=source.end_at,
                        detail=source.detail,
                        is_attendence_check=source.is_attendence_check,
                    )
                    created += 1
                else:
                    # Unlinked / unfiltered grade rows are never touched here.
                    # Only re-sync stale rows: `source_snapshot_at` older than
                    # the source's `updated` means the source changed after the
                    # last pull. Fresh (snapshot >= updated) rows are skipped;
                    # a linked row without snapshot counts as stale.
                    snapshot = schedule.source_snapshot_at
                    if snapshot is not None and snapshot >= source.updated:
                        continue
                    self._grade_schedule_service.apply_sync(
                        schedule,
                        source,
                        sync_date=body.sync_date,
                        sync_name=body.sync_name,
                        sync_start_time=body.sync_start_time,
                        sync_end_time=body.sync_end_time,
                    )
                    updated += 1

            await session.commit()

        return SyncGradeScheduleResponse(created=created, updated=updated)
