from django.shortcuts import render

from decorators.check_module_permissions import check_user_permission
from graphs.views.base import verify_chart_data, get_chart_data
from django.http import JsonResponse
import json
from graphs.forms.count_chart import BaseForm
from graphs.models import InternalManagerGraphs


@check_user_permission("add_internalmanagergraphs")
def create_chart(request):
    if request.method == "GET":
        base_form = BaseForm()
        return render(request, "graphs/new.html", {"baseForm": base_form})
    if request.method == "POST":
        data = request.POST
        save = data["save"]
        data = json.loads(data["data"])
        success, msg = verify_chart_data(data)
        if success:
            json_data = msg
            success, chart_data = get_chart_data(msg)
            msg = chart_data
            is_save = True if save == "true" else False
            if success:
                if is_save:
                    title = json_data["title"]
                    graph_type = json_data["graph_type"]
                    InternalManagerGraphs.objects.save(title=title, chart_id=graph_type, query_data=json.dumps(json_data), is_active=True)

        return JsonResponse({"success": success, "msg": msg})





