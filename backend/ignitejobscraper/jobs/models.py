from django.db import models

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    posted_date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True, blank=True)
    location_type = models.JSONField(null=True, blank=True)
    salary = models.CharField(max_length=255, null=True, blank=True)
    employment_type = models.JSONField()
    skills = models.JSONField(null=True, blank=True)
    job_details = models.TextField(null=True, blank=True)
    job_id = models.IntegerField(default=1)

    def __str__(self):
        return self.title