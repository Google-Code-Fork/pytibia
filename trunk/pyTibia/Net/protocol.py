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
		'SPEAK_PRIVATE'     :0x04,
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
			0x69:self.parseTileUpdated,
			#0x6d:self.parseThingMove, # ?
			0x6B:self.parseCreatureTurn,
			0xA3:self.parseCancelAttacking,
			0x8F:self.parseChangeSpeed,
			0xB5:self.parseCancelWalk,
			0x0A:self.parseThingAppear,
			0x96:self.parseTextWindow,
			0xD3:self.parseVIPLogin,
			0xD4:self.parseVIPLogout,
			0xD2:self.parseVIP,
			0xB4:self.parseTextMessage,
			0x84:self.parseAnimatedText,
			0x83:self.parseMagicEffect,
			0x85:self.parseDistanceShoot,
			0xA0:self.parseUpdateStats,
			0xA1:self.parseUpdateSkills,
			0x8C:self.parseAddCreatureHealth,
			0x6C:self.parseRemoveThing,
			0x70:self.parseAddItemCparsetainter,
			0x71:self.parseTransformItemCparsetainer,
			0x72:self.parseRemoveItemCparsetainter,
			0x82:self.parseWorldLightLevel,
			0x8D:self.parsePlayerLightLevel,
			0x97:self.parseHouseWindow,
			0x90:self.parseSkull,
			0x91:self.parsePartyIcparse,
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
			
	def parseTileUpdated(self,msg):
		pass
		
	def parseCreatureTurn(self,msg):
		pass
		
	def parseCancelAttacking(self,msg):
		pass
		
	def parseChangeSpeed(self,msg):
		pass
		
	def parseCancelWalk(self,msg):
		pass
		
	def parseThingAppear(self,msg):
		pass
		
	def parseTextWindow(self,msg):
		pass
		
	def parseVIPLogin(self,msg):
		pass
		
	def parseVIPLogout(self,msg):
		pass
		
	def parseVIP(self,msg):
		pass
		
	def parseTextMessage(self,msg):
		pass
		
	def parseAnimatedText(self,msg):
		pass
		
	def parseMagicEffect(self,msg):
		pass

	def parseDistanceShoot(self,msg):
		pass

	def parseUpdateStats(self,msg):
		pass

	def parseUpdateSkills(self,msg):
		pass

	def parseAddCreatureHealth(self,msg):
		pass

	def parseRemoveThing(self,msg):
		pass

	def parseAddItemCparsetainter(self,msg):
		pass

	def parseTransformItemCparsetainer(self,msg):
		pass

	def parseRemoveItemCparsetainter(self,msg):
		pass

	def parseWorldLightLevel(self,msg):
		pass

	def parsePlayerLightLevel(self,msg):
		pass

	def parseHouseWindow(self,msg):
		pass

	def parseSkull(self,msg):
		pass

	def parsePartyIcparse(self,msg):
		pass

			
			
			
			
			
			
	#for user events
	def onTileUpdated(self,msg):
		pass
		
	def onCreatureTurn(self,msg):
		pass
		
	def onCancelAttacking(self,msg):
		pass
		
	def onChangeSpeed(self,msg):
		pass
		
	def onCancelWalk(self,msg):
		pass
		
	def onThingAppear(self,msg):
		pass
		
	def onTextWindow(self,msg):
		pass
		
	def onVIPLogin(self,msg):
		pass
		
	def onVIPLogout(self,msg):
		pass
		
	def onVIP(self,msg):
		pass
		
	def onTextMessage(self,msg):
		pass
		
	def onAnimatedText(self,msg):
		pass
		
	def onMagicEffect(self,msg):
		pass

	def onDistanceShoot(self,msg):
		pass

	def onUpdateStats(self,msg):
		pass

	def onUpdateSkills(self,msg):
		pass

	def onAddCreatureHealth(self,msg):
		pass

	def onRemoveThing(self,msg):
		pass

	def onAddItemContainter(self,msg):
		pass

	def onTransformItemContainer(self,msg):
		pass

	def onRemoveItemContainter(self,msg):
		pass

	def onWorldLightLevel(self,msg):
		pass

	def onPlayerLightLevel(self,msg):
		pass

	def onHouseWindow(self,msg):
		pass

	def onSkull(self,msg):
		pass

	def onPartyIcon(self,msg):
		pass

