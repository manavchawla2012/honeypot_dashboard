from django.urls import path
from graphs.views.get import get_graphs_list, get_form, load_graphs, Graphs
from graphs.views.new import create_chart
from graphs.views.edit import edit_graph, inactive_graph, Delete


urlpatterns = [
    path("list", get_graphs_list, name="get_graph_list"),
    path("new", create_chart, name="new"),
    path("get/form", get_form, name="get_form"),
    path("delete/<int:graph_id>", Delete.as_view(), name="delete"),
    path("edit/<int:graph_id>", edit_graph, name="edit"),
    path("inactive/<int:graph_id>", inactive_graph, name="inactive"),
    path("load_graphs", load_graphs, name="load"),
    path("", Graphs.as_view(), name="list")
]
