from django import forms
from django.utils.safestring import mark_safe

from .models import GoldStandardsEnum


class TableFromJSONForm(forms.Form):
    table_name = forms.CharField(
        widget=forms.TextInput(),
        label="Table name",
        max_length=200,
        required=True,
        label_suffix=""
    )
    json_file = forms.FileField(
        widget=forms.FileInput(attrs={'accept': '.json'}),
        label="Insert a JSON file",
        required=True,
        label_suffix=""
    )


class AnnotationFromJSONForm(forms.Form):
    json_file = forms.FileField(
        widget=forms.FileInput(attrs={'accept': '.csv'}),
        label="Insert a CSV file",
        required=True,
        label_suffix=""
    )
    gs_type = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control selectpicker'}),
        label="Task Type",
        choices=[(tag.name, tag.value) for tag in GoldStandardsEnum],
        required=True,
        label_suffix=""
    )


class FamiliarityInterestForm(forms.Form):
    highlightIndexes = forms.CharField(widget=forms.HiddenInput())

    # 1 high
    # 0 low
    familiarityChoices = forms.ChoiceField(
        widget=forms.RadioSelect,
        required=True,
        choices=[
            (0, mark_safe("<span class='text'><span class='title'>Low Familiarity</span>"
                          # "<p class='description'>A <b>low</b> degree of familiarity implies that all "
                          # "keywords will be explained. <br/>"
                          # "The output will be understood with no effort by any kind of audience.</p>
                          "</span>"
                          )),
            (1, mark_safe("<span class='text'><span class='title'>High Familiarity</span>"
                          # "<p class='description'>An <b>high</b> degree of familiarity implies that no"
                          # "concept will be explained.<br/>"
                          # "The output will contain highly specific analysis and comparisons.</p>
                          "</span>"
                          )),
        ]
    )

    interestChoices = forms.ChoiceField(
        widget=forms.RadioSelect,
        required=True,
        choices=[
            (0, mark_safe("<span class='text'><span class='title'>Low Interest</span>"
                          # "<p class='description'></p>
                          "</span>"
                          )),
            (1, mark_safe("<span class='text'><span class='title'>High Interest</span>"
                          # "<p class='description'></p>
                          "</span>"
                          )),
        ]
    )
