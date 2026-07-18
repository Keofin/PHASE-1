import urllib.request
import json

# Your live production Cloudflare Worker URL
url = "https://keofin-advisor-api.keofinadvisors.workers.dev"

# The exact same customer scenario payload
data = {
    "income": 80000,
    "existing_emis": 15000,
    "proposed_loan": 500000,
    "rate": 10.5,
    "tenure_months": 36,
    "customer_query": "Can I easily afford this new loan EMI?"
}

# Encode the request payload safely
encoded_data = json.dumps(data).encode('utf-8')

# ─── ADD A REAL USER-AGENT HEADER HERE ───
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(
    url, 
    data=encoded_data, 
    headers=headers,
    method='POST'
)

print("Sending test request to Cloudflare Edge AI network...\n")

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("🚀 API RESPONSE RECEIVED SUCCESSFULLY:\n")
        print(json.dumps(result, indent=4, ensure_ascii=False))
except Exception as e:
    print(f"❌ Request failed: {e}")