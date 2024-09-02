import requests

# API endpoint for the chatbot
endpoint = 'http://127.0.0.1:8000/chat'

# Data to be sent in the POST request, including the message content and the conversation ID(to track previous messages)
data = {
    'content': 'What is MONEYME\'s strategy and focus areas?',
    'conversation_id': 'conv1234'
}

# Send a POST request to the chat endpoint with the provided data
response = requests.post(endpoint, json=data)

print(response.json()['response'])