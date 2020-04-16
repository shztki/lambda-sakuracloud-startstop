import os
import sys
import time
#import inspect
import slack
import json
import requests
import boto3

from saklient.cloud.api import API
from base64 import b64decode

def lambda_handler(event, context):

  #token = os.environ['SAKURACLOUD_ACCESS_TOKEN']
  token = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['SAKURACLOUD_ACCESS_TOKEN']))['Plaintext'].decode('utf-8')
  #secret = os.environ['SAKURACLOUD_ACCESS_TOKEN_SECRET']
  secret = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['SAKURACLOUD_ACCESS_TOKEN_SECRET']))['Plaintext'].decode('utf-8')
  #zone = os.environ['SAKURACLOUD_ZONE']
  zones = ["is1a", "is1b", "tk1a"]
  target_tags = ["autostartstop"]
  action = event['Action']
  #messages = ['', '', '']
  text = ''
  count = 0

  if action == 'Start':
    msg = "おはようございます :sunrise: *以下のサーバを起動しました。* \\n\\n"
    text += '[{"type": "section", "text": {"type": "mrkdwn", "text": "' + msg + '"}},{"type": "section","fields": ['
  elif action == 'Stop':
    msg = "お疲れさまでした :stars: *以下のサーバを停止しました。* \\n\\n"
    text += '[{"type": "section", "text": {"type": "mrkdwn", "text": "' + msg + '"}},{"type": "section","fields": ['

  for zone in zones:
    api = API.authorize(token, secret, zone)
    
    #print('searching servers')
    model_server = api.server
    model_server.with_tags(target_tags)
    servers = model_server.find()
    
    start_list = []
    stop_list = []
    
    for i in servers:
      #print(i.name)
      #print(inspect.getmembers(i.instance))
      #print(i.instance.status)  
      if i.instance.status == 'down' and action == 'Start':
        start_list.append(i.id)
      elif i.instance.status == 'up' and action == 'Stop':
        stop_list.append(i.id)
    
    #print('Zone ->', zone)
    #messages[count] += ':sacloud-green: Zone -> ' + zone + '\\n'
    text += '{"type": "plain_text","text": ":sacloud-green: Zone -> ' + zone + '","emoji": true},'
    text += '{"type": "plain_text","text": ":ballot_box_with_check: Result","emoji": true},'
    if start_list:
      #print('Starting', len(start_list), 'instances', start_list)
      #messages[count] += 'Starting' + len(start_list) + 'instances' + start_list + '\\n'
      for i in start_list:
        #messages[count] += model_server.get_by_id(i).get_name() + ' -> '
        text += '{"type": "plain_text","text": "' + model_server.get_by_id(i).get_name() + '","emoji": true},'
        try:
          model_server.get_by_id(i).boot()
          #print('Start:', model_server.get_by_id(i).get_name())
          #messages[count] += 'started\\n'
          text += '{"type": "plain_text","text": ":up:","emoji": true},'
        except Exception as e:
          text += '{"type": "plain_text","text": ":warning: Error:' + str(e) + '","emoji": true},'

  
    elif stop_list:
      #print('Stopping', len(stop_list), 'instances', stop_list)
      #messages[count] += 'Stopping' + len(stop_list) + 'instances' + stop_list + '\\n'
      for i in stop_list:
        #messages[count] += model_server.get_by_id(i).get_name() + ' -> '
        text += '{"type": "plain_text","text": "' + model_server.get_by_id(i).get_name() + '","emoji": true},'
        try:
          model_server.get_by_id(i).shutdown() # stop
          #print('Stop:', model_server.get_by_id(i).get_name())
          #messages[count] += 'stopped\\n'
          text += '{"type": "plain_text","text": ":no_entry:","emoji": true},'
        except Exception as e:
          text += '{"type": "plain_text","text": ":warning: Error:' + str(e) + '","emoji": true},'
    
    count+=1
    text = text.rstrip(",")
    if count < len(zones):
      text += ']},{"type": "divider"},{"type": "section","fields": ['

  #print(messages)
  #j = '[{"type": "section", "text": {"type": "mrkdwn", "text": "' + text + '"}},{"type": "section","fields": [{"type": "plain_text","text": "' + messages[0] + '", "emoji": true},{"type": "plain_text","text": "' + messages[1] + '", "emoji": true},{"type": "plain_text","text": "' + messages[2] + '","emoji": true}]}]'
  text += ']}]'
  json_data = json.loads(text)
  #print(json_data)
  post_to_slack(json_data)

def post_to_slack(message):
  #webhook_url = os.environ['SLACK_WEBHOOK_URL']
  webhook_url = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['SLACK_WEBHOOK_URL']))['Plaintext'].decode('utf-8')
  slack_data = json.dumps({'blocks': message})
  response = requests.post(
      webhook_url, data=slack_data,
      headers={'Content-Type': 'application/json'}
  )
  if response.status_code != 200:
      raise ValueError(
        'Request to slack returned an error %s, the response is:\\n%s'
        % (response.status_code, response.text)
      )

