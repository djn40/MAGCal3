#!c:\python27\python.exe
#import cgitb
import cgi
import lib_index, lib_error
try:
	lib_index.main( cgi.FieldStorage() )
except Exception, err:
		lib_error.DoException( Exception, err)