#!c:\python27\python.exe

from oauth2client.client import flow_from_clientsecrets
import cgi,os, cgitb, httplib2
from apiclient.discovery import build
import lib_google
import datetime

#cgitb.enable()

query = os.environ[ "QUERY_STRING" ]
print """Content-Type: text/html
"""

flow = flow_from_clientsecrets('client_secret.json',
							   scope='https://www.googleapis.com/auth/calendar',
							   redirect_uri='https://localhost/mag/callback.py')

def getCode(qs):
	"""Given a query string, returns the token"""
	return str(cgi.parse_qs(qs)["code"][0])

code=getCode(query)
print "code is "+code

credentials = flow.step2_exchange(code)
print "Code accepted."



http = httplib2.Http()
http = credentials.authorize(http)
service = build('calendar', 'v3', http=http)

print "created a service object."

now=datetime.datetime.today()

request = service.events().list(calendarId='primary')
#Asking to get a list of events 

# Loop until all pages have been processed.
while request != None:
  # Get the next page.
  response = request.execute()
#all requests need to be exicuted
  # Accessing the response like a dict object with an 'items' key
  # returns a list of item objects (events).
  for event in response.get('items', []):
	# The event object is a dict object with a 'summary' key.
	print repr(event.get('summary', 'NO SUMMARY')) + '<br />'
  # Get the next request object by passing the previous request object to
  # the list_next method.
  request = service.events().list_next(request, response)

a=lib_google.DoQuickEntry(service, "Dinner with Shen on Thursday", None)
print(a["end"])

print str(lib_google.BasicEventDataToDic(a))

now=datetime.datetime.now()
