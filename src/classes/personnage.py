import melee
from enum import Enum

from classes.coup import Coup

class Personnage:
	# TODO Devrait utliser mon propre énum de coup plutôt que melee.enums.Action...
	coups: dict = {
		melee.enums.Action.NEUTRAL_ATTACK_1: Coup(melee.enums.Button.BUTTON_A, 0.5, 0.5, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.DASH_ATTACK: Coup(melee.enums.Button.BUTTON_A, 0.5, 0.5, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FTILT_HIGH: Coup(melee.enums.Button.BUTTON_A, 1.0, 0.9, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FTILT_HIGH_MID: Coup(melee.enums.Button.BUTTON_A, 1.0, 0.7, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FTILT_MID: Coup(melee.enums.Button.BUTTON_A, 1.0, 0.5, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FTILT_LOW_MID: Coup(melee.enums.Button.BUTTON_A, 1.0, 0.3, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FTILT_LOW: Coup(melee.enums.Button.BUTTON_A, 1.0, 0.1, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.UPTILT: Coup(melee.enums.Button.BUTTON_A, 0.5, 1.0, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.DOWNTILT: Coup(melee.enums.Button.BUTTON_A, 0.5, 0.3, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FSMASH_HIGH: Coup(melee.enums.Button.BUTTON_C, 1.0, 0.9, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FSMASH_MID_HIGH: Coup(melee.enums.Button.BUTTON_C, 0.5, 0.7, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FSMASH_MID: Coup(melee.enums.Button.BUTTON_C, 1.0, 0.5, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FSMASH_MID_LOW: Coup(melee.enums.Button.BUTTON_C, 1.0, 0.3, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FSMASH_LOW: Coup(melee.enums.Button.BUTTON_C, 1.0, 0.1, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.UPSMASH: Coup(melee.enums.Button.BUTTON_C, 0.5, 1.0, [melee.Position(0, 0), melee.Position(5, 25)]),
		melee.enums.Action.DOWNSMASH: Coup(melee.enums.Button.BUTTON_C, 0.5, 0.0, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.NAIR: Coup(melee.enums.Button.BUTTON_A, 0.5, 0.5, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.FAIR: Coup(melee.enums.Button.BUTTON_C, 1.0, 0.5, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.BAIR: Coup(melee.enums.Button.BUTTON_C, 0.0, 0.5, [melee.Position(-5, 5), melee.Position(5, 5)]),
		melee.enums.Action.UAIR: Coup(melee.enums.Button.BUTTON_C, 0.5, 1.0, [melee.Position(0, 0), melee.Position(5, 25)]),
		melee.enums.Action.DAIR: Coup(melee.enums.Button.BUTTON_C, 0.5, 0.0, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.DOWN_B_GROUND: Coup(melee.enums.Button.BUTTON_B, 0.5, 0.0, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.UP_B_GROUND: Coup(melee.enums.Button.BUTTON_B, 0.5, 1.0, [melee.Position(0, 0), melee.Position(5, 10)]),
		melee.enums.Action.NEUTRAL_B_ATTACKING: Coup(melee.enums.Button.BUTTON_B, 0.5, 0.5, [melee.Position(20, 0), melee.Position(40, 10)])
	}

	def __init__(self, controller):
		self.controller = controller

	def effectuer_coup(self, coup: Coup):
		#TODO faire en sorte qu'on puisse spécifier pendant combien de frame maintenir le bouton avant de relacher.

		# Si le bouton est un stick, on l'incline plutôt que d'appuyer.
		if(coup.bouton in [melee.enums.Button.BUTTON_MAIN, melee.enums.Button.BUTTON_C]):
			if(round(self.controller.prev.c_stick[0], 2) != 0.5 or round(self.controller.prev.c_stick[1], 2) != 0.5):
				self.controller.tilt_analog(melee.enums.Button.BUTTON_C, 0.5, 0.5)
				self.controller.release_button(melee.enums.Button.BUTTON_C)
			else:
				self.controller.tilt_analog(melee.enums.Button.BUTTON_C, coup.stick_x, coup.stick_y)
		else:
			if(not self.controller.prev.button[coup.bouton]):
				self.controller.simple_press(coup.stick_x, coup.stick_y, coup.bouton)
			else:
				self.controller.release_button(coup.bouton)