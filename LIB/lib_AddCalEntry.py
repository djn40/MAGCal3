import cgitb; cgitb.enable()
import cgi
import MakeHTML

cal_entry = {
	"AddCalEntry": { 'TITLE': "My Accessible Google - Calendar Entry",
							'TEMPLATE': "./calendar_template.html"
							}
}
def main( dets ):
	print "Content-type: text/html\n"
	print
	print MakeHTML.DoSinglePage ( cal_entry, "AddCalEntry", False )

if __name__ == "__main__":
	main ( cgi.FieldStorage() )