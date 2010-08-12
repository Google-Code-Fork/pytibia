from struct import pack, unpack
from pyTibia.Classes import *


class NetMsg(object):
	u"Class for handle netmsg"
		
	_msg = ''
	_readPos = 0
		
	def __init__(self, msg = ''):
		self._msg = msg
		if len(msg)>0:
			self._msgLen = self.getU16()
		
	#Add data
		
	def addByte(self, num):
		self._msg += chr(num)
		self._readPos += 1
		
	def addU16(self, num):
		self._msg += pack('<H',num)
		self._readPos += 2
		
	def addU32(self,num):
		self._msg += pack('<I', num)	
		self._readPos += 4
				
	def addString(self, str):
		strLen = len(str)
		self.addU16(strLen)
		self._msg += str
		self._readPos += strLen
		
	def addPosition(self, pos):
		self.addU16(pos.x)
		self.addU16(pos.y)
		self.addByte(pos.z)
		
	#Get data
	
	def getByte(self):
		self._readPos += 1
		return ord(self._msg[self._readPos-1])
		
	def getU16(self):
		ret = unpack('<H',self._msg[self._readPos:self._readPos+2])
		self._readPos += 2
		return ret[0]
		
	def getU32(self):
		ret = unpack('<I',self._msg[self._readPos:self._readPos+4])
		self._readPos += 4
		return ret[0]
		
	def getString(self):
		strLen = self.getU16()
		ret = self._msg[self._readPos:self._readPos+strLen]
		self._readPos += strLen
		return ret

	def getPosition(self):
		return Position(x = self.getU16(), 
			y = self.getU16(), z = self.getByte())
		
		
	#Other
	
	def skipBytes(self, count):
		self._readPos += count
		
	def getPreparedMsg(self):
		retLen = len(self._msg);
		ret = pack('<H', retLen) + self._msg
		return ret
		
	def reset(self):
		self._msg = ''
		self._readPos = 0