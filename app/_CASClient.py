import os, cgi, urllib, re

form = cgi.FieldStorage()

class CASClient:
    def __init__(self):
        self.cas_url = "https://fed.princeton.edu/cas/"

    def Authenticate(self):
      # If the request contains a login ticket, try to validate it
      if form.has_key('ticket'):
         netid = self.Validate(form['ticket'].value)
         if netid != None:
            return netid
         else:
            return None

    def Validate(self, ticket):
        val_url = self.cas_url + "validate" + \
            '?service=' + urllib.quote(self.ServiceURL()) + \
            '&ticket=' + urllib.quote(ticket)
        r = urllib.urlopen(val_url).readlines()   # returns 2 lines
        if len(r) == 2 and re.match("yes", r[0]) != None:
            return r[1].strip()
        return None
    
    def ServiceURL(self):
        if os.environ.has_key('REQUEST_URI'):
            ret = 'http://' + os.environ['HTTP_HOST'] + os.environ['REQUEST_URI']
            ret = re.sub(r'ticket=[^&]*&?', '', ret)
            ret = re.sub(r'\?&?$|&$', '', ret)
            return ret
        return Exception("Missing REQUEST_URI environment variable")
