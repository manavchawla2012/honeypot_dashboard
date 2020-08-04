from django.db import models
from django.utils import timezone

# Create your models here.


class AttackPatternType(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    description = models.CharField(max_length=5000, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "attack_pattern_type"
        app_label = "stix"


class CourseOfAction(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    description = models.CharField(max_length=300, null=False, blank=False)
    generic_id = models.CharField(max_length=20, null=True, blank=True)
    action = models.CharField(max_length=300, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "course_of_action"
        app_label = "stix"


class IdentityType(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    description = models.CharField(max_length=5000, null=False, blank=False)
    label = models.CharField(max_length=45, null=True, blank=True)
    identity_class = models.CharField(max_length=45, null=False, blank=False)
    sectors = models.CharField(max_length=45, null=True, blank=True)
    contact_information = models.CharField(max_length=45, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "identity_type"
        app_label = "stix"


class MalwareLabel(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    description = models.CharField(max_length=5000, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "malware_label"
        app_label = "stix"


class StixType(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    identifier = models.CharField(max_length=45, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "stix_type"
        app_label = "stix"

    def __str__(self):
        return self.name


class StixFiles(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    stix_type = models.ForeignKey(StixType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    updated_at = models.DateTimeField(null=False, blank=False, default=timezone.now)

    class Meta:
        managed = True
        db_table = "stix_files"
        app_label = "stix"
