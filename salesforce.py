import requests
import json
from datetime import datetime

def queryAndSaveToTheFile(objectName, condition, afterCondition):
  global auth_token_salesforce
  session = requests.Session()
  headers_dict = {"Authorization": "Bearer " + str(auth_token_salesforce),
                  "Accept" : "*/*",
                  'Content-Type': 'application/json; charset=utf-8'}
  session.headers.update(headers_dict)

  base_endpoint = 'https://yit--devgenus1.my.salesforce.com/services/data/v52.0/query/?q=SELECT+'
  queryFields = 'FIELDS(ALL)'

  if(condition != ''):
    condition = '+WHERE+' + condition.replace(' ', '+')
  else:
    condition = ''

  if(afterCondition != ''):
    afterCondition = '+' + afterCondition.replace(' ', '+')
  else:
    afterCondition = ''

  finalEndpoint = base_endpoint + queryFields + '+FROM+' + objectName + condition + afterCondition + '+LIMIT+100'
  print('endpoint = ' + finalEndpoint)
  r = requests.get(finalEndpoint, headers = session.headers)
  print(str(r))
  if(str(r) == '<Response [400]>'):
    print('RESPONSE IS 400')

  isFirst = True
  if(str(r) == '<Response [200]>'):
    json_data = json.loads(r.text)
    file_output = ''
    for line in json_data['records']:
      for key in line:
        if key != 'attributes':
          value = line.get(key)
          if str(value) == 'None':
            value = ''
          else:
            if str(key) == 'Id':

              space = ''
              if isFirst == True:
                isFirst = False
              else:
                space = '\n\n\n\n\n\n\n'

              file_output += space + str(key) + ',' + '"' + str(value).replace('"','') + '"' + '\n'
            else:
              file_output += str(key) + ',' + '"' + str(value).replace('"','') + '"' + '\n'

    if file_output != '':
      file = open(objectName + ".csv", "w")
      file.write(file_output)
      file.close()
  
config = open('config.json')
data = json.load(config)
username = data.get('username')
password = data.get('password')
print('Username loaded from config.json -> ' + username)
tokenRequest = requests.post("https://test.salesforce.com/services/oauth2/token", data={
    "password": password + "UKa0sUELKLfTJXh1DaDe4C0pq",
    "username": username,
    "client_id": "3MVG9LzKxa43zqdKmeTTNjkqgD7kdz0MLKldZ7biF6_ashxHNPWRbR40XNy3LXAf.88xb_V.zXLGHOiLJwVW1",
    "client_secret": "13ECA1F4747E92570FD8DEE558558214F5813D5BB38FA9A9DDC9738DE6A9D0BE",
    "grant_type": "password"}
)
global auth_token_salesforce
auth_token_salesforce = json.loads(tokenRequest.text)['access_token']
print('salesforce token obtained succesfully')

condition = "lastModifiedDate > 2021-09-02T23:59:00Z AND lastModifiedDate < 2021-09-03T23:59:00Z AND createdBy.UserName LIKE '%vip.integration%'"
afterCondition = 'ORDER BY CreatedDate DESC'
objects = [ "Account", 
            "Opportunity", 
            "ServiceContract",
            "Product2",
            "Project_TT__c",
            "Reservation__c",
            "Contact"
            ]

for object in objects:
  queryAndSaveToTheFile(object,condition,afterCondition)


