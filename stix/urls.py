from django.urls import path
from stix.views.render import *


urlpatterns = [
    path('visualization', ListStixDetails.as_view(), name="visualization"),
    path('visualize/<int:stix_type>/<int:key>', StixVisualize.as_view(), name="visualize")
]