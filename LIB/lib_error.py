import cgitb 
#cgitb.enable()
import cgi
import MakeHTML, MAGCookie
import urllib2
import sys, traceback, linecache

error_pages = {
	"error": { 'TITLE': "Povidi - My Accessible Google - Error",
					'TEMPLATE': "./calendar_template.html",
					'ERR_STR': "Unknown Error in Unknown code block."
					}
}



def main( dets ):
	print "Content-type: text/html\n"
	print
	print MakeHTML.DoSinglePage (error_pages, "error", False )	
	
def DoException ( ThisExcept, ExceptStr):
	MAGCookie.ExpireCookies()
	error_pages["error"]['ERR_STR'] = "<h4>%s</h4>%s" % (sys.exc_type, sys.exc_value)
	exc_type, exc_value, exc_traceback = sys.exc_info()
	filename = exc_traceback.tb_frame.f_code.co_filename
	lineno = exc_traceback.tb_lineno
	line = linecache.getline(filename, lineno)
	error_pages['error']['ERR_STR'] += "<h4>exception occurred at %s:%d: %s</h4> and %s" % (filename, lineno, line, str(exc_traceback))
	main ( cgi.FieldStorage() )

def test():
	try:
		print "hello"
		raise IOError("Darryl reckons this will fail")
	except Exception, err:
		DoException( Exception, err)


if __name__ == "__main__":
	#main( cgi.FieldStorage() )
	test()
