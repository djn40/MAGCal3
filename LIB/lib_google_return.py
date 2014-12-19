#!c:\python27\python.exe
#import cgitb; cgitb.enable()
import cgi,os, httplib2
import pickle, StringIO
import MAGCookie, lib_mag_calendar, calGlobals
from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from calService import getServiceObject

def getAuthSubCode ():
	query = os.environ[ "QUERY_STRING" ]
	return str(cgi.parse_qs(query)["code"][0])

def getCredsObject():
	"""Returns a credentials object from code in URL. Can only be called once per code."""
	flow = flow_from_clientsecrets('client_secret.json',
							   scope=calGlobals.scope,
							   redirect_uri=calGlobals.redirect_uri)

	authsub_code = getAuthSubCode()
	return flow.step2_exchange(authsub_code)


def DoGoogleReturn ():
	retstr = "starting...<br>"
	creds=getCredsObject()
	#calendar_service = getServiceObject(creds)
	MAGCookie.saveCreds(creds)

	lib_mag_calendar.ShowCalendar(creds, 1, True )
	#print MAGCookie.GetCookieQueue()
	print "Content-type: text/html"
	print
	print """<a href="test.py">Test the shit out</a>"""
	print MAGCookie.getCreds()


	retstr += "<h3>token, calendar_service and cookie created</h3>"
	return (True, retstr)



def main ():
	retstr = DoGoogleReturn ()


if __name__ == '__main__':
	main ( None )