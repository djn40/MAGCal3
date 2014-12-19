#!c:\python27\python.exe

import MAGCookie
from calService import getServiceObject
import datetime, lib_google

print "Content-Type: text/html"
print

def dformat(x):
	return datetime.datetime.strftime(x, '%Y-%m-%dT%H:%M:%SZ')

creds=MAGCookie.getCreds()
service=getServiceObject(creds)
today=datetime.datetime.now()
day=datetime.timedelta(days=2)  
yesterday=today-day
tomorrow=today+day

request = service.events().list(calendarId='primary', timeMax = dformat(tomorrow), timeMin=dformat(yesterday), singleEvents=True)
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
	d=lib_google.BasicEventDataToDic(event)
	print d
	print "<br />"
  # Get the next request object by passing the previous request object to
  # the list_next method.
  request = service.events().list_next(request, response)



print dformat(today)