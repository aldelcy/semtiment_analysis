import requests
import re
from datetime import datetime

url = "https://octopi.zendesk.com/api/v2/tickets.json?sort_by=created_at&sort_order=desc"
email = "sebastien@cetuslabs.com"
with open('zendesk.token', 'r') as t:
  token = t.read()

def preprocess(message):
  # Lowercase the message
  text = message.lower()
  # Replace email addresses with a space in the message
  text = re.sub(r'(?:\.?)([\w\-_+#~!$&\'\.]+(?<!\.)(@|[ ]?\(?[ ]?(at|AT)[ ]?\)?[ ]?)(?<!\.)[\w]+[\w\-\.]*\.[a-zA-Z-]{2,3})(?:[^\w])', ' ', text)
  # Replace URLs with a space in the message
  text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
  # Replace usernames with a space. The usernames are any word that starts with @.
  text = re.sub(r'[@][A-Za-z][\S]*', ' ', text)
  # Replace #tags with a space.
  text = re.sub(r'[#][A-Za-z][\S]*', ' ', text)
  # Replace everything not a letter with a space
  text = re.sub(r'\W', ' ', text)
  return text

def get_datetime(datetime_string, datetime_format, tzname='UTC'):
  return datetime.strptime(datetime_string, datetime_format).date()

supportTickets = []
apiRequest = requests.get(url, auth=(f"{email}/token", token)).json()['tickets']

for item in apiRequest:
  ticket = {
    "id" : item['id'],
    "date" : str( get_datetime(item['created_at'][:-4].replace('T', ' '), '%Y-%m-%d %H:%M') ),
    "subject" : item['subject'],
    "message" : item['description'],
    "api_message" : preprocess(item['description'])[:500],
    "tags" : item['tags'],
    "status" : item['status'],
    "link" : "https://octopi.zendesk.com/agent/tickets/" + str(item['id'])
  }
  supportTickets.append( ticket )

# supportTickets = {"tickets": []}
# while url:
#   response = requests.get(url, auth=(f"{email}/token", token))
#   supportTickets["tickets"].extend(response.json()["tickets"])
#   url = response.json()["next_page"]
