import melee
from classes.personnage import Personnage

class ModuleAttaque:
	def __init__(self, controller: melee.Controller):
		self.controller = controller
		self.personnage = Personnage(controller)
		
	def doit_attaquer(self, gamestate: melee.GameState, opposant: melee.PlayerState):
		for coup in self.personnage.coups:
			if(self.personnage.in_range(gamestate.players[self.controller.port], opposant, gamestate.stage, coup)):
				return True
			else:
				continue

	def attaquer(self, gamestate: melee.GameState, opposant: melee.PlayerState):
		# Essaye chaque coup, prend le premier que devrais toucher.
		for coup in self.personnage.coups:
			if(self.personnage.in_range(gamestate.players[self.controller.port], opposant, gamestate.stage, coup)):
				onleft = gamestate.players[self.controller.port].position.x < opposant.position.x
				self.personnage.effectuer_coup(action=coup, direction=int(onleft))
				return
