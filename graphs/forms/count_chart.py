from django import forms
from graphs.models import GraphType


class BaseForm(forms.Form):
    graph_type = forms.ModelChoiceField(widget=forms.Select(attrs={"name": "graph_type"}), queryset=GraphType.objects.all())
    title = forms.CharField(max_length=100, widget=forms.TextInput())


class CustomChoice(forms.MultipleChoiceField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_choice = ()
        self.choices = ()
        self.initial = ()

    def clean(self, value):
        choices = []
        if type(value) == str:
            choices.append((value, value))
        elif type(value) == list:
            for i, val in enumerate(value):
                choices.append((val, val))
        self.choices = tuple(choices)
        return value


class CountForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), required=True, label="Query")
    others = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": ""}), required=False)
    required_columns = CustomChoice(widget=forms.SelectMultiple(attrs={"multiple": True
        , "class": "multi-tag form-control"}), required=False)
    count = forms.BooleanField(widget=forms.CheckboxInput(attrs={}), required=False)
    group_by_field = CustomChoice(widget=forms.SelectMultiple(attrs={"multiple": True
        , "class": "multi-tag form-control"}),
                                  label="Group By", required=True)
    count_column = CustomChoice(widget=forms.Select(attrs={"multiple": False
        , "class": "multi-tag form-control"}),
                                label="Count Column", required=False)
    rename_columns = CustomChoice(widget=forms.SelectMultiple(attrs={"multiple": True
        , "class": "multi-tag form-control", "placeholder": "Enter Data Key, Value"}),
                                  label="Rename Fields", required=False)
    field_name = CustomChoice(widget=forms.Select(attrs={"multiple": False
        , "class": "multi-tag form-control"}), required=False)


