import melee

class ModuleApproche:
	def __init__(self, controller: melee.Controller):
		self.controller = controller

	def doit_approcher(self, gamestate: melee.GameState):
		if(gamestate.players[self.controller.port].off_stage):
			return False
		return True

	def approcher(self, gamestate: melee.GameState, port_opposant: int):
		# Simplement suivre l'opposant.
		onleft = gamestate.players[self.controller.port].position.x < gamestate.players[port_opposant].position.x
		self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(onleft), 0.5)

		# Sauter au besoin
		if(gamestate.players[self.controller.port].position.y <= gamestate.players[port_opposant].position.y and abs(gamestate.players[self.controller.port].position.y - gamestate.players[port_opposant].position.y) > 20):
			if(self.controller.prev is not None):
				if(not self.controller.prev.button[melee.enums.Button.BUTTON_Y]):
					self.controller.press_button(melee.enums.Button.BUTTON_Y)
				else:
					self.controller.release_button(melee.enums.Button.BUTTON_Y)
