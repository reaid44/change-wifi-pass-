from dotenv import load_dotenv
import os
import random
import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

# Environment variables
admin_user = os.getenv('ROUTER_USER')
admin_pass = os.getenv('ROUTER_PASS')
router_ip = os.getenv('ROUTER_IP', '192.168.0.1')  # Tenda F3 default
slack_token = os.getenv('SLACK_TOKEN')
slack_channel = os.getenv('SLACK_CHANNEL')

# Generate new password
words = open("wordlist.txt", "r").read().splitlines()
new_password = random.choice(words).capitalize() + random.choice(words).capitalize()
if len(new_password) < 8:
    new_password += "X"  # Ensure minimum 8 chars

# Start a session
s = requests.Session()

# Tenda login
login_url = f"http://{router_ip}/"
login_data = {
    "login_user": admin_user,   # Tenda login field
    "login_pass": admin_pass
}
r = s.post(login_url, data=login_data)
if r.status_code != 200:
    print("Login failed. Check credentials or router IP.")
    exit()

# Tenda password change URL
change_url = f"http://{router_ip}/userRpm/WlanSecurityRpm.htm"
payload = {
    "wl_wpa_psk": new_password,   # Tenda WiFi password field
    "action": "apply"
}

r = s.post(change_url, data=payload)
if r.status_code == 200:
    print(f"WiFi password updated successfully: {new_password}")
else:
    print("Failed to update WiFi password.")

# Send new password to Slack
slack_data = {
    'token': slack_token,
    'channel': slack_channel,
    'text': f"New Wi-Fi Password: {new_password}",
}
requests.post("https://slack.com/api/chat.postMessage", params=slack_data)
