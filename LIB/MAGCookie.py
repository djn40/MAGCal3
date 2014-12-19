#!c:\python27\python.exe


import calGlobals, calService, Cookie,datetime,os,cgitb
cgitb.enable()
import pickle, StringIO, xtea_enc

CookieQueue = []
def log(t):
	f=open("c:\wamp\www\mag\log.txt","a")
	f.write(str(t))
	f.write("\n")
	f.close()

def SetCookieQueue( mc ):
	global CookieQueue
	CookieQueue.append( str(mc) )
	log(mc)

def GetCookieQueue():
	global CookieQueue
	ret = ""
	for x in CookieQueue:
		ret += "%s\n" % x
	CookieQueue = []
	return ret


def GetCookieStr ( cookie_name ):
	val = None
	if 'HTTP_COOKIE' in os.environ:
		cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
		if cookie_name in cookie:
			val=  cookie[ cookie_name ].value 
	return val

def SetCookieStr( cookie_name, data, delta=30, Queue = False):
		mc = Cookie.SimpleCookie()
		mc[cookie_name] = data
		expires=datetime.datetime.now() + datetime.timedelta(days=delta)
		mc[cookie_name]["expires"] =expires.strftime("%a, %d-%b-%Y %H:%M:%S PST")
		if Queue == False:
			print mc
		else:
			SetCookieQueue( mc )

		return True



def setCalendarCookie( data ):
	return SetCookieStr( "calendarData", xtea_enc.crypt(calGlobals.keyCode, data), Queue=False)

def getCalendarCookieDic( ):
	""" Once a call to GetCalendarCookie we need to make a dictionary from the data 
	"""
	cs = GetCookieStr( "calendarData" )
	if cs == None: return {}
	cs = xtea_enc.crypt(calGlobals.keyCode, cs)
	if cs == "" or cs == None or str == 'None':
		return {}
	return eval( str(cs) )
def saveCreds(creds):
	cookie_data = {}
	credsStream = StringIO.StringIO()
	pickle.dump(creds, credsStream )
	tmp = credsStream.getvalue()
	cookie_data["creds"] = str(tmp)
	setCalendarCookie(  str(cookie_data) )

def DeriveCreds( creds_str ):
	creds_file = StringIO.StringIO( str(creds_str ))
	return pickle.load( creds_file)
def getCreds():
	creds=getCalendarCookieDicAndCreds()[1]
	return creds


def getCalendarCookieDicAndCreds():
	cd = getCalendarCookieDic ()
	#print cd
	if cd == {}:
		return ({}, None )
	else:
		creds = None
		if "creds" in cd:
			creds = DeriveCreds( cd["creds"] )
		return (cd,creds)
def getCalendarCookieDicAndCSO():
	cd, creds = getCalendarCookieDicAndCreds()
	cso=calService.getServiceObject(creds)
	return (cd, cso)



def GetTodayCookieStr ():
	return GetCookieStr("today")

def GetTZCookie ():
	return GetCookieStr( "CTZ" )

def ExpireCookies ( CookieList = ['CTZ', 'today', 'calendarData', 'LastQP', 'LastQS', 'LastQE'] ):
	for c in CookieList:
		SetCookieStr( c, '', -30, True)



if __name__ == "__main__":
	setCalendarCookie ( {} )
	#SetCookieStr( 'ctz', '12:00')

	print GetCookieQueue()