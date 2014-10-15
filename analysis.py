# -*- coding: utf-8 -*-
#!/usr/bin/python

import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
import json


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = '/Users/purav.aggarwal/Documents/Purav/ResearchMe/Gmail/client_secret_420499423545-cnsrrvqkdsld299sop84qv3it8lkc70h.apps.googleusercontent.com.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
#IMP: https://developers.google.com/apis-explorer/#p/gmail/v1/
gmail_service = build('gmail', 'v1', http=http)
ids = gmail_service.users().messages().list(userId = "****@gmail.com",q="to:user@spark.apache.org", maxResults = 10,includeSpamTrash = False,fields="messages").execute()

companyCount = {}
personCount = {}
for id_thread in ids['messages']:
    id1 = id_thread['id']
    thread = id_thread['threadId']
    final_res = gmail_service.users().messages().get(userId = "****@gmail.com",id=id1,format="full",fields="payload").execute()
    for kv in final_res['payload']['headers']:
        if(kv['name'] == 'From'):
            emailId = kv['value']
            company = emailId.split('@')[1].split('.')[0]
            name = emailId.split(' <')[0]+"_"+company
            if(companyCount.has_key(company)):
                companyCount[company] += 1
            else:
                companyCount[company] = 1
            if(personCount.has_key(name)):
                personCount[name] += 1
            else:
                personCount[name] = 1


'''
# Retrieve a page of threads
threads = gmail_service.users().threads().list(userId='me').execute()

# Print ID for each thread
if threads['threads']:
  for thread in threads['threads']:
    print 'Thread ID: %s' % (thread['id'])
'''
