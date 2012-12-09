Icecast
=======

A python module for getting statistics from an Icecast server.  It requires python-requests to 
make HTTP requests to the server, and Element Tree to parse the XML returned.

Example usage:

	>>> from Icecast.py import IcecastServer
	>>> myhost = IcecastServer("myhost","localhost","8000","username","password")
	>>> for m in myhost.Mounts:
	...  print (myhost.Name + m.Name)
	...  for l in m.Listeners:
	...   print ("  " + l.IP + " connected for " + l.Connected + " seconds.  User Agent: " + l.UserAgent) 
	... 
	myhost/mount-point-one
	 43.25.36.121 connected for 4308 seconds.  User Agent: VLC/2.0.1 LibVLC/2.0.1
	 89.34.11.53 connected for 208 seconds.  User Agent: NSPlayer/12.00.7601.17514 WMFSDK/12.00.7601.17514
	myhost/mount-point-two
	 174.53.25.11 connected for 6 seconds.  User Agent: iTunes/10.7 (Macintosh; Intel Mac OS X 10.6.8) AppleWebKit/534.51.22
  

