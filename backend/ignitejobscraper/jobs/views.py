from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializers import JobSerializer
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json


class JobListView(APIView):
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    
class create_job(APIView):
    @csrf_exempt  
    def post(request):
        if request.method == 'POST':
            try:
                
                data = json.loads(request.body)
                
                
                job_id = data.get('job_id')
                job_title = data.get('job_title')
                company_name = data.get('company_name')
                location = data.get('location')
                employment_type = data.get('employment_type')
                skills = data.get('skills')
                job_details = data.get('job_details')
                posted_date = parse_datetime(data.get('posted_date'))
                modified_date = parse_datetime(data.get('modified_date'))

               
                job = Job(
                    job_id=job_id,
                    job_title=job_title,
                    company_name=company_name,
                    location=location,
                    employment_type=employment_type,
                    skills=skills,
                    job_details=job_details,
                    posted_date=posted_date,
                    modified_date=modified_date
                )
                job.save()

                
                return JsonResponse({'message': 'Job created successfully!'}, status=201)

            except Exception as e:
                return JsonResponse({'message': str(e)}, status=400)
        else:
            return JsonResponse({'message': 'Invalid method. Use POST.'}, status=405)