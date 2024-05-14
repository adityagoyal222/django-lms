import requests


# get current  date unix timestamp
import time
import datetime
import calendar
now = datetime.datetime.now()
unixtime = calendar.timegm(now.utctimetuple())

data = {
    'name': 'John Doe',
    'issuer': 'Your Issuer',
    'issue_date': '13456789900',  # Replace with the actual date
}

def send_certificate_request(name, issuer, unixtime):
    data = {
        'name': name,
        'issuer': issuer,
        'issue_date': unixtime,  # Replace with the actual date
    }
    # Define the URL of the FastAPI endpoint
    api_endpoint_url = 'http://0.0.0.0:8080/issue-certificate'  # Replace with the actual URL

    # Make a POST request to the endpoint with the provided data
    response = requests.post(api_endpoint_url, json=data)

    if response.status_code == 200:
        # The response content is available in response.json()
        certificate_response = response.json()
        return certificate_response
    else:
        # Handle the error and return an error response
        return {"error": f"API request failed with status code {response.status_code}"}

def verify_certificate(certificate_id):
    # Define the URL of the FastAPI endpoint
    api_endpoint_url = 'http://0.0.0.0:8080/verify-certificate'

    response = requests.post(api_endpoint_url, json={'certificate_id': certificate_id})

    if response.status_code == 200:
        # The response content is available in response.json()
        certificate_response = response.json()
        return certificate_response
    else:
        # Handle the error and return an error response
        return {"error": f"API request failed with status code {response.status_code}"}
