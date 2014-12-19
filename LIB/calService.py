#!c:\python27\python.exe
import httplib2
from apiclient.discovery import build
def getServiceObject(credentials):
	"""Given a credentials object, returns a valid service object."""
	http = httplib2.Http()
	http = credentials.authorize(http)
	return build('calendar', 'v3', http=http)

