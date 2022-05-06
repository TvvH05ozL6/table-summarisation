import datetime

from mantistablex.models import Tables, GlobalStatusEnum
from mantistablex.process.utils.channels.channel import Channel


class Internal(Channel):
    def __init__(self, channel_id):
        super().__init__(channel_id, "internal")

    @staticmethod
    def general():
        return Internal("general")

    @staticmethod
    def table(table_id: int):
        return Internal(table_id)

    def notify_task_end(self, task_id):
        self.send({
            'type': 'task_end',
            'task_id': task_id,
        })

    def notify_completed_table(self, last_completed_table_id, elapsed_time: datetime.timedelta, total_jobs_completed: int):
        self.send({
            'type': 'completed_table',
            'last_completed_table_id': last_completed_table_id,
            'elapsed': str(elapsed_time),
            'completed': total_jobs_completed,
        })

    def notify_started_phase(self, phase_key: str):
        assert (len(phase_key) > 0)

        self.send({
            'type': 'started_phase',
            'phase': phase_key
        })

    def notify_completed_phase(self, phase_key: str):
        assert (len(phase_key) > 0)

        self.send({
            'type': 'completed_phase',
            'phase': phase_key
        })

    def notify_started_process_all(self):
        server_state = ServerState.objects.first()
        self.send({
            'type': 'started_process_all',
            'process_all_task_id': server_state.current_process_all_task_id,
            'processing_tables_count': server_state.current_tables_in_progress,
        })

    def notify_table_state_changed(self, table_id):
        table = Table.objects.get(id=table_id)
        tables_completed_count = Table.objects.filter(global_status=GlobalStatusEnum.DONE.value).count()
        tables_in_progress_count = Table.objects.filter(global_status=GlobalStatusEnum.DOING.value).count()
        self.send({
            'type': 'table_state_changed',
            'table_id': table_id,
            'global_state': table.global_status,
            'process_state': {key: table.process["phases"][key]["status"] for key in table.process["phases"].keys()},
            'tables_completed_count': tables_completed_count,
            'tables_in_progress_count': tables_in_progress_count,
            'last_edit': table.last_edit_date.strftime("%d/%m/%Y - %H:%M:%S"),
        })

    def notify_import_progress(self, curr_table_count, table_gs_type, total_table_count):
        self.send({
            'type': 'import_progress',
            'table_gs_type': table_gs_type,
            'current_table_count': curr_table_count,
            'total_table_count': total_table_count,
        })

    def notify_import_status(self, status: str):
        self.send({
            'type': 'import_status',
            'status': status
        })

    def notify_delete_all_finished(self, deleted_tables: int):
        self.send({
            'type': 'delete_all_finished',
            'deleted_tables': deleted_tables
        })

