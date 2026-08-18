import melee

from classes.personnage import Personnage

class ModuleRecovery:

	def __init__(self, controller):
		self.controller = controller
		self.personnage = Personnage(controller)

	def doit_recover(self, gamestate: melee.GameState):
		return gamestate.players[self.controller.port].off_stage

	def recover(self, gamestate: melee.GameState):
		positionJoueur = gamestate.players[self.controller.port].position
		estCotéGauche = positionJoueur.x < 0
		positionRebord = melee.stages.EDGE_POSITION[gamestate.stage]
		if(estCotéGauche):
			positionRebord -= positionRebord * 2

		distanceRebord = abs(positionRebord - positionJoueur.x)
		if(gamestate.players[self.controller.port].jumps_left > 0 and distanceRebord < 15):
			if(self.controller.prev is not None):
				if(not self.controller.prev.button[melee.enums.Button.BUTTON_Y]):
					self.controller.press_button(melee.enums.Button.BUTTON_Y)
					return
				else:
					self.controller.release_button(melee.enums.Button.BUTTON_Y)
					return
		if(distanceRebord > 20):
			self.personnage.effectuer_coup(melee.enums.Action.SWORD_DANCE_1_AIR, int(estCotéGauche)) #Side-B si trop loin du stage
			return
		if(distanceRebord < 5):
			self.personnage.effectuer_coup(melee.enums.Action.UP_B_GROUND) #up-b quand assez proche
			return
		self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(estCotéGauche), 0.5)



		
