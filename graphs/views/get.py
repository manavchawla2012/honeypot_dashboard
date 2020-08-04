from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import ListView

from graphs.models import InternalManagerGraphs
from graphs.forms.count_chart import CountForm
from django.forms import formset_factory
from django.shortcuts import render
from graphs.views.base import create_graph
import json
from dateutil import parser
from datetime import datetime, timedelta
from decorators.check_module_permissions import check_user_permission, class_view_decorator


@require_http_methods(["POST"])
@login_required
def get_graphs_list(request):
    if request.method == "POST":
        graph_details = InternalManagerGraphs.objects.filter(is_active=1).values("id", "position", "chart_id", "title") \
            .order_by("position")
        if not graph_details:
            success = False
            message = "No Graphs Found"
        else:
            success = True
            message = "Success"
        return JsonResponse({"success": success, "message": message, "graphs_details": list(graph_details)})


@class_view_decorator(check_user_permission("view_internalmanagergraphs"))
class Graphs(ListView):
    queryset = InternalManagerGraphs.objects.all().order_by("pk")
    template_name = "graphs/graphs.html"
    model = InternalManagerGraphs
    paginate_by = 10


@require_http_methods(["GET"])
@login_required
@check_user_permission("view_internalmanagergraphs")
def get_form(request):
    if request.method == "GET":
        get_data = request.GET
        graph_type = int(get_data["graph"]) if "graph" in get_data else None
        if graph_type in [1, 2, 3]:
            form = CountForm()
            return render(request, "graphs/forms/forms.html", {"form": form})
        elif graph_type == 4:
            form = formset_factory(CountForm, extra=2)
            return render(request, "graphs/forms/forms.html",
                          {"form": form({'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MAX_NUM_FORMS': '',
                                         }), "formset": True})
        else:
            return HttpResponseNotFound("Form Id not Found")


def get_graph_details(graph_id):
    graph_data = InternalManagerGraphs.objects.check_graph_exist(graph_id)
    if graph_data:
        data = graph_data
        query_data = json.loads(data["query_data"])
        data = query_data
    else:
        data = ""
    response = data
    return response


def load_graphs(request):
    if request.method == "POST":
        try:
            data = request.POST
            query_id = data["query_id"]
            to_date = str(data["to_date"])
            from_date = str(data["from_date"])
            if to_date and from_date:
                to_date = parser.parse(to_date).date()
                from_date = parser.parse(from_date).date()
            else:
                to_date = datetime.now()
                from_date = to_date - timedelta(hours=1)
            success = True
            query_data_object = InternalManagerGraphs.objects.get_query_data(query_id)
            if query_data_object:
                query_data = json.loads(query_data_object["query_data"])
                data = create_graph(query_data, to_date, from_date)
            else:
                success = False
                data = {}
            return JsonResponse({"success": success, "data": data})
        except Exception as e:
            return JsonResponse({"success": False, "data": {}})
