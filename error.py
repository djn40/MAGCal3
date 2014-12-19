#!/usr/bin/python
import cgitb
import cgi

import lib_error
lib_error.main( cgi.FieldStorage() )