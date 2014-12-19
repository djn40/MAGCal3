import cgitb; cgitb.enable()
import cgi
import MakeHTML

calendar_list = {
	"cal_change": { 'TITLE': "My Accessible Google - Calendar Entry",
							'TEMPLATE': "./calendar_template.html"
							}
}
def main( dets ):
	print "Content-type: text/html\n"
	print
	print MakeHTML.DoSinglePage ( calendar_list, "cal_change", False )

if __name__ == "__main__":
	main ( cgi.FieldStorage() )