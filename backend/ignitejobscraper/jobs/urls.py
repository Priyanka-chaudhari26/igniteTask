from django.urls import path
from .views import JobListView, create_job

urlpatterns = [
    path('api/jobs/', create_job.as_view(), name='create_job'),
    path('api/jobs/list/', JobListView.as_view(), name='job-list'),

]
