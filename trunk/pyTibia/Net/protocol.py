from socket import socket, AF_INET, SOCK_STREAM
from pyTibia.Net.NetworkMessage import NetMsg
from time import sleep

MAX_MSG_SIZE = 8192

class ProtocolBase(object):
	address = ''
	acc = 0
	pswd = ''
	name = ''
	port = 7171
	sock = socket(AF_INET, SOCK_STREAM)
		
	def connect(self):
		self.sock.connect((self.address, self.port))
		return True
			
class Protocol76(ProtocolBase):

	def __init__(self, address = 'localhost', acc = 111111, pswd = 'tibia', name = 'Yurez', port = 7171):
		self.address = address
		self.acc = acc
		self.pswd = pswd
		self.name = name
		self.port = port

		self.packets = { 0x14:self.onErrPacket, }
		
	def getLoginPacket(self):
		msg = NetMsg()
		msg.addU16(0x020A)
		msg.addByte(0)
		msg.addU16(760)
		msg.addByte(0)
		msg.addU32(self.acc)
		msg.addString(self.name)
		msg.addString(self.pswd)
		return msg.getPreparedMsg()
		
	def login(self):
		self.sock.send(self.getLoginPacket())
		msg = self.sock.recv(MAX_MSG_SIZE)
		if len(msg) == 0:
			print 'Login error: Wrong acc, password, or char name'
			return
		self.parsePacket(NetMsg(msg))
		
	def parsePacket(self, msg):
		packetId = msg.getByte()
		self.packets[packetId](msg)
		
	def onErrPacket(self, msg):
		print 'Login error:',msg.getString()