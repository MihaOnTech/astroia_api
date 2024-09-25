import swisseph as swe
import requests
import json

# URL to which the request will be sent
url = 'http://127.0.0.1:5000/natal_chart'

# Data to be sent in JSON format
data = {
    "date": "22/01/91",
    "time": "23:30",
    "location": "Sabadell, España"
}
# Convert data dictionary to JSON
json_data = json.dumps(data)

# Headers you might want to send along with the request
headers = {
    'Content-Type': 'application/json',  # This header informs the server about the type of the content
    'Custom-Header': 'value'             # Example of a custom header
}

# Making the POST request
response = requests.post(url, data=json_data, headers=headers)

# Printing the response from the server
print(response.text)

# Write the response text into a response.json file
with open('response.json', 'w', encoding='utf-8') as f:
    # If you want the file to be formatted as valid JSON, try to load it into a dictionary first
    try:
        json_response = json.loads(response.text)
        json.dump(json_response, f, ensure_ascii=False, indent=4)  # Writing in pretty-printed JSON format
    except json.JSONDecodeError:
        # If the response is not valid JSON, just write it as plain text
        f.write(response.text)

# Additional data examples
data_miguel = {
    'date': '05/02/93',
    'time': '03:30',
    'location': 'Barcelona, España'
}
data_olga = {
    'date': '22/01/91',
    'time': '23:30',
    'location': 'Sabadell, España'
}
