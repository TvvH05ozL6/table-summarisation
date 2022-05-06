import datetime
import json
import os
import random

from celery.result import AsyncResult

from app.celery import app
from mantistablex.models import Tables, Table_Datas, Table_Annotations, GlobalStatusEnum, PhasesEnum, GoldStandardsEnum
from mantistablex.process.utils.assets.assets import Assets
from mantistablex.process.utils.channels.internal import Internal

process = {
    "phases": {
        tag.value["key"]: {
            'name': tag.value["name"],
            'routeName': tag.value["key"],
            'status': GlobalStatusEnum.TODO.value,
            'next': idx == 0,
            'execution_time': str(datetime.timedelta(0)).split('.', 2)[0][3:]
        }
        for idx, tag in enumerate(PhasesEnum)
    },
    "execution_time": str(datetime.timedelta(0)).split('.', 2)[0][3:]
}


# TODO: Refactoring needed
def _create_table(table_name, file_name, gs_type, content):
    assert (len(table_name) > 0)
    assert (len(file_name) > 0)
    assert (len(content) > 0)

    print(file_name)
    json_data = json.loads(content)
    header = list(json_data[0].keys())

    table = Tables(
        name=table_name,
        gs_type=gs_type,
        file_name=file_name,
        header=header,
        num_cols=len(list(json_data[0].keys())),
        num_rows=len(json_data),
        process=process
    )

    def table_datas_builder(tab):
        datas = []
        for col_index in range(0, len(header)):
            data = []
            for i in range(0, len(json_data)):
                col_name = header[col_index]
                if col_name in json_data[i]:
                    data.append({
                        "value": json_data[i][col_name]
                    })
                else:
                    data.append({
                        "value": ""
                    })

            datas.append(data)

        return Table_Datas(
            table=tab,
            header=header,
            data_original=datas,#json_data,
            data=datas#json_data,
        )

    return table, table_datas_builder


def load_table(table_name, file_name, content):
    assert (len(table_name) > 0)
    assert (len(file_name) > 0)
    assert (len(content) > 0)

    print(file_name)
    json_data = json.loads(content)
    header = list(json_data[0].keys())

    table = Tables(
        name=table_name,
        file_name=file_name,
        header=header,
        num_cols=len(list(json_data[0].keys())),
        num_rows=len(json_data),
        process=process
    )
    table.save()
    print(header)
    print(len(header))

    datas = []
    for col_index in range(0, len(header)):
        x = []
        for i in range(0, len(json_data)):
            col_name = header[col_index]
            if col_name in json_data[i]:
                x.append({
                    "value": json_data[i][col_name]
                })
                print(x)
            else:
                x.append({
                    "value": ""
                })

        datas.append(x)

    Table_Datas(
        table=table,
        header=header,
        data_original=datas,
        data=datas,
    ).save()

def load_annotation(table, file_name, gs_type, content):
    assert (len(file_name) > 0)
    #assert (len(content) > 0)

    print(file_name)
    # json_data = json.loads(content)

    Table_Annotations.objects.create(
        table=table,
        file_name=file_name,
        gs_type=gs_type,
        data=content,
    )
    
    return
    
def edit_annotation(annotation_id, table, file_name, gs_type, content):
    # assert (len(file_name) > 0)
    # assert (len(content) > 0)

    print(file_name)
    # json_data = json.loads(content)

    annotation = Table_Annotations.objects.get(id=annotation_id)
    annotation.table = table
    if (len(file_name) > 0):
        annotation.file_name = file_name
    if (len(gs_type) > 0):
        annotation.gs_type = gs_type
    if (len(file_name) > 0):
        annotation.data = content
    annotation.save()
    
    return

# NOTE: gs_type is one of Table.LIMAYE200, Table.T2D, ecc...
@app.task(bind=True)
def load_gs_tables(self, gs_type):
    try:
        file_names = {
            GoldStandardsEnum.T2D.value: json.loads(Assets().get_asset("tables/T2Dv2/t2dTables.json")),
            GoldStandardsEnum.Limaye200.value: list(map(
                lambda path: os.path.splitext(os.path.basename(path))[0],
                Assets().list_files("tables/Limaye200/converted/"))
            ),
            GoldStandardsEnum.ROUND2.value: json.loads(Assets().get_asset("tables/Round2/round2Tables.json")),
        }.get(gs_type, [])

        if len(file_names) > 0:
            __load_gs_tables({  # Type,           "directory"
                                 GoldStandardsEnum.T2D.value: (GoldStandardsEnum.T2D, "T2Dv2"),
                                 GoldStandardsEnum.Limaye200.value: (GoldStandardsEnum.Limaye200, "Limaye200"),
                                 GoldStandardsEnum.ROUND2.value: (GoldStandardsEnum.ROUND2, "Round2")
                             }.get(gs_type, None), file_names)

            state = ServerState.objects.get()
            if gs_type == GoldStandardsEnum.T2D.value:
                state.loaded_t2d = True
            elif gs_type == GoldStandardsEnum.Limaye200.value:
                state.loaded_limaye200 = True
            elif gs_type == GoldStandardsEnum.ROUND2.value:
                state.loaded_round2 = True

            state.save()

            state = AsyncResult(self.request.id).state
            if state == "PENDING":
                state = "SUCCESS"
            Internal.general().notify_import_status(state)
        else:
            Internal.general().notify_import_status("FAILURE")
            return None
    except FileNotFoundError:
        Internal.general().notify_import_status("FAILURE")
        
        
@app.task(bind=True)
def load_round2_sample(self):
    try:
        file_names = json.loads(Assets().get_asset("tables/Round2/round2Tables.json"))
        file_names = random.sample(file_names, k=300)
        if len(file_names) > 0:
            __load_gs_tables((GoldStandardsEnum.ROUND2, "Round2"), file_names)

            state = ServerState.objects.get()
            state.loaded_round2 = True
            state.save()

            state = AsyncResult(self.request.id).state
            if state == "PENDING":
                state = "SUCCESS"
            Internal.general().notify_import_status(state)
        else:
            Internal.general().notify_import_status("FAILURE")
    except FileNotFoundError:
        Internal.general().notify_import_status("FAILURE")


def __load_gs_tables(gs_type, file_names):
    assert (gs_type is not None)
    assert (len(file_names) > 0)

    tables = []
    table_data_builders = []
    for i in range(0, len(file_names)):
        content = Assets().get_asset("tables/{gs}/converted/{file}.json".format(
            gs=gs_type[1],
            file=file_names[i],
        ))

        # load_table(file_names[i], "{file}.json".format(file=file_names[i]), gs_type[0], content)
        table, table_data_builder = _create_table(file_names[i], "{file}.json".format(file=file_names[i]), gs_type[0].value,
                                                  content)
        tables.append(table)
        table_data_builders.append(table_data_builder)

    curr_table_count = Table.objects.count()
    total_table_count = curr_table_count + len(tables)
    for i, table in enumerate(tables):
        table.save()
        table_data_builders[i](table).save()

        Internal.general().notify_import_progress(curr_table_count + i, table.gs_type, total_table_count)
        # Table.objects.bulk_create(tables)


# NOTE: gs_type is one of Table.LIMAYE200, Table.T2D, ecc...
@app.task(bind=True)
def delete_gs_tables(self, gs_type):
    Table.objects.filter(gs_type=gs_type).delete()

    state = ServerState.objects.get()
    if gs_type == GoldStandardsEnum.T2D.value:
        state.loaded_t2d = False
    elif gs_type == GoldStandardsEnum.Limaye200.value:
        state.loaded_limaye200 = False
    elif gs_type == GoldStandardsEnum.ROUND2.value:
        state.loaded_round2 = False

    state.save()

    state = AsyncResult(self.request.id).state
    if state == "PENDING":
        state = "SUCCESS"
    Internal.general().notify_import_status(state)
