import melee
from classes.personnage import Personnage

class ModuleAttaque:

	def __init__(self, controller):
		self.controller = controller
		self.personnage = Personnage(controller)
		
	def doit_attaquer(self, gamestate: melee.GameState, port_opposant: int):
		for coup in self.personnage.coups:
			if(self.personnage.in_range(gamestate.players[self.controller.port], gamestate.players[port_opposant], gamestate.stage, coup)):
				return True
			else:
				continue

	def attaquer(self, gamestate: melee.GameState, port_opposant: int):
		# Essaye chaque coup, prend le premier que devrais toucher.
		for coup in self.personnage.coups:
			if(self.personnage.in_range(gamestate.players[self.controller.port], gamestate.players[port_opposant], gamestate.stage, coup)):
				onleft = gamestate.players[self.controller.port].position.x < gamestate.players[port_opposant].position.x
				self.personnage.effectuer_coup(action=coup, direction=int(onleft))
				return
