from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import copy

ibmTokens = {}

with open('ibm-credentials-yordan.env', 'r') as t:
  for line in t.readlines():
    lineSplit = line.split('=')
    ibmTokens[ lineSplit[0] ] = lineSplit[1].replace('\n', '')

authenticator = IAMAuthenticator( ibmTokens['TONE_ANALYZER_APIKEY'] )
tone_analyzer = ToneAnalyzerV3(
  version='2020-04-29',
  authenticator=authenticator
)

tone_analyzer.set_service_url( ibmTokens['TONE_ANALYZER_URL'] )

tones = {
  "joy": 0,
  "anger": 1,
  "fear": 2,
  "analytical": 3,
  "sadness": 4,
  "confident": 5,
  "tentative": 6
}

emotions = {
  "excited": 0,
  "frustrated": 1,
  "impolite": 2,
  "polite": 3,
  "sad": 4,
  "satisfied": 5,
  "sympathetic": 6
}

pill = {
  0: "success" ,
  1: "danger" ,
  2: "dark" ,
  3: "primary" ,
  4: "info" ,
  5: "success" ,
  6: "light"
}

statuses = {
  "open": 0,
  "pending": 1,
  "solved": 2,
  "closed": 3
}

def get_label_color(item):
  label = "light"
  if item in tones: label = pill[tones[item]]
  if item in emotions: label = pill[emotions[item]]
  return label

def get_watson_utterance( chat ):
  emotion = tone_analyzer.tone_chat(chat).get_result()
  return emotion['utterances_tone']

def get_watson_tones( message ):
  tone_analysis = tone_analyzer.tone(
    {'text': message},
    content_type='application/json'
  ).get_result()

  tonesResult = copy.deepcopy(tone_analysis['document_tone']['tones'])

  tonesData = []

  for i in range(len(tonesResult)):
    data = {}
    data['tone_name'] = tonesResult[i]['tone_id']
    data['label'] = get_label_color(data['tone_name'])
    tonesData.append(data)

  return tonesData

def gather_watson_sentiment_data( ticketList ):
  data = copy.deepcopy(ticketList)

  chat = [
    {
      "text": ticket['api_message'] if len(ticket['api_message']) > 0 else "text",
      "user": "system"
    }
    for ticket in data
  ]
  watsonEmotions = get_watson_utterance(chat)

  for i in range( len(data) ):
    ticket = data[i]
    ticket['tones'] = get_watson_tones( ticket['api_message'] )

    if len(watsonEmotions[i]['tones']) > 0:
      emotion = watsonEmotions[i]['tones'][0]['tone_id']
      ticket['emotion'] = {
        'emotion_name': emotion,
        'label': get_label_color(emotion)
      }
  return data
