import requests

# Step 1: Upload the PDF file
upload_url = "http://127.0.0.1:1111/api/upload/"
files = {'file': open('stock.pdf', 'rb')}
upload_response = requests.post(upload_url, files=files)

# Print the raw response text for debugging
print("Upload response text:", upload_response.text)

# Attempt to parse the response as JSON
try:
    upload_response_json = upload_response.json()
    print("Upload response JSON:", upload_response_json)
except requests.exceptions.JSONDecodeError:
    print("Failed to parse upload response as JSON")
    exit()

# Step 2: Generate flashcards using the uploaded file
generate_flashcards_url = "http://127.0.0.1:1111/api/generate_flashcards/"
payload = {"filename": "stock.pdf"}

print(f"Sending request to generate flashcards for file: {payload['filename']}")
generate_response = requests.post(generate_flashcards_url, json=payload)

# Print the raw response text for debugging
print("Generate flashcards response text:", generate_response.text)

# Attempt to parse the response as JSON
try:
    generate_response_json = generate_response.json()
    print("Generate flashcards response JSON:", generate_response_json)
except requests.exceptions.JSONDecodeError:
    print("Failed to parse generate flashcards response as JSON")
