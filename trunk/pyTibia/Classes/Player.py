from pyTibia.Classes.Creature import Creature

class Player(creature):

	name = ''
	lvl = 1
	exp = 0
	mlv = 0
	skills = [10,10,10,10,10,10,10,]
	skillsProc = [0,0,0,0,0,0,0,]
	
	def __init__(self):
		pass