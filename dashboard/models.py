from django.db import models
from rules.models import Rules

# Create your models here.


class SnortDetailsManager(models.Manager):
    def get_attack_details(self, key):
        return self.filter(pk=key).first()


class SnortDetails(models.Model):
    sig = models.ForeignKey(Rules, on_delete=models.DO_NOTHING, default=None)
    sig_rev = models.CharField(max_length=30, blank=True, null=True)
    msg = models.CharField(max_length=300, blank=True, null=True)
    proto = models.CharField(max_length=30, blank=True, null=True)
    src = models.CharField(max_length=117, blank=True, null=True)
    srcport = models.CharField(max_length=30, blank=True, null=True)
    src_city = models.CharField(max_length=135, blank=True, null=True)
    src_country = models.CharField(max_length=135, blank=True, null=True)
    dst = models.CharField(max_length=117, blank=True, null=True)
    dstport = models.CharField(max_length=30, blank=True, null=True)
    dst_city = models.CharField(max_length=135, blank=True, null=True)
    dst_country = models.CharField(max_length=135, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    src_longitude = models.CharField(max_length=45, blank=True, null=True)
    src_latitude = models.CharField(max_length=45, blank=True, null=True)
    dst_longitude = models.CharField(max_length=45, blank=True, null=True)
    dst_latitude = models.CharField(max_length=45, blank=True, null=True)
    objects = SnortDetailsManager()

    class Meta:
        managed = True
        db_table = 'snort_details'
