#!/usr/bin/python
import cgi
import lib_cal_change,lib_error
try:
	lib_cal_change.main( cgi.FieldStorage () )
except Exception, err:
		lib_error.DoException( Exception, err)