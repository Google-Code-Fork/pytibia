from socket import socket

class ProtocolBase(object):
	_address = ''
	_accId = 0
	_password = ''
	_playerName = ''
		
	
class Protocol76(ProtocolBase):
	def __init__(self, address = 'localhost', acc = 111111, pswd = 'tibia', name = 'Yurez'):
		self._address = address
		self._accId = acc
		self._password = pswd
		self._playerName = name
