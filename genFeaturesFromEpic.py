import requests
import json
import os

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_key = os.getenv("OpenAI_Key")

headers = {
    'Authorization': f'Bearer {OPENAI_key}',
    'Content-Type': 'application/json'
}


def generate_features(epic_description):
  url = OPENAI_URL

  payload = json.dumps({
    "model": "gpt-4",
    "messages": [
      {
        "role": "system",
        "content": "You are an industry leader expert product owner who can write features diligently based on the Epic description.You never make up any information that isn't there. "
      },
      {
        "role": "user",
        "content": f" Epic description : '{epic_description}'. "
      },
      {
        "role": "system",
        "content": """Generate top five Features which will satisfy the given Epic description strictly in a Syntactical correct JSONArray format.
        Review all generated features thoroughly and provide detailed hypothesis, acceptance criteria, leading indicators, non-functional requirements (NFRs),
        and objectives and key results (OKRs). Estimate 'Business Value', 'Time Criticality', and 'RR/OE' for each of the features in Fibonacci numbers,
        with at least one feature having a value '1' as Business Value. Provide detailed explaination reasoning for each of the estimations
        so that everyone can understand and agree. Generate output strictly in a Syntactical correct JSONArray format.
        ## Sample JSONArray Ouput  as follows :
        {  "ArraySize": 2, 'Features': [{'feature': { 'Title': 'Sample Title', 'Hypothesis': 'Sample ', 'Acceptance Criteria': '[Given] Sample [When] sample [Then] sample', 'Leading Indicators': 'Sample ', 'Non-functional Requirements': 'Sample', 'Business Value': { 'value': 8, 'rationale': 'Sample' }, 'Time Criticality': { 'value': 8, 'rationale': 'Sample.' }, 'RR/OE': { 'value': 3, 'rationale': 'Sample.' } } }, // Include similar structures for the remaining features...] }' """
      }
    ],
    "temperature": 0,
    "max_tokens": 2000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
  })
    print(f"IN Calling OpenAI ${headers}")

  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)
  # Parse the response text to a Python dictionary
  response_data = json.loads(response.text)
  # Access choices[0] from the response data
  choices_0 = response_data['choices'][0]
  print(choices_0)

# card_data ="Create a Mentor-Mentee Initiative"
# generate_features(card_data)
