"""
ServiceMetrics will call the serviceMetrics api to return the train
identifiers for trains that have run from defined dates and times.
"""
import base64
import json
from typing import Dict
import requests


# 1. Generate Service Metrics Payload
def return_service_metrics_payload(from_loc, to_loc, from_time, to_time, from_date, to_date, days):
    service_metrics_payload = {
        'from_loc': from_loc,
        'to_loc': to_loc,
        'from_time': from_time,
        'to_time': to_time,
        'from_date': from_date,
        'to_date': to_date,
        'days': days}
    return service_metrics_payload

# 2. Return Service Metrics
def get_service_metrics(service: Dict[str, str]) -> Dict:
    # Load configuration data (email, password)
    with open('../config.json', 'r') as file:
        data = json.load(file)
        auth_value = base64.b64encode(f"{data['email']}:{data['password']}".encode()).decode()

    # Base URL for API Call
    url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"

    # Header definition
    headers = {
        "Authorization": f"Basic {auth_value}",
        "Content-Type": "application/json",
        "Host": "hsp-prod.rockshore.net"
    }

    # Payload definition, from defined data in service param.
    payload = {
        "from_loc": f"{service['from_loc']}",
        "to_loc": f"{service['to_loc']}",
        "from_time": f"{service['from_time']}",
        "to_time": f"{service['to_time']}",
        "from_date": f"{service['from_date']}",
        "to_date": f"{service['to_date']}",
        "days": f"{service['days']}"
    }

    # Sending POST request to API
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

# 3. Return RIDS of Service Metrics
def get_rid_from_metrics(metrics: Dict[str, str]) -> list[str, str]:
    rids = []
    for service in metrics['Services']:
        rids.extend(service['serviceAttributesMetrics']['rids'])
    return rids
