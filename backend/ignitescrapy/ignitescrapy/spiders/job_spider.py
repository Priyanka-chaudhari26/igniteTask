
import scrapy
import requests
from datetime import datetime, timedelta

class JobScraperSpider(scrapy.Spider):
    name = "job_scraper"
    start_urls = [
        "https://www.dice.com/jobs?q=Software&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&filters.postedDate=ONE&filters.workplaceTypes=Remote&filters.employmentType=CONTRACTS&currencyCode=USD&language=en"
    ]

    def start_requests(self):
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        yield scrapy.Request(self.start_urls[0], headers=headers, callback=self.parse)

        
        self.fetch_jobs_from_api()

    def fetch_jobs_from_api(self):
        
        headers = {
            'x-api-key': '1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8',
        }
        params = {
            'q': 'Software',
            'countryCode2': 'US',
            'radius': '30',
            'radiusUnit': 'mi',
            'page': '1',
            'pageSize': '20',
            'facets': 'employmentType|postedDate|workFromHomeAvailability|workplaceTypes|employerType|easyApply|isRemote|willingToSponsor',
            'filters.workplaceTypes': 'Remote',
            'filters.employmentType': 'CONTRACTS',
            'filters.postedDate': 'ONE',
            'currencyCode': 'USD',
            'fields': 'id|jobId|title|companyName|jobLocation.displayName|postedDate|modifiedDate|employmentType|detailsPageUrl|salary|employerType|workFromHomeAvailability|workplaceTypes|isRemote',
        }

        try:
            response = requests.get(
                "https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            jobs = response.json().get('data', [])
            for job in jobs:
                job_data = {
                    'job_id': job.get('jobId'),
                    'job_title': job.get('title'),
                    'company_name': job.get('companyName'),
                    'location': job.get('jobLocation', {}).get('displayName'),
                    'posted_date': job.get('postedDate'),
                    'salary': job.get('salary'),
                    'employment_type': job.get('employmentType'),
                    'details_url': job.get('detailsPageUrl'),
                    'modified_date': job.get('modifiedDate'),
                    'location_type': job.get('workplaceTypes', []),
                    'job_details': job.get('jobMetadata'),
                }
               
                print(f"Job data: {job_data}")  
                self.send_job_to_api(job_data)

        except requests.exceptions.RequestException as e:
            self.log(f"API request failed: {e}")

    def send_job_to_api(self, job_data):
        api_url = 'http://127.0.0.1:8000/api/jobs/' 
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(api_url, headers=headers, json=job_data)
            if response.status_code == 201:
                self.log(f"Successfully saved job {job_data['job_title']}")
            else:
                self.log(f"Failed to save job {job_data['job_title']} - {response.json()}")
        except requests.exceptions.RequestException as e:
            self.log(f"Failed to send job to API: {e}")

    def parse(self, response):
        
        self.log(f"Received response from {response.url} with status {response.status}")
        
        job_ids = response.css('h5 > a[data-cy="card-title-link"]::attr(id)').getall()
        base_url = "https://www.dice.com/job-detail/"

        for job_id in job_ids:
            job_url = f"{base_url}/{job_id}"
            yield response.follow(job_url, callback=self.parse_job_details)

    
