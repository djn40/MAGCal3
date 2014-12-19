import cgi, cgitb 
#cgitb.enable()
import MakeHTML
import MAGCookie, StringIO, pickle
import lib_google, calGlobals, lib_cal_datetime
import datetime, sys
from oauth2client.client import flow_from_clientsecrets



if sys.platform == 'win32':
	gblGoogleReturnAddress  = "http://localhost/dev/povidi/site/mag/google_return.py"
	gblRefreshAddress  = "http://localhost/dev/povidi/site/mag/mag_calendar.py"
else:
	gblGoogleReturnAddress  = "http://povidi.com/mag/google_return.py"
	gblRefreshAddress  = "http://povidi.com/mag/mag_calendar.py"

gblGoogleScope ='http://www.google.com/calendar/feeds/'

main_pages = {
	"calendar": { 'TITLE': "My Accessible Google Calendar",
						'TEMPLATE': "calmain_template.html",
						"DayList" : [], "No_Entries": "", "Msg_Str": "", "Err_Str": ""
						},
	"index": { 'TITLE': "Povidi - My Accessible Google",
					'TEMPLATE': "calindex_template.html"
					},
	"test_only" : {'TEMPLATE': "test.html"}
}



def GetToday ( ctz ):
	return lib_cal_datetime.GetUserNow ( ctz )	

def GetCTZ ():
	ret = MAGCookie.GetCookieStr( "CTZ")
	if ret == "" or ret == None:
		return "+00:00"
	if ret[0] != '-' and ret[0] != '+':
		ret = '+' + ret
	return ret


def GetAuthSubUrl( next, scope):
	flow = flow_from_clientsecrets('client_secret.json',
                               scope=scope,
                               redirect_uri=next)
	return flow.step1_get_authorize_url()



def SetLastQueryCookies( qp, qs, qe):
	MAGCookie.SetCookieStr( "LastQP", qp, Queue=True)
	MAGCookie.SetCookieStr("LastQS", qs, Queue=True)
	MAGCookie.SetCookieStr("LastQE", qe, Queue=True)


def DoLastCookieQuery( cd, cso, today, ctz, calid ):
	LastQP = MAGCookie.GetCookieStr("LastQP")
	LastQS = MAGCookie.GetCookieStr( "LastQS" )
	LastQE = MAGCookie.GetCookieStr( "LastQE" )
	if LastQP != "":
		main_pages["calendar"]["DayList"] = lib_google.DoQuickPick( cso, LastQP, today, ctz, calid)
		main_pages["calendar"]["Msg_Str"] += "<h3>%s</h3>" % LastQP

	elif (LastQS != "" and LastQE != ""):
		event_list = lib_google.GetEvents( cso, LastQS, LastQE, ctz, calid)
		main_pages["calendar"]["DayList"] = event_list					 
		gs = lib_cal_datetime.MthFirstStr( LastQS)
		ge = lib_cal_datetime.MthFirstStr( LastQE)
		main_pages["calendar"]["Msg_Str"] += "<h3>%s To %s</h3>" % (gs, ge)		
	else:
		main_pages["calendar"]["DayList"] = lib_google.DoQuickPick( cso, "Today", today, ctz, calid)

	DoPrint( MakeHTML.DoSinglePage( main_pages, 'calendar', False) )


def DoQuickQuery( dets, cd, cso, ctz, today, calid ):
	val = dets["QuickPick"].value
	main_pages["calendar"]["Msg_Str"] += "<h3>%s</h3>" % val
	main_pages["calendar"]["DayList"] = lib_google.DoQuickPick( cso, val, today, ctz, calid)
	SetLastQueryCookies(val, "", "")
	DoPrint( MakeHTML.DoSinglePage(main_pages, 'calendar', False) )


def DoQuery ( dets, cd, cso, ctz, calid ):
	#validate here 
	try:
		StartDate_str = lib_cal_datetime.Web2GDt (	dets["SYear"].value, dets["SMonth"].value, 	dets["SDay"].value )
		EndDate_str = lib_cal_datetime.Web2GDt (	dets["EYear"].value, 
		dets["EMonth"].value, 	dets["EDay"].value )
		EndDate_str = lib_cal_datetime.PyDt2GDt( lib_cal_datetime.GDt2PyDt( EndDate_str) + lib_cal_datetime.DeltaDtDays(1))
		if lib_cal_datetime.GDt2PyDt(StartDate_str) > lib_cal_datetime.GDt2PyDt(EndDate_str):
			raise
	except:
		main_pages["calendar"]["Msg_Str"] += "<h2>Invalid dates - Query could not run.</H2>"
		ShowCalendar( cd, cso )
	
	event_list = lib_google.GetEvents( cso, StartDate_str, EndDate_str, ctz, calid)
	main_pages["calendar"]["DayList"] = event_list
	gs = lib_cal_datetime.MthFirstStr( StartDate_str)
	ge = lib_cal_datetime.MthFirstStr( EndDate_str)
	main_pages["calendar"]["Msg_Str"] += "<h3>%s To %s</h3>" % (gs, ge)
	SetLastQueryCookies("", StartDate_str, EndDate_str)
	DoPrint( MakeHTML.DoSinglePage( main_pages, 'calendar', False ) )


def DoQuickEntry ( cd, cso, dets, ctz, PyToday, CurrCal ):
	if dets.has_key('QuickEntryDets'):
		val = dets["QuickEntryDets"].value
		if val != "" and val != None:
			res = lib_google.DoQuickEntry( cso, val, ctz)
			main_pages["calendar"]["Msg_Str"] += "<h2>Quick Calendar Entry Added</H2>"
	else:
		main_pages["calendar"]["Msg_Str"] += "<h2>No information to add to calendar.</H2>"
	DoLastCookieQuery ( cd, cso, PyToday, ctz, CurrCal )	


def CheckEmptyEvents ( page ):
	"""Assumes existence of 2 keys in the dic
	"""
	if main_pages[page]["DayList"] == []:
		main_pages[page]["No_Entries"] = calGlobals.NO_EVENTS_STR
	return True


def DoDelCalEvent ( cso, dets ):
	event = dets["DelCalEvent"].value
	res = lib_google.DeleteEvent( cso, event )
	if not res:
		main_pages["calendar"]["Msg_Str"] += "<H2>Event Deleted Successfully</H2>"
	else:
		main_pages["calendar"]["Msg_Str"] += "<H2>Failed to delete Event</H2> "+str(res)


def GetCurrentCalendar ( caldic ):
	if caldic.has_key("calid"):
		return caldic["calid"]
	return "default"

def DoPrint ( s ):
	print "Content-type: text/html"
	print MAGCookie.GetCookieQueue()
	print
	print s


def ShowIndex():
	main_pages["index"]["GOOGLEURL"] = str( GetAuthSubUrl (calGlobals.redirect_uri, calGlobals.scope) )
	retstr = MakeHTML.DoSinglePage ( main_pages, "index", False )
	DoPrint( retstr )



def ShowCalendar( cd = None, cso = None, refresh=False):
	if refresh:
		main_pages['calendar']['refresh'] = '<meta http-equiv="refresh" content="1;url=%s">' % gblRefreshAddress
	else:
		if cd == None or cso == None:
			cd, cso = MAGCookie.getCalendarCookieDicAndCSO()		
		ctz = GetCTZ ()			
		PyToday = GetToday ( ctz )
		CurrCal = GetCurrentCalendar ( cd )
		main_pages["calendar"]["DayList"] = lib_google.DoQuickPick( cso, "Today", PyToday, ctz, CurrCal)
		#main_pages["calendar"]["DayList"] = lib_google.GetAllEvents( cso)
		CheckEmptyEvents( "calendar" )
	retstr = MakeHTML.DoSinglePage ( main_pages, "calendar", False )
	DoPrint ( retstr )


def main( dets ):

	retstr = ""
	cd, cso = MAGCookie.getCalendarCookieDicAndCSO()		
	if cd == {}:
		MAGCookie.ExpireCookies()
		ShowIndex()
		return 0

	ctz = GetCTZ ()			
	PyToday = GetToday ( ctz )
	CurrCal = GetCurrentCalendar ( cd )

	if dets.has_key("SubmitQuickQuery"):
		DoQuickQuery ( dets, cd, cso, ctz, PyToday, CurrCal )

	elif dets.has_key( "SubmitQuery"):
		DoQuery ( dets, cd, cso, ctz, CurrCal  )

	elif dets.has_key( "SubmitQuickEntry" ) or dets.has_key("QuickEntryDets"):
		DoQuickEntry ( cd, cso, dets, ctz,  PyToday, CurrCal )

	elif dets.has_key("DelCalEvent" ):
		DoDelCalEvent( cso, dets )
		#DoLastCookieQuery ( cd, cso,PyToday, ctz, CurrCal )
		main_pages["calendar"]["DayList"] = lib_google.DoQuickPick( cso, "Today", PyToday, ctz, CurrCal)

	else:
		ShowCalendar(cd , cso)







if __name__ == "__main__":
	#main( cgi.FieldStorage() )
		print "main"
	
