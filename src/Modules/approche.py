import melee

from Modules.utilitaire import ModuleUtilitaire
from classes.input import Input, TypeInput, Coordonnées

class ModuleApproche:
	def __init__(self, controller: melee.Controller):
		self.controller = controller

	def doit_approcher(self, gamestate: melee.GameState, opposant: melee.PlayerState):
		if(gamestate.players[self.controller.port].off_stage or opposant.off_stage):
			return False
		return True

	def approcher(self, gamestate: melee.GameState, opposant: melee.PlayerState):
		# TODO Permettre de wavedash
		séquence_input: list[input] = []
		# Simplement suivre l'opposant.
		onleft = gamestate.players[self.controller.port].position.x < opposant.position.x
		self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(onleft), 0.5)
		#séquence_input.insert(0, Input(melee.enums.Button.BUTTON_MAIN, Coordonnées(int(onleft), 0.5), TypeInput.APPUYER))

		# Sauter au besoin
		if(gamestate.players[self.controller.port].position.y <= opposant.position.y and abs(gamestate.players[self.controller.port].position.y - opposant.position.y) > 20):
			if(gamestate.players[self.controller.port].jumps_left > 0 and ModuleUtilitaire.peut_agir(gamestate.players[self.controller.port])):
				séquence_input.append(Input(melee.enums.Button.BUTTON_Y, Coordonnées(int(onleft), 0.5), TypeInput.APPUYER))
				séquence_input.append(Input(melee.enums.Button.BUTTON_Y, Coordonnées(int(onleft), 0.5), TypeInput.RELACHER))
		return séquence_input
