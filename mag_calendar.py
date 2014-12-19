#!c:\python27\python.exe
import lib_mag_calendar, cgi, lib_error
if __name__ == "__main__":
#	try:
	lib_mag_calendar.main( cgi.FieldStorage () )
	#except Exception, err:										
		#lib_error.DoException( Exception, err)
