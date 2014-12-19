#!/usr/bin/python
import cgitb
import cgi
import lib_AddCalEntry, lib_error
try:
	lib_AddCalEntry.main( cgi.FieldStorage () )
except Exception, err:
		lib_error.DoException( Exception, err)