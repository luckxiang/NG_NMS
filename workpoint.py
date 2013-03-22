import pycurl
import cStringIO

idiot = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'https://ngnms-server/login')
c.setopt(pycurl.TIMEOUT, 10)

c.setopt(pycurl.FOLLOWLOCATION, 1)
c.setopt(c.POSTFIELDS, 'j_username=admin&j_password=manager')
c.setopt(pycurl.COOKIEJAR, 'data/ngnms.cookie')

c.setopt(c.VERBOSE, True)
c.setopt(pycurl.SSL_VERIFYPEER, 0);
 
c.perform()

c.setopt(pycurl.URL, 'https://ngnms-server/users?login=admin')
c.perform()

c.setopt(pycurl.URL, 'https://ngnms-server/folders/config/582')
c.setopt(pycurl.WRITEFUNCTION, idiot.write)

c.perform()
folder = idiot.getvalue()
c.close()

#print "FOLDER: ", folder
abc = eval(folder)
#print "abc: ", abc

for item in abc:
    print item

# for item in folder.lstrip('[').rstrip(']').split('}'):
#     print item.lstrip(',{')

