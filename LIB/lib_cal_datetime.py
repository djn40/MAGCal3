#Series of functions to do date time conversions and manipulations for interaction between python datetime object, google api and web front end

import time,datetime
import calGlobals


def PyDt2GDt ( dt ):
	return dt.strftime("%Y-%m-%d")

def GDt2PyDt ( s ):
	tm = time.strptime( s, "%Y-%m-%d" )
	return datetime.datetime.fromtimestamp(time.mktime(tm))  


def Web2PyDt( y, m, d ):
	return GDt2PyDt( "%s-%s-%s" % (y,m,d) )

def Web2GDt( y, m, d ):
	return "%s-%s-%s" % (y,m,d)

def MthFirstStr( gdate_str):
	s=gdate_str.split('-')
	return "%s %s, %s" % (calGlobals.NumMthToStr[s[1]],s[2],s[0])

def DeltaDtDays( d):
	return datetime.timedelta(days=d)

def DeltaDtHours( h ):
	return datetime.timedelta(hours=h)


def GetStartEndFromDelta ( sdt, delta ):
	""" return tuple of start and end date with delta
	"""
	return (sdt, sdt+DeltaDtDays( delta ) )

def GetToday( now ):
	return( GetStartEndFromDelta( now, 1) )

def GetTomorrow( now ):
	s,e = GetToday( now )
	return GetStartEndFromDelta( e, 1 )

def GetNext2Days( now ):
	return GetStartEndFromDelta( now, 2)

def GetNext5Days( now ):
	return GetStartEndFromDelta( now, 5)

def GetNext7Days( now ):
	return GetStartEndFromDelta( now, 7)

def GetNext14Days( now ):
	return GetStartEndFromDelta( now, 14)

def GetToEOM ( now ):
	s = PyDt2GDt ( now).split('-')
	i=[]
	for x in s:
		i.append( int(x) )
	if i[1] == 12:
		i[1] = 1
		i[0]+=1
	else:
		i[1]+=1
	i[2]=1
	return (now, GDt2PyDt( "%s-%s-%s" % (i[0],i[1],i[2]) ) )

def GetNextMth( now ):
	sdt,edt = GetToEOM( now)
	return GetToEOM( edt )

def GetQuickPickDates ( now, param ):

	dispatch = { 'Today': GetToday, 'Tomorrow': GetTomorrow, 
	'Next 2 Days':	GetNext2Days, 'Next 5 Days': GetNext5Days, 
	'Next 7 Days': GetNext7Days, 'Next 2 Weeks': GetNext14Days, 
	'Remainder of Month': GetToEOM, 	'Next Month': GetNextMth }

	if param in calGlobals.ValidQuickPicks:
		return dispatch[param]( now )
	else:
		return dispatch['Today'](now)




def AMPM_Str ( hr_str, min_str):
	if hr_str == '' or min_str == '':
		return ''
	if int(hr_str) < 12:
		ampm = 'am'
		if int(hr_str) == 0:
			hr_str='12'
	else:
		ampm = 'pm'
		if int(hr_str) > 12:
			hr_str = str(int(hr_str)-12)
	return "%s:%s%s" % (hr_str, min_str, ampm)



def DatePlusTZ(date, ctz):
	""" ctz MUST have format (+/-)HH:MM ONLY
	"""
	if ":" in ctz:
		chunks=[int(i) for i in ctz.split(":")]
		newDate=date+datetime.timedelta(hours=chunks[0],minutes=chunks[1])
		return newDate
	return None

def GetUserNow(tz):
	today=datetime.datetime.utcnow()
	return DatePlusTZ(today,tz)


if __name__ == "__main__":
	dt = datetime.datetime.now()
	print PyDt2GDt( dt)
	print PyDt2GDt( dt+DeltaDtDays(1) )
	print GetQuickPickDates( dt, 'Next Month')
