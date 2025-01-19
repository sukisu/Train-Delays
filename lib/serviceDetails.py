"""
ServiceDetails will return the timings and cancellation times for each RID.
"""
import base64
import json
from typing import Dict

import requests

# 1. Returning service details per RID.
def get_service_details(rid: list[str, str]) -> Dict:

    with open('../config.json', 'r') as file:
        data = json.load(file)
        auth_value = base64.b64encode(f"{data['email']}:{data['password']}".encode()).decode()

    # Base URL for API Call
    url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"

    headers = {
        "Authorization": f"Basic {auth_value}",
        "Content-Type": "application/json",
        "Host": "hsp-prod.rockshore.net"
    }

    for identifier in rid:
        payload = {
            "rid": identifier,
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code, response.text

print(get_service_details(['201607294212242']))
