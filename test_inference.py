import requests

url = "http://127.0.0.1:8000/upload/"
payload = {"filename": "MMT.pdf"}

response = requests.post(url, json=payload)

# Print the raw response text for debugging
print("Response text:", response)

# Attempt to parse the response as JSON
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Failed to parse response as JSON")
