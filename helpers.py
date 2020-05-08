import json
import time
import copy
from tone_analyzer import *
from zendesk import *
import pickle

def write_to_file(file, data):
  with open(file, 'wb') as f:
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def read_from_file(file):
  with open(file, 'rb') as f:
    return pickle.load(f)

def getTickets():
  # 1- Read the data.json file
  tickets_from_file = read_from_file('data.json')
  # 2- Get the latest support tickets from Zendesk
  tickets_from_api = supportTickets

  ids_from_file = [ item['id'] for item in tickets_from_file ]
  ids_from_api = [ item['id'] for item in tickets_from_api ]

  # 3- Compare the latest tickets with the data.json by ticket ID remove duplicates
  if set(ids_from_api) != set(ids_from_file):
    if tickets_from_file:
      # 4- Run remaining ticket through gather_watson_sentiment_data()
      newTickets = [ ticket for ticket in tickets_from_api if ticket['id'] not in ids_from_file ]

      tickets_from_file += gather_watson_sentiment_data( newTickets[:2] )

      # 5- re-write the data.json file with new tickets
      write_to_file( 'data.json', tickets_from_file )

    else:
      tickets_from_file += gather_watson_sentiment_data( supportTickets[:2] )
      write_to_file( 'data.json', tickets_from_file )

  tickets_from_file = read_from_file('data.json')

  return tickets_from_file


def udpate_data_json( ticket ):
  tickets_from_file = copy.deepcopy(getTickets())

  for i in range(len(tickets_from_file)):
    current_ticket = tickets_from_file[i]
    if ticket['id'] == current_ticket['id']:
      tickets_from_file[i] = ticket

  write_to_file( 'data.json', tickets_from_file )


def sentiment_trainer():
  sentiment_trainer = []
  for ticket in getTickets():
    sentiment_trainer.append(
      {
        "message": ticket.get("message", ""),
        "tones": [ item['tone_name'] for item in ticket['tones']],
        "emotion": ticket.get("emotion", "")
      }
    )
  return sentiment_trainer


def get_sentiments():
  pass
  # sentiments = {
  #   'tones': {},
  #   'emotions': {}
  # }

  # for item in getTickets():
  #   if item['emotion'] in sentiments['emotions']:
  #     sentiments['emotions'][item['emotion']] += 1
  #   else:
  #     sentiments['emotions'][item['emotion']] = 1

  #   if item['emotion'] in sentiments['emotions']:
  #     sentiments['emotions'][item['emotion']] += 1
  #   else:
  #     sentiments['emotions'][item['emotion']] = 1

  # return sentiments
