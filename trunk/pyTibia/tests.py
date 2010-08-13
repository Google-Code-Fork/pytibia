from pyTibia.Net.Protocol import *

if __name__=="__main__":
	print "Test"
	prot = Protocol76(name='Yurez')
	prot.connect()
	prot.login()
	prot.recvLoop()