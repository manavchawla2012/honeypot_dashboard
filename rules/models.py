from django.db import models
from stix.models import MalwareLabel, CourseOfAction, AttackPatternType
from django.utils import timezone

# Create your models here.


class RuleSource(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "rule_src"


class Tools(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "tools"


class Rules(models.Model):
    sid = models.IntegerField(null=False, blank=False)
    rev = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    file_name = models.CharField(max_length=50, null=True, blank=True)
    rule_src = models.ForeignKey(RuleSource, on_delete=models.DO_NOTHING)
    tool = models.ForeignKey(Tools, on_delete=models.DO_NOTHING)
    malware_label = models.ForeignKey(MalwareLabel, on_delete=models.CASCADE, default=None)
    attack_pattern_type = models.ForeignKey(AttackPatternType, on_delete=models.CASCADE, default=None)
    course_of_action = models.ForeignKey(CourseOfAction, on_delete=models.DO_NOTHING, default=None)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "rules"
        unique_together = (("sid", "rev"),)
