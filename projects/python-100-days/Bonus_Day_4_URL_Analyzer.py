# use virus total api key to analyze URLs
# requires the user to have a valid VirusTotal API key
# API key is stored in a seperate file names "vt_api_key.txt"
# checks if api key file exists, if not create one and prompt the user to enter their API key. adds api key to the file.
# continues accepting urls until the user decides to stop
# display the final numerical risk score
# display low, medium, and high risk levels
# handle uppercase and lowercase URLs
# does not crash if the user enters something strange or incopmplete

import os
import base64
import requests

# colors
COLOR_RESET = "\033[0m"
COLOR_LOW = "\033[92m"      # Green
COLOR_MEDIUM = "\033[93m"   # Yellow
COLOR_HIGH = "\033[91m"     # Red

API_KEY_FILE = "api_keys/vt_api_key.txt"
TARGET_URL = ""

# function to check if vt_api_key.txt exists in the api_keys dir, and contains a valid API key
def check_api_key():
    if not os.path.exists("api_keys"):
        os.makedirs("api_keys")
    if not os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "w") as f:
            f.write(input("Enter your VirusTotal API key: ").strip())
    with open(API_KEY_FILE) as f:
        key = f.read().strip()
    if not key:
        raise ValueError("API key is missing in api_keys/vt_api_key.txt")
    return key

# function to determine risk score based on VirusTotal analysis stats
def determine_risk(stats):
    if stats['malicious'] > 0:
        return "High"
    elif stats['suspicious'] > 0:
        return "Medium"
    else:
        return "Low"

def determine_numerical_score(stats): # updated so that 1 malicious result doesn't automatically mean the highest score
    score = 0
    score += stats['malicious'] * 3
    score += stats['suspicious'] * 2
    score += stats['undetected'] * 1
    return score

while True:
    TARGET_URL = input("Enter a URL to analyze (or 'quit' ): ").strip()
    if TARGET_URL.lower() == "quit":
        break
    url_id = base64.urlsafe_b64encode(TARGET_URL.encode()).decode().strip("=")
    endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {
        "accept": "application/json",
        "x-apikey": check_api_key()
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        result = response.json()
        stats = result['data']['attributes']['last_analysis_stats']
        print(f"Results for URL: {TARGET_URL}")
        print(f" - Malicious: {stats['malicious']}")
        print(f" - Suspicious: {stats['suspicious']}")
        print(f" - Undetected: {stats['undetected']}")
        print(f" - Harmless: {stats['harmless']}")
        risk_level = determine_risk(stats)
        if risk_level == "High":
            color = COLOR_HIGH
        elif risk_level == "Medium":
            color = COLOR_MEDIUM
        else:
            color = COLOR_LOW
        print(f" - Risk Level: {color}{risk_level}{COLOR_RESET}")
        numerical_score = determine_numerical_score(stats)
        print(f" - Numerical Score: {numerical_score}")
    elif response.status_code == 404:
        print(f"URL not found: {TARGET_URL}")
    else:
        print(f"Error: {response.status_code}")
