import cgitb 
cgitb.enable()
import cgi
import MAGCookie, lib_mag_calendar, lib_google, calService



def ShowIndexPage ():
	lib_mag_calendar.ShowIndex()


																									   

def main( dets ):
	cd, creds = MAGCookie.getCalendarCookieDicAndCreds()

	if dets.has_key("DoGoogleLogout"):
		#cso=calService.getServiceObject(creds)
		lib_google.DoLogout( creds )
		cso = None;
		cd = {}
		MAGCookie.setCalendarCookie( cd )
		ShowIndexPage ()
	else:
		if creds == None:
			ShowIndexPage ()
		else:
			lib_mag_calendar.ShowCalendar()



if __name__ == "__main__":
	main( cgi.FieldStorage() )
