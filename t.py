#!c:\python27\python.exe

from oauth2client.client import flow_from_clientsecrets
flow = flow_from_clientsecrets('client_secret.json',
                               scope='https://www.googleapis.com/auth/calendar',
                               redirect_uri='http://localhost/mag/google_return.py')
url=flow.step1_get_authorize_url()
print """Content-Type: text/html
"""
print """<a href="%s">Click to get google</a>""" %(url)
