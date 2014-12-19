import cgitb 
#cgitb.enable()
import cgi
import MakeHTML
import gdata.calendar.service
import gdata.auth
import urllib2


about_pages = {
	"about": { 'TITLE': "Povidi - My Accessible Google",
					'TEMPLATE': "./calendar_template.html"
					}
}


def main( dets ):
	print "Content-type: text/html\n"
	print
	
	print MakeHTML.DoSinglePage (about_pages, "about", False )






if __name__ == "__main__":
	main()



