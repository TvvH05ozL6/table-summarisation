import ast
import csv
import json
from multiprocessing import context
import uuid


import pycountry
from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie
from geopy.geocoders import Nominatim

from mantistablex.process.utils.assets import importer
from .forms import TableFromJSONForm, AnnotationFromJSONForm, FamiliarityInterestForm
from .models import Tables, Table_Datas, Table_Annotations, GlobalStatusEnum, GoldStandardsEnum, OcularMovement
import os
from mantistablex.viewfunctions.lexicalise import doLexicalisation
from mantistablex.viewfunctions.tripleviz import tripleviz

def coordinate_to_country(list_of_coords):
    geolocator = Nominatim(user_agent="mantistablex-1")
    location = geolocator.reverse(list_of_coords, timeout=10)
    country = pycountry.countries.get(alpha_2=location.raw["address"]["country_code"].upper())
    return country.name


def max_v_count(dictionary):
    max_count = max(len(v) for v in dictionary.values())
    max_value = [k for k, v in dictionary.items() if len(v) == max_count]
    return max_count, max_value


def oxford_comma(listed):
    if len(listed) == 0:
        return []
    if len(listed) == 1:
        return listed[0]
    if len(listed) == 2:
        listed[0][len(listed[0]) - 1] = listed[0][len(listed[0]) - 1][:-1]
        return listed[0] + ['and'] + listed[1][2:]
    else:
        result = list()
        for i in range(1, len(listed) - 1):
            listed[i][len(listed[i]) - 1] = listed[i][len(listed[i]) - 1][:-1]  # Remove final dot from sentence
            result = [','] + result + listed[i][2:]  # Add all sentences with a comma in between
        listed[0][len(listed[0]) - 1] = listed[0][len(listed[0]) - 1][:-1]  # Remove final dot from first sentence
        return listed[0] + result + ['and'] + listed[len(listed) - 1][2:]  # Add first and last sentence


def simple_comma(listed):
    if len(listed) == 0:
        return []
    if len(listed) == 1:
        return listed[0]
    if len(listed) == 2:
        return listed[0] + ' and ' + listed[1]
    return ', '.join(listed[:-1]) + ', and ' + listed[-1]


# Index
def index(request):
    string = 'text'
    context = {'text': string}
    return render(request, 'mantistablex/index.html', context)


# Home
def home(request):
    table_list = Tables.objects.order_by('-pub_date')
    tables_count = Tables.objects.count()

    num_elem = 25
    paginator = Paginator(table_list, num_elem)
    page = request.GET.get('page')
    tables = paginator.get_page(page)

    context = {
        'tables': tables,
        'tables_count': tables_count
    }

    return render(request, 'mantistablex/home.html', context)


# Show table
def show_table(request, table_id):
    table = get_object_or_404(Tables, id=table_id)
    table_data = Table_Datas.objects.get(table=table)

    data = []
    data_bootstrap = []

    # Extract data from table
    for row_idx in range(0, table.num_rows):
        row = []
        row_bootstrap = {}
        for col_idx, col in enumerate(table_data.data_original):
            row.append(col[row_idx]["value"])
            row_bootstrap[table_data.header[col_idx]] = col[row_idx]["value"]

        # data = [['Mount Everest', '8,848', 'Himalayas', 'May 29, 1953']]
        data.append(row)
        # data_bootstrap = [{'MOUNTAIN': 'Mount Everest', 'HEIGHT IN METERS': '8,848', 'RANGE': 'Himalayas', 'CONQUERED ON': 'May 29, 1953'}]
        data_bootstrap.append(row_bootstrap)

    annotations = dict()
    for a in Table_Annotations.objects.filter(table=table):
        if (a.gs_type).upper() == 'CPA':
            annotations.update({"CPA": ast.literal_eval(a.data)})
        elif (a.gs_type).upper() == 'CTA':
            annotations.update({"CTA": ast.literal_eval(a.data)})
        elif (a.gs_type).upper() == 'CEA':
            annotations.update({"CEA": ast.literal_eval(a.data)})
        # else:
        #     annotations.update({"Unokwn GS": ast.literal_eval(a.data)})

    request.session['annotations'] = annotations
    request.session['table_datas_bootstrap'] = data_bootstrap
    request.session['table_header_bootstrap'] = table_data.header

    context = {
        'table': table,
        'table_datas': data,
        'table_datas_bootstrap': data_bootstrap,
        'table_header_bootstrap': table_data.header,
        'table_header': table.header,
        'table_cols': 1 + table.num_cols,
        'table_rows': table.num_rows,
        'tables_count': Tables.objects.count(),
        'annotations': Table_Annotations.objects.filter(table=table),
        "annotations_complete": len(annotations) >= 3,
        'dic_annotations': annotations,
        'annotations_count': Table_Annotations.objects.filter(table=table).count(),
        'phase_name': 'start'
    }

    return render(request, 'mantistablex/tables/00-show.html', context)


# Experiments
def analyze_table(request, table_id):
    table = get_object_or_404(Tables, id=table_id)

    context = {
        'table': table
    }
    return render(request, 'mantistablex/experiments/analyze.html', context)


@ensure_csrf_cookie
def eye_tracking_table(request, table_id):
    table = get_object_or_404(Tables, id=table_id)
    table_data = Table_Datas.objects.get(table=table)

    if request.method == 'POST':
        results = request.POST.get("results", None)
        table_name = request.POST.get("table_name", None)
        try:
            jsonResults = json.loads(results)
            if results is not None:
                if len(jsonResults) > 0:
                    OcularMovement(
                        user=uuid.uuid4(),
                        results=jsonResults,
                        table_name=table_name
                    ).save()

                    return JsonResponse({"status": "ok"}, status=200)
                else:
                    return JsonResponse({"status": "failure"}, status=400)
        except:
            return JsonResponse({"status": "failure"}, status=400)
    else:
        data = []
        data_bootstrap = []
        for row_idx in range(0, table.num_rows):
            row = []
            row_bootstrap = {}
            for col_idx, col in enumerate(table_data.data_original):
                row.append(col[row_idx]["value"])
                row_bootstrap[table_data.header[col_idx]] = col[row_idx]["value"]

            data.append(row)
            data_bootstrap.append(row_bootstrap)

        context = {
            'table': table,
            'table_datas': data,
            'table_datas_bootstrap': data_bootstrap,
            'table_header_bootstrap': table_data.header
        }
        return render(request, 'mantistablex/experiments/eye-tracking.html', context)


def questionnaires(request, table_id):
    table = get_object_or_404(Tables, id=table_id)

    context = {
        'table': table
    }
    return render(request, 'mantistablex/experiments/questionnaires.html', context)


def select_familiarity(request, table_id):
    table = get_object_or_404(Tables, id=table_id)
    table_data = Table_Datas.objects.get(table=table)

    data = []
    data_bootstrap = []

    # Extract data from table
    for row_idx in range(0, table.num_rows):
        row = []
        row_bootstrap = {}
        for col_idx, col in enumerate(table_data.data_original):
            row.append(col[row_idx]["value"])
            row_bootstrap[table_data.header[col_idx]] = col[row_idx]["value"]

        # data = [['Mount Everest', '8,848', 'Himalayas', 'May 29, 1953']]
        data.append(row)
        # data_bootstrap = [{'MOUNTAIN': 'Mount Everest', 'HEIGHT IN METERS': '8,848', 'RANGE': 'Himalayas', 'CONQUERED ON': 'May 29, 1953'}]
        data_bootstrap.append(row_bootstrap)

    annotations = request.session.get('annotations')
    subject_col_index = annotations.get('CPA')[0][1]

    context = {
        'table': table,
        'table_datas': data,
        'table_datas_bootstrap': data_bootstrap,
        'table_header_bootstrap': table_data.header,
        'subject_index': subject_col_index,
        "familiarity_interest_form": FamiliarityInterestForm(
            initial={'familiarityChoices': 0, 'interestChoices': 1}),
    }

    return render(request, 'mantistablex/tables/01-select-familiarity.html', context)

def lexicalisation(request, table_id):
    context = doLexicalisation(request, table_id)
    return render(request, 'mantistablex/tables/03-summary.html', context)

def triples_viz(request, table_id):
    context = tripleviz(request, table_id)
    return render(request, 'mantistablex/tables/02-triples-viz.html', context)


# OTHER

def delete_table(request, table_id):
    table = Tables.objects.get(id=table_id)
    table.delete()
    table_list = Tables.objects.order_by('-pub_date')
    paginator = Paginator(table_list, 50)
    page = request.GET.get('page')

    tables = paginator.get_page(page)
    context = {'tables': tables}

    return render(request, 'mantistablex/home.html', context)


def delete_annotation(request, annotation_id):
    annotation = Table_Annotations.objects.get(id=annotation_id)
    table = annotation.table
    table_data = Table_Datas.objects.get(table=table)
    data = table_data.data_original
    header = table_data.header

    annotation.delete()

    data = []
    for row_idx in range(0, table.num_rows):
        row = []
        for col_idx, col in enumerate(table_data.data_original):
            # print(col[row_idx]["value"])
            row.append(col[row_idx]["value"])

        data.append(row)

    annotations = dict()

    for a in Table_Annotations.objects.filter(table=table):
        if (a.gs_type).upper() == 'CPA':
            annotations.update({"CPA": ast.literal_eval(a.data)})
        elif (a.gs_type).upper() == 'CTA':
            annotations.update({"CTA": ast.literal_eval(a.data)})
        elif (a.gs_type).upper() == 'CEA':
            annotations.update({"CEA": ast.literal_eval(a.data)})
        else:
            annotations.update({"Unokwn GS": ast.literal_eval(a.data)})

    request.session['annotations'] = annotations

    context = {
        'table': table,
        'table_datas': data,
        'table_header': table.header,
        'table_cols': table.num_cols,
        'tables_count': Tables.objects.count(),
        'annotations': Table_Annotations.objects.filter(table=table),
        'dic_annotations': annotations,
        'annotations_count': Table_Annotations.objects.filter(table=table).count(),
        'phase_name': 'start'
    }

    return render(request, 'mantistablex/tables/00-show.html', context)


# FROM MANTIS

def create_tables(request):
    invalid_file = False
    valid_file = False

    # state = ServerState.objects.get()

    if request.method == 'POST':
        form = TableFromJSONForm(request.POST, request.FILES)
        if form.is_valid():
            assert ('json_file' in request.FILES)

            # NOTE: Huge file could be bad for server performance
            # NOTE: What about chuncking the input?
            data = request.FILES['json_file'].file.read()
            file_name = request.FILES['json_file'].name
            table_name = request.POST.get('table_name')
            # Bad post request
            # if gs_type not in (gs.name for gs in GoldStandardsEnum):
            # return HttpResponseRedirect(reverse('home'))

            try:
                importer.load_table(table_name, file_name, data)
                valid_file = True
            except ValueError as e:
                invalid_file = True
    else:
        form = TableFromJSONForm()

    tables_completed_count = Tables.objects.filter(global_status=GlobalStatusEnum.DONE.value).count()
    tables_in_progress_count = Tables.objects.filter(global_status=GlobalStatusEnum.DOING.value).count()

    context = {
        'invalidfile': invalid_file,
        'validfile': valid_file,
        'form': form,
        'tables_count': Tables.objects.count(),
        'tables_completed': tables_completed_count,
        'tables_in_progress': tables_in_progress_count  # ,
        # 'standard_loaded': {
        #    "t2d": state.loaded_t2d,
        #    "limaye200": state.loaded_limaye200,
        #    "round2": state.loaded_round2
        # }
    }
    return render(request, 'mantistablex/tables/create-table.html', context)


def add_annotation(request, table_id):
    invalid_file = False
    valid_file = False
    t = get_object_or_404(Tables, id=table_id)

    if request.method == 'POST':
        form = AnnotationFromJSONForm(request.POST, request.FILES)
        if form.is_valid():
            assert ('json_file' in request.FILES)
            # NOTE: Huge file could be bad for server performance
            # NOTE: What about chuncking the input?

            # data = request.FILES['json_file'].file.read()
            data = []
            f = request.FILES['json_file']
            decoded_f = f.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_f)
            for row in reader:
                data.append(row)
            file_name = request.FILES['json_file'].name
            gs_type = request.POST.get('gs_type')

            # Bad post request
            if gs_type not in (gs.name for gs in GoldStandardsEnum):
                return HttpResponseRedirect(reverse('home'))

            try:
                importer.load_annotation(t, file_name, gs_type, data)
                valid_file = True
            except ValueError as e:
                invalid_file = True
        else:
            print(form.errors)
    else:
        form = AnnotationFromJSONForm()

    tables_completed_count = Tables.objects.filter(global_status=GlobalStatusEnum.DONE.value).count()
    tables_in_progress_count = Tables.objects.filter(global_status=GlobalStatusEnum.DOING.value).count()

    context = {
        'invalidfile': invalid_file,
        'validfile': valid_file,
        'form': form,
        'table': t
    }
    return render(request, 'mantistablex/tables/create-annotation.html', context)


def edit_annotation(request, annotation_id):
    invalid_file = False
    valid_file = False
    annotation = Table_Annotations.objects.get(id=annotation_id)
    t = annotation.table
    if request.method == 'POST':
        form = AnnotationFromJSONForm(request.POST, request.FILES)
        if form.is_valid():
            assert ('json_file' in request.FILES)
            # NOTE: Huge file could be bad for server performance
            # NOTE: What about chuncking the input?
            # data = request.FILES['json_file'].file.read()
            data = []
            f = request.FILES['json_file']
            decoded_f = f.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_f)
            for row in reader:
                data.append(row)
            file_name = request.FILES['json_file'].name
            gs_type = request.POST.get('gs_type')

            # Bad post request
            if gs_type not in (gs.name for gs in GoldStandardsEnum):
                return HttpResponseRedirect(reverse('home'))

            try:
                importer.edit_annotation(annotation_id, t, file_name, gs_type, data)
                valid_file = True
            except ValueError as e:
                invalid_file = True
        else:
            print(form.errors)
    else:
        form = AnnotationFromJSONForm()

    context = {
        'invalidfile': invalid_file,
        'validfile': valid_file,
        'form': form,
        'table': t,
        'annotation': Table_Annotations.objects.get(id=annotation_id)
        # 'annotation': Table_Annotations.objects.get(table=t)
    }
    return render(request, 'mantistablex/tables/edit-annotation.html', context)


def load_gs_tables(request):
    table_type = request.GET.get('type', None)

    # TODO: Could use enum for automatic mapping...
    if table_type == 't2d':
        task = importer.load_gs_tables.delay(GoldStandardsEnum.T2D.value)
    elif table_type == 'limaye200':
        task = importer.load_gs_tables.delay(GoldStandardsEnum.Limaye200.value)
    elif table_type == 'round2':
        task = importer.load_gs_tables.delay(GoldStandardsEnum.ROUND2.value)
    else:
        return {'error': 'wrong gs type'}

    response_data = {'task_id': task.id}
    return JsonResponse(response_data)


def delete_gs_tables(request):
    table_type = request.GET.get('type', None)

    # TODO: Could use enum for automatic mapping...
    if table_type == 't2d':
        task = importer.delete_gs_tables.delay(GoldStandardsEnum.T2D.value)
    elif table_type == 'limaye200':
        task = importer.delete_gs_tables.delay(GoldStandardsEnum.Limaye200.value)
    elif table_type == 'round2':
        task = importer.delete_gs_tables.delay(GoldStandardsEnum.ROUND2.value)
    else:
        return {'error': 'wrong gs type'}

    response_data = {'task_id': task.id}
    return JsonResponse(response_data)


def export(request):
    export_data = OcularMovement.objects.filter()

    return HttpResponse(serializers.serialize('json', export_data), content_type="application/json")
