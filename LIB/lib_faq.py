import cgitb 
#cgitb.enable()
import cgi
import MakeHTML


faq_pages = {
	"faq": { 'TITLE': "Povidi - My Accessible Google",
					'TEMPLATE': "./calendar_template.html"
					}
}


def main( dets ):
	print "Content-type: text/html\n"
	print
	print MakeHTML.DoSinglePage (faq_pages, "faq", False )


if __name__ == "__main__":
	main( cgi.FieldStorage() )
