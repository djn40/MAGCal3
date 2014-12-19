#!/usr/bin/python
import cgitb
import lib_faq, lib_error
import cgi
try:
	lib_faq.main( cgi.FieldStorage() )
except Exception, err:
		lib_error.DoException( Exception, err)
