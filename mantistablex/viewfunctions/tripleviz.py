from django.shortcuts import get_object_or_404
from ..models import Tables, Table_Datas
import json

def tripleviz(request, table_id):
    table = get_object_or_404(Tables, id=table_id)
    annotations = request.session.get('annotations')
    table_data_bootstrap = request.session.get('table_datas_bootstrap')
    table_header_bootstrap = request.session.get('table_header_bootstrap')

    context = {
        'table': table,
        'table_datas_bootstrap': table_data_bootstrap,
        'table_header_bootstrap': table_header_bootstrap,
        "neural_network_output": ""
    }

    if request.method == 'POST':
        familiarity_choices = request.POST.get('familiarityChoices')
        interest_choices = request.POST.get('interestChoices')
        highlight_indexes = json.loads(request.POST['highlightIndexes'])
        context["familiarity"] = "low" if familiarity_choices == "0" else "high"
        context["interest"] = "low" if interest_choices == "0" else "high"

        request.session['familiarity'] = familiarity_choices
        request.session['interest'] = interest_choices

        cpa = annotations.get("CPA", [])
        id_subj = cpa[0][1]

        context['subject_index'] = id_subj

        predicates = {}
        entities = {}
        for ann in cpa:
            _, id_subj, id_obj, p = ann
            predicates[id_obj] = p
            entities[id_obj] = {}

        cta = annotations.get("CTA", [])
        concepts = {}
        for ann in cta:
            _, id_col, c = ann
            if c != "":
                concepts[id_col] = c

        table_data = Table_Datas.objects.get(table=table)
        data_original = table_data.data_original
        for id_col, cols in enumerate(data_original):
            id_col = str(id_col)
            for id_row, cell in enumerate(cols):
                id_row = str(id_row)
                cell = list(cell.items())[0][1]
                if id_col != id_subj and id_col in predicates: #and id_col not in concepts
                    entities[id_col][id_row] = cell

        cea = annotations.get("CEA", [])
        subject = {id_subj: {}}
        context["triples"] = []
        for ann in cea:
            print(ann)
            _, id_row, id_col, e = ann
            if id_col == id_subj:
                subject[id_subj][id_row] = e
            else:
                entities[id_col][id_row] = e
        print(subject)
        print(entities)
        for id_col in highlight_indexes["colIndexes"]:
            id_col = str(id_col)
            for id_row in highlight_indexes["rowIndexes"]:
                id_row = str(id_row)
                indexes = {
                    "row": id_row,
                    "col": id_col
                }
                print(id_col, id_row)
                if id_col != id_subj and id_row in subject[id_subj] and id_row in entities[id_col]:
                    context["triples"].append(
                        {
                            "indexes": indexes,
                            "triple":
                                {
                                    "sbj": subject[id_subj][id_row],
                                    "pred": predicates[id_col],
                                    "obj": entities[id_col][id_row]
                                }
                        }
                    )
                if id_col == id_subj and id_row in subject[id_subj]:
                    context["triples"].append(
                        {
                            "indexes": indexes,
                            "triple":
                                {
                                    "sbj": subject[id_subj][id_row],
                                    "pred": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                    "obj": concepts[id_col]
                                }
                        }
                    )
        request.session['triples'] = context["triples"]
    return context