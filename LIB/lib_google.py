#Functions to call into Google API (wrappers) and rendering to format for web view
# see: https://support.google.com/calendar/answer/36604?hl=en
# for useage of the quick entry
#
# for property reference:
# https://developers.google.com/google-apps/calendar/v3/reference/events
#
import time,datetime,cgi,cgitb, httplib2
import os,Cookie,urllib, calGlobals
import xtea_enc
import lib_cal_datetime

def uri_info ( calid ):
	return "/calendar/feeds/"+calid+"/private/full"



def GuiDateTimes( google_dt_str ):
	"""creates a dictionary of useful formats for dates and times
	"""
	ret = { 'dow': '', 'yr' : '', 'day':'', 'mth':'', 'hr':'', 'min':'', 'timestr':'', 'pydt': None, 'sort_time':0, 'sort_dt':0, 'mthstr': '', 'input_str': ''  }

	dt = google_dt_str.split("T")
	ret["input_st"] = "T".join( dt )
	(ret["yr"], ret["mth"], ret["day"]) = dt[0].split('-')
	if len(dt)>1:
		ret["input_str"] += dt[1]
		(ret["hr"],ret["min"]) = (dt[1].split(':'))[0:2]
		ret["timestr"] = lib_cal_datetime.AMPM_Str( ret["hr"], ret["min"] )
	ret["pydt"] = lib_cal_datetime.GDt2PyDt( dt[0] )
	ret["mthstr"]=calGlobals.NumMthToStr[ ret["mth"] ]
	aaa = ret["pydt"]
	ret["dow"] = calGlobals.NumDOWToStr[str(ret["pydt"].weekday())]
	ret["sort_dt"] =  "%s%s%s" % (ret["yr"], ret["mth"],ret["day"]) 
	if ret["hr"] == '' or ret["min"] == '':
		ret["sort_time"] = '0000'
	else:
		ret["sort_time"] =  "%s%s" % (ret["hr"], ret["min"]) 


	return ret		

def RenderSummary ( d ):
	ret = d["Title"]
	if d["Where"] != None or d["Summary"] != None:
		ret += "<BR>"
	if d["Summary"] != None:
		ret+= d["Summary"]
	if d["Where"] != None:
		ret += d["Where"]
	return ret



def BasicEventDataToDic ( event, cso=None, calid=None ):
	#print "Content-type: text/html"
	#print
	#print "<h4>Test : %s</h4>" % event.original_event.href
	ret = {}

	if event.get('recurrence') != None:
		ret["Google_SDate"] = "2014-02-23T00:00:00+00:00"
		ret["Google_EDate"] = "2014-02-23T00:00:00+00:00"
	else:
		ret["Google_SDate"] = event["start"].get('date', "2014-02-23T00:00:00+00:00")
		ret["Google_EDate"] = event["end"].get("date", "2034-02-23T00:00:00+00:00")
	ret["Title"] = event.get("summary")
	ret["Summary"] = event.get("description")
	ret["Where"] = event.get("location")
	ret["EntrySumm"] = RenderSummary( ret )
	ret["EventID"] = event['id']
	if event.get('recurringEventId') != None:
		ret["ParentID"] = event['recurringEventId']
		a= cso.events().get( calendarId='primary', eventId=ret["ParentID"] )
		a=a.execute()
		ret["ParentDelUID"] = a["id"]
	ret["GuiSDate"] = GuiDateTimes( ret["Google_SDate"] )
	ret["GuiEDate"] = GuiDateTimes( ret["Google_EDate"] )
	ret["ShortDtTime"] = "%s	 %s %s - %s" % ( ret["GuiSDate"]["mthstr"], ret["GuiSDate"]["day"], ret["GuiSDate"]["timestr"], ret["GuiEDate"]["timestr"] )
	ret["sort_order"] = "%s%s" % (ret["GuiSDate"]["sort_dt"], ret["GuiSDate"]["sort_time"])
	return ret



def DoQuickEntry( cso, s, ctz, calid="default" ):
	"""cso is the calendar service object to use, s the string and calid the id of the calendar we want to use
	Returns what google does - a tuple with first element being success / failure
	"""
	r = cso.events().quickAdd(calendarId='primary', text=s)
	return r.execute()

def GetAllEvents( cso, ctz, calid="default" ):
	return GetEvents(cso,  "2004-01-01", "2035-12-31", ctz, calid )
def getEventsBetween(cso, std, edt_str, ctz, calid="primary"):
	request = cso.events().list(calendarId='primary', timeMin = std, timeMax= edt_str, singleEvents=True)
	eventList=[]
	while request != None:
		# Get the next page.
		response = request.execute()
		eventList.extend(response.get('items', []))

		request = cso.events().list_next(request, response)
	return eventList


def GetEvents( cso,  sdt_str, edt_str, ctz, calid="default" ):
	#StartDate_str="2011-04-07T02:30:00-07:00" #UTC I think
	StartDate_str="%sT00:00:00%s" % (sdt_str, ctz) #UTC NOT GMT
	EndDate_str="%sT00:00:00%s" % (edt_str, ctz)
	#Use for DEBUG
	#StartDate_str = "2014-02-23T00:00:00+00:00"
	#EndDate_str = "2014-02-24T00:00:00+00:00"
	#cso.sortorder = "a"

	if sdt_str == "" and edt_str == "":
		feed=getEventsBetween(cso,  StartDate_str, EndDate_str, ctz, calid="primary")
	else:
		feed=getEventsBetween(cso,  StartDate_str, EndDate_str, ctz, calid="primary")
	#print "Content-Type: text/html"
	#print
	#print "\n".join([str(i) for i in feed])
	dates_list=[]
	for event in feed:
		d = BasicEventDataToDic ( event, cso, calid )
		if d != None:
			found = False
			for cdate in dates_list:
				if cdate["sort_dt"] == d["GuiSDate"]["sort_dt"]:
					found = True
					cdate["Events"].append( d )
					break
			if not found:
				new_date_dic = {}
				new_date_dic["sort_dt"] = d["GuiSDate"]["sort_dt"]
				new_date_dic["dow"] = d["GuiSDate"]["dow"]
				new_date_dic["day"] =d["GuiSDate"]["day"]
				new_date_dic["mthstr"]=d["GuiSDate"]["mthstr"]
				new_date_dic["yr"]=d["GuiSDate"]["yr"]
				new_date_dic["Events"] = []
				new_date_dic["Events"].append( d )
				dates_list.append(new_date_dic)

	#sort
	dates_list.sort( key=lambda x: x["sort_dt"] )
	for date in dates_list:
		date["Events"].sort( key=lambda x: x["sort_order"] )


	#finally hack out Google's day bug issues

	s = sdt_str.split("-")
	OurStart = int("%s%s%s" % (s[0],s[1],s[2]))
	s = edt_str.split("-")
	OurEnd = int("%s%s%s" % (s[0],s[1],s[2]))
	for cdate in range( len(dates_list)-1, -1, -1):
		GStart = int( dates_list[cdate]["sort_dt"])
		if GStart < OurStart or GStart>OurEnd:
			del dates_list[ cdate ]

	return dates_list

def DeleteEvent(cso, event_id):
	return cso.events().delete(calendarId='primary', eventId=event_id).execute()
	#return cso.DeleteEvent( event_id )


def DoQuickPick ( cso, QP_Param, today, ctz, calid="default"):
	PyStartDate, PyEndDate = lib_cal_datetime.GetQuickPickDates( today, 
	QP_Param)
	StartDate_str = lib_cal_datetime.PyDt2GDt( PyStartDate )
	EndDate_str = lib_cal_datetime.PyDt2GDt( PyEndDate )
	return GetEvents( cso, StartDate_str, EndDate_str, ctz, calid)


def DoLogout ( creds ):
	if creds != None:
		return creds.revoke(httplib2.Http())
	return True


if __name__ == "__main__":
	#print GuiDateTimes( '2011-04-04T14:00:00.000+12:00' )
	print "hi"