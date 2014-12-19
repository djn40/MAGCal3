iv="DylanIsA"
keyCode="0338525903040501"
scope='https://www.googleapis.com/auth/calendar'
redirect_uri='http://localhost/mag/google_return.py'



debug=1

ValidQuickPicks = [ 'Today', 'Tomorrow', 'Day After Tomorrow', 'Next 2 Days',
							'Next 5 Days', 'Next 7 Days', 'Next 2 Weeks',
							'Remainder of Month', 'Next Month']

ValidDaysForMonth = {	'January': 31, 'February':29, 'March':31, 'April':30,											'May':31, 'June':30, 'July': 31, 'August':31,															'September':30, 'October':31,	'November':30,													'December':31 }

MinYear = 2001
MaxYear = 2050

NumMthToStr = {'01':'January', '02':'February', '03':'March', '04':'April',
								'05':'May', '06':'June', '07':'July', '08':'August',
								'09':'September', '10':'October', '11':'November', 
								'12':'December' }

IntMthToStr = {1:'January', 2:'February', 3:'March', 4:'April',
								5:'March', 6:'June', 7:'July', 8:'August',
								9:'September', 10:'October', 11:'November', 
								12:'December' }



NumDOWToStr = {'0':'Monday', '1':'Tuesday', '2':'Wednesday', '3':'Thursday',
							'4':'Friday', '5':'Saturday', '6':'Sunday'}

NO_EVENTS_STR = "<H2>No Entries for Today or Your Chosen Dates</H2>Please make a choice from either the Quick Pick option or the custom date range set and submit your query</P>"
