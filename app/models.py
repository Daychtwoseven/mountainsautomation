from django.db import models


class Urls(models.Model):
    url = models.TextField()
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Url: {self.description} | #{self.id}'


class UrlResults(models.Model):
    record_id = models.CharField(max_length=255, null=True)
    url = models.ForeignKey(Urls, models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    date = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=255, null=True, blank=True)
    applicant = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    job_value = models.CharField(max_length=255, null=True, blank=True)
    kw = models.CharField(max_length=255, null=True, blank=True)
    panel_upgrade = models.CharField(max_length=255, null=True, blank=True)
    existing_solar_system = models.CharField(max_length=255, null=True, blank=True)
    utility_information = models.CharField(max_length=255, null=True, blank=True)
    total_cost = models.CharField(max_length=255, null=True, blank=True)




