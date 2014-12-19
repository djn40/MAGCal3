#!/usr/bin/python
import cgitb
import cgi
import lib_about, lib_error
try:
	lib_about.main( cgi.FieldStorage () )
except Exception, err:
		lib_error.DoException( Exception, err)
