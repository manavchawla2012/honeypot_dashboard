from django import forms
from stix.models import StixType


class StixTypeForm(forms.Form):
    stix_type = forms.ModelChoiceField(queryset=StixType.objects.all(), required=True, label="Select Stix Type")