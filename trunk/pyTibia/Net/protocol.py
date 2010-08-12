from socket import socket, AF_INET, SOCK_STREAM
from pyTibia.Net.NetworkMessage import NetMsg
from time import sleep

MAX_MSG_SIZE = 8192

DEBUG = True

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

	speakClasses = { 
		'SPEAK_SAY'         :0x01,
		'SPEAK_WHISPER'     :0x02,
		'SPEAK_YELL'        :0x03,
		'SPEAK_BROADCAST'   :0x09,
		'SPEAK_PRIVATE'     :0x4,
		'SPEAK_PRIVATE_RED' :0x0B,
		'SPEAK_CHANNEL_Y'   :0x05,
		'SPEAK_CHANNEL_R1'  :0x0A,
		'SPEAK_CHANNEL_R2'  :0x0E,
		'SPEAK_CHANNEL_0'   :0x0C,
		'SPEAK_MONSTER1'    :0x10,
		'SPEAK_MONSTER2'    :0x11,
	}

	def __init__(self, address = 'localhost', acc = 111111, pswd = 'tibia', name = 'Yurez', port = 7171):
		self.address = address
		self.acc = acc
		self.pswd = pswd
		self.name = name
		self.port = port

		self.packets = { 
			0x14:self.onErrPacket, 
			0x1E:self.onPingPacket,
			0xAA:self.onMessagePacket,
		}
		
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
		
	#for now
	#TODO asynchronous
	def recvLoop(self):
		while True:
			msg = self.sock.recv(MAX_MSG_SIZE)
			self.parsePacket(NetMsg(msg))
		
	def parsePacket(self, msg):
		packetId = msg.getByte()
		try:
			self.packets[packetId](msg)
		except KeyError:
			print 'Unknown packet type:', '%x' % packetId
		
	def onErrPacket(self, msg):
		print 'Login error:',msg.getString()
	
	def onPingPacket(self, msg):
		if DEBUG:
			print 'Ping <-> Pong'
		msg.reset()
		msg.addByte(0x1E)
		self.sock.send(msg.getPreparedMsg())
		
	def onMessagePacket(self, msg):
		creature = msg.getString()
		type = msg.getByte()
		if type == self.speakClasses['SPEAK_CHANNEL_Y'] or type == self.speakClasses['SPEAK_CHANNEL_R1'] or type == self.speakClasses['SPEAK_CHANNEL_R2']:
			print 'Channel:', '%x' % msg.getU16(), 'Msg:', msg.getString()
		else:
			msg.getPosition()
			print creature, 'say:', msg.getString()