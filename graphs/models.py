from django.db import models
from datetime import datetime
from django.utils import timezone
from django.forms.models import model_to_dict
# Create your models here.


class InternalManagerGraphsManager(models.Manager):
    def get_query_data(self, graph_id):
        return self.filter(id=graph_id).values("query_data").first()

    def save(self, title=None, chart_id=None, query_data=None, is_active=None):
        last_position = self.order_by("-position").first()
        last_position = last_position.position if last_position else 0
        new_position = int(last_position) + 1
        current_time = datetime.now()
        data = InternalManagerGraphs(position=new_position, chart_id=chart_id, query_data=query_data,
                                     is_active=is_active, created_at=current_time, updated_at=current_time, title=title)
        data.save()

    def check_graph_exist(self, graph_id):
        graph_data = self.filter(pk=graph_id).first()
        return model_to_dict(graph_data) if graph_data else None


class GraphType(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(blank=False, null=False, default=timezone.now)
    updated_at = models.DateTimeField(blank=False, null=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "graph_type"
        app_label = "graphs"

    def __str__(self):
        return self.name


class InternalManagerGraphs(models.Model):
    title = models.CharField(max_length=100)
    position = models.IntegerField(blank=True, null=True)
    chart = models.ForeignKey(GraphType, on_delete=models.DO_NOTHING)
    query_data = models.TextField()  # This field type is a guess.
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    objects = InternalManagerGraphsManager()

    class Meta:
        managed = True
        db_table = 'internal_manager_graphs'

    def __str__(self):
        return self.title

