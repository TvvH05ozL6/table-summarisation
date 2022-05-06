from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import JSONField
from djongo.models.json import JSONField
import json, uuid

from enum import Enum


class MongoJSONField(JSONField):
    def to_python(self, value):
        if isinstance(value,str):
            value = json.load(value)
        return super().to_python(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return str(value)

class Tables(models.Model):
    LIMAYE200 = 'Limaye200'
    T2D = 'T2D'
    CTA = 'CTA'
    CEA = 'CEA'
    CPA = 'CPA'
    NONE = 'NONE'
    GOLD_STANDARD_CHOICES = (
        (LIMAYE200, 'Limaye200'),
        (T2D, 'T2D'),
        (CTA, 'CTA'),
        (CEA, 'CEA'),
        (CPA, 'CPA'),
        (NONE, 'None'),
    )
    name = models.CharField(max_length=200)
    gs_type = models.CharField(max_length=10, choices=GOLD_STANDARD_CHOICES, default=NONE)
    file_name = models.TextField()
    global_status = models.CharField(max_length=5)
    process = JSONField(null=True, blank=True)
    pub_date = models.DateTimeField(default=now)
    last_edit_date = models.DateTimeField(default=now)
    header = models.TextField(default="")
    num_cols = models.PositiveIntegerField(default=0)
    num_rows = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Table_Datas(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    # index = models.PositiveIntegerField(default=0)
    # prefscore = models.IntegerField(default=0)
    header = JSONField()#models.TextField(default="")
    # data_original = MongoJSONField()
    # data = MongoJSONField()
    data_original = JSONField()#models.TextField(default="")
    data = JSONField()#models.TextField(default="")

class Table_Annotations(models.Model):
    LIMAYE200 = 'Limaye200'
    T2D = 'T2D'
    CTA = 'CTA'
    CEA = 'CEA'
    CPA = 'CPA'
    NONE = 'NONE'
    GOLD_STANDARD_CHOICES = (
        (LIMAYE200, 'Limaye200'),
        (T2D, 'T2D'),
        (CTA, 'CTA'),
        (CEA, 'CEA'),
        (CPA, 'CPA'),
        (NONE, 'None'),
    )
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    file_name = models.TextField()
    gs_type = models.CharField(max_length=10, choices=GOLD_STANDARD_CHOICES, default=NONE)
    data = models.TextField()

## from mantistable ##

class SparqlEndpoint(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    priority = models.PositiveIntegerField(default=0)
    error = models.BooleanField()
    checked_date = models.DateTimeField(default=now)

    @classmethod
    def reset(cls):
        SparqlEndpoint.objects.all().update(error=False)

class GoldStandardsEnum(Enum):
    CTA = 'CTA'
    CEA = 'CEA'
    CPA = 'CPA'


class GlobalStatusEnum(Enum):
    TODO = 'TODO'
    DOING = 'DOING'
    DONE = 'DONE'


class PhasesEnum(Enum):
    #DATA_PREPARATION = {'key': 'dataPreparation', 'name': 'Data Preparation'}
    COLUMN_ANALYSIS = {'key': 'columnsAnalysis', 'name': 'Column Analysis'}
    CONCEPT_ANNOTATION = {'key': 'conceptDatatypeAnnotation', 'name': 'Concept and Datatype Annotation'}
    PREDICATE_ANNOTATION = {'key': 'relationshipsAnnotation', 'name': 'Predicate Annotation'}
    ENTITY_LINKING = {'key': 'entityLinking', 'name': 'Entity Linking'}


class OcularMovement(models.Model):
    user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    results = JSONField(default=[])
    table_name = models.CharField(max_length=200)
