from struct import pack, unpack

class NetMsg(object):
	u"Class for handle netmsg"
		
	_msg = ''
	_readPos = 0
		
	def __init__(self, msg = ''):
		self._msg = msg
		
	def reset():
		self._msg = ''
		self._readPos = 0
		
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
		
	def _addMessageLength(self):
		retLen = len(self._msg);
		self.addU16(retLen)
		self._msg += self._msg
		self._readPos += retLen
		
	def addString(self, str):
		strLen = len(str)
		self.addU16(strLen)
		self._msg += str
		self._readPos += strLen
		
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

















