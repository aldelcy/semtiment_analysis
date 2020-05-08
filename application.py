from flask import Flask, render_template, request
import json
from helpers import *
from zendesk import *

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
  data = { 'tickets': getTickets()[:] }
  data['tones'] = list( tones.keys() )
  data['emotions'] = list( emotions.keys() )
  data['statuses'] = list( statuses.keys() )
  return render_template( 'index.html', viewData = data )

@app.route('/tickets')
def get_tickets():
  return json.dumps(getTickets(), indent=2)

@app.route('/ticket/<id>')
def get_ticket(id):
  ticket = [ ticket for ticket in read_from_file('data.json') if ticket['id'] == int(id) ]
  return json.dumps(ticket, indent=2)

@app.route('/edit_ticket/<id>', methods=['GET', 'POST'])
def edit_ticket(id):
  print( request.form )
  newTones = request.form.get('tones').split(',')
  newEmotion = request.form.get('emotion')

  ticket = [ ticket for ticket in read_from_file('data.json') if ticket['id'] == int(id) ][0]
  ticket['emotion'] = []
  ticket['tones'] = []

  ticket['emotion'] = {
    'emotion_name': newEmotion.strip(),
    'label': get_label_color(newEmotion.strip())
  }

  for tone in newTones:
    ticket['tones'].append(
      {
        'tone_name': tone.strip(),
        'label': get_label_color(tone.strip())
      }
    )

  udpate_data_json( ticket )

  return json.dumps(ticket, indent=2)

app.run()
