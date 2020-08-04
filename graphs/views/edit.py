from django.shortcuts import render
from django.views.generic import DeleteView

from graphs.models import InternalManagerGraphs
from graphs.views.get import get_graph_details
from graphs.forms.count_chart import CountForm, BaseForm
from django.forms import formset_factory
from django.http import HttpResponseNotFound, JsonResponse
import json
from graphs.views.base import verify_chart_data, get_chart_data
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from decorators.check_module_permissions import check_user_permission, class_view_decorator


@check_user_permission("change_internalmanagergraphs")
def edit_graph(request, graph_id):
    if request.method == "GET":
        response = get_graph_details(graph_id)
        if response:
            graph_type = int(response["graph_type"])
            graph_title = response["title"]
            graph_data = response["graph_data"]
            form_data = FormData(graph_type, graph_data)
            base_form = BaseForm({"graph_type": graph_type, "title": graph_title})
            success, msg, form, is_formset = form_data.convert_form_data()
            if success:
                return render(request, "graphs/edit.html", {"baseForm": base_form, "form": form,
                                                            "formset": is_formset, "id": graph_id})

        return HttpResponseNotFound('<h3>Graph Details not found</h3>')
    elif request.method == "POST":
        data = request.POST
        update = data["save"]
        data = json.loads(data["data"])
        success, msg = verify_chart_data(data)
        if success:
            json_data = msg
            success, chart_data = get_chart_data(msg)
            msg = chart_data
            is_update = True if update == "true" else False
            if success:
                if is_update:
                    title = json_data["title"]
                    graph_type = json_data["graph_type"]
                    current_time = datetime.now()
                    InternalManagerGraphs.objects.filter(pk=graph_id).update(title=title, chart_id=graph_type,
                                                                             query_data=json.dumps(json_data),
                                                                             is_active=True, updated_at=current_time)
        return JsonResponse({"success": success, "msg": msg})


@csrf_exempt
@check_user_permission("change_internalmanagergraphs")
def inactive_graph(request, graph_id):
    if request.method == "POST":
        status = True if request.POST.get("status") == "true" else False
        if graph_id:
            current_time = datetime.now()
            try:
                InternalManagerGraphs.objects.filter(pk=graph_id).update(is_active=status, updated_at=current_time)
                success = True
                msg = f"Graph {graph_id} successfully " + ("Activated" if status else "Deactivated")
            except Exception as e:
                success = False
                msg = "Some Issues in Updating Please refresh the Page"
        else:
            success = False
            msg = "Some error Occurred, Please Refresh the Page"

        return JsonResponse({"success": success, "msg": msg})


class FormData:
    def __init__(self, graph_type: int, data: list):
        self.type = graph_type
        self.data = data

    def convert_form_data(self):
        data_elements = len(self.data)
        if self.type in [1, 2, 3]:
            is_formset = False
            if data_elements != 1 and type(data_elements) == list:
                success = False
                msg = "Data Elements > 1"
                final_data = {}
            else:
                success = True
                data = self.data[0] if type(self.data) == list else self.data
                msg = "Data Processed"
                if data:
                    final_data = data
                else:
                    success = False
                    msg = "No Data Found"
                    final_data = {}
            form = CountForm(final_data)
        elif self.type == 4:
            is_formset = True
            if data_elements <= 1:
                success = False
                msg = "Data Elements <= 1"
                final_data = {}
                count = 0
            else:
                success = True
                msg = "Data Processes"
                final_data = {}
                count = 0
                for i, data in enumerate(self.data):
                    if data and type(data) == dict:
                        for key, value in data.items():
                            final_data[f"form-{i}-{key}"] = value
                    count = i
                count += 1
                final_data["form-TOTAL_FORMS"] = count
                final_data["form-INITIAL_FORMS"] = count
                final_data["form-MAX_NUM_FORMS"] = ""
            form_formset = formset_factory(CountForm, extra=count)
            form = form_formset(final_data)

        else:
            is_formset = False
            success = False
            msg = "Graph Type not Supported"
            form = None

        return success, msg, form, is_formset


@class_view_decorator(check_user_permission("delete_internalmanagergraphs"))
class Delete(DeleteView):
    template_name = "graphs/delete.html"
    success_url = reverse_lazy("graphs:list")
    model = InternalManagerGraphs
    pk_url_kwarg = "graph_id"
