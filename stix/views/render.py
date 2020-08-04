from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import View
from django.http import JsonResponse
from django.core.paginator import Paginator

from dashboard.models import SnortDetails
from stix.views.base import StixBase
from users.models import Users
from stix.forms.stix_type import StixTypeForm, StixType
import json


class ListStixDetails(ListView):
    template_name = "stix/visualization.html"
    queryset = SnortDetails.objects.all().order_by("timestamp")
    paginate_by = 10
    stix_type = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super(ListStixDetails, self).get_context_data()
        stix_type_form = StixTypeForm(initial={"stix_type": StixType.objects.filter(pk=self.stix_type).first()})
        context_data["stix_form"] = stix_type_form
        context_data["stix_type"] = self.stix_type
        return context_data

    def get_queryset(self):
        query_params = self.request.GET
        stix_type = query_params.get("stix_type")
        try:
            self.stix_type = int(stix_type)
        except:
            self.stix_type = None
        if self.stix_type == 2:
            query_set = SnortDetails.objects.filter(sig__attack_pattern_type_id__isnull=False).order_by("timestamp")
        else:
            query_set = SnortDetails.objects.none()
        paginator = Paginator(query_set, self.paginate_by)
        return paginator.object_list


class StixVisualize(View, StixBase):

    def get(self, request, stix_type, key):
        StixBase.__init__(self, key)
        if stix_type == 2:
            data = self.attack_pattern()
            return render(request, "stix/visualize.html", {"stix_data": data}) if json.loads(data) else JsonResponse({"success": False, "msg": "Not Found"}, status=404)
        else:
            return JsonResponse({"success": False, "msg": "Currently we are not supporting Stix Type"}, status=400)
