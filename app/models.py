from django.db import models


class Urls(models.Model):
    url = models.TextField()
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Url: {self.description} | #{self.id}'


class UrlResults(models.Model):
    record_id = models.CharField(max_length=255, null=True)
    url = models.ForeignKey(Urls, models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    date = models.TextField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    zip = models.TextField(null=True, blank=True)
    applicant = models.TextField(null=True, blank=True)
    owner = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    job_value = models.TextField(null=True, blank=True)
    kw = models.TextField(null=True, blank=True)
    panel_upgrade = models.TextField(null=True, blank=True)
    existing_solar_system = models.TextField(null=True, blank=True)
    utility_information = models.TextField(null=True, blank=True)
    total_cost = models.TextField(null=True, blank=True)




