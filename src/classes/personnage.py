import math
import melee
from classes.coup import Coup, Coordonnées

class Personnage:
	coups: dict = {
		melee.enums.Action.NEUTRAL_ATTACK_1: Coup(melee.enums.Button.BUTTON_A, Coordonnées(0.5, 0.5), melee.Action.NEUTRAL_ATTACK_1),
		melee.enums.Action.DASH_ATTACK: Coup(melee.enums.Button.BUTTON_A, Coordonnées(0.5, 0.5), melee.Action.DASH_ATTACK),
		melee.enums.Action.FTILT_HIGH: Coup(melee.enums.Button.BUTTON_A, Coordonnées(None, 0.9), melee.Action.FTILT_HIGH),
		melee.enums.Action.FTILT_HIGH_MID: Coup(melee.enums.Button.BUTTON_A, Coordonnées(None, 0.7), melee.Action.FTILT_HIGH_MID),
		melee.enums.Action.FTILT_MID: Coup(melee.enums.Button.BUTTON_A, Coordonnées(None, 0.5), melee.Action.FTILT_MID),
		melee.enums.Action.FTILT_LOW_MID: Coup(melee.enums.Button.BUTTON_A, Coordonnées(None, 0.3), melee.Action.FTILT_LOW_MID),
		melee.enums.Action.FTILT_LOW: Coup(melee.enums.Button.BUTTON_A, Coordonnées(None, 0.1), melee.Action.FTILT_LOW),
		melee.enums.Action.UPTILT: Coup(melee.enums.Button.BUTTON_A, Coordonnées(0.5, 1.0), melee.Action.UPTILT),
		melee.enums.Action.DOWNTILT: Coup(melee.enums.Button.BUTTON_A, Coordonnées(0.5, 0.3), melee.Action.DOWNTILT),
		melee.enums.Action.FSMASH_HIGH: Coup(melee.enums.Button.BUTTON_C, Coordonnées(None, 0.9), melee.Action.FSMASH_HIGH),
		melee.enums.Action.FSMASH_MID_HIGH: Coup(melee.enums.Button.BUTTON_C, Coordonnées(0.5, 0.7), melee.Action.FSMASH_MID_HIGH),
		melee.enums.Action.FSMASH_MID: Coup(melee.enums.Button.BUTTON_C, Coordonnées(None, 0.5), melee.Action.FSMASH_MID),
		melee.enums.Action.FSMASH_MID_LOW: Coup(melee.enums.Button.BUTTON_C, Coordonnées(None, 0.3), melee.Action.FSMASH_MID_LOW),
		melee.enums.Action.FSMASH_LOW: Coup(melee.enums.Button.BUTTON_C, Coordonnées(None, 0.1), melee.Action.FSMASH_LOW),
		melee.enums.Action.UPSMASH: Coup(melee.enums.Button.BUTTON_C, Coordonnées(0.5, 1.0), melee.Action.UPSMASH),
		melee.enums.Action.DOWNSMASH: Coup(melee.enums.Button.BUTTON_C, Coordonnées(0.5, 0.0), melee.Action.DOWNSMASH),
		melee.enums.Action.NAIR: Coup(melee.enums.Button.BUTTON_A, Coordonnées(0.5, 0.5), melee.Action.NAIR),
		melee.enums.Action.FAIR: Coup(melee.enums.Button.BUTTON_C, Coordonnées(1.0, 0.5), melee.Action.FAIR),
		melee.enums.Action.BAIR: Coup(melee.enums.Button.BUTTON_C, Coordonnées(0.0, 0.5), melee.Action.BAIR),
		melee.enums.Action.UAIR: Coup(melee.enums.Button.BUTTON_C, Coordonnées(0.5, 1.0), melee.Action.UAIR),
		melee.enums.Action.DAIR: Coup(melee.enums.Button.BUTTON_C, Coordonnées(0.5, 0.0), melee.Action.DAIR),
		melee.enums.Action.DOWN_B_GROUND: Coup(melee.enums.Button.BUTTON_B, Coordonnées(0.5, 0.0), melee.Action.DOWN_B_GROUND),
		melee.enums.Action.UP_B_GROUND: Coup(melee.enums.Button.BUTTON_B, Coordonnées(0.5, 1.0), melee.Action.UP_B_GROUND),
		melee.enums.Action.NEUTRAL_B_ATTACKING: Coup(melee.enums.Button.BUTTON_B, Coordonnées(0.5, 0.5), melee.Action.NEUTRAL_B_ATTACKING),
		melee.enums.Action.SWORD_DANCE_1_AIR: Coup(melee.enums.Button.BUTTON_B, Coordonnées(None, 0.5), melee.Action.SWORD_DANCE_1_AIR),
	}

	def __init__(self, controller):
		self.controller = controller
		self.frameData = melee.framedata.FrameData()

	def effectuer_coup(self, action: melee.enums.Action, direction: float = 1.0):
		#TODO faire en sorte qu'on puisse spécifier pendant combien de frame maintenir le bouton avant de relacher.
		coup = self.coups[action]
		
		# Si le bouton est un stick, on l'incline plutôt que d'appuyer.
		if(coup.bouton in [melee.enums.Button.BUTTON_MAIN, melee.enums.Button.BUTTON_C]):
			if(round(self.controller.prev.c_stick[0], 2) != 0.5 or round(self.controller.prev.c_stick[1], 2) != 0.5):
				self.controller.tilt_analog(melee.enums.Button.BUTTON_C, 0.5, 0.5)
				self.controller.release_button(melee.enums.Button.BUTTON_C)
			else:
				self.controller.tilt_analog(melee.enums.Button.BUTTON_C, coup.stick_input.x or direction, coup.stick_input.y)
		else:
			if(not self.controller.prev.button[coup.bouton]):
				self.controller.simple_press(coup.stick_input.x or direction, coup.stick_input.y, coup.bouton)
			else:
				self.controller.release_button(coup.bouton)

	def in_range(self, attacker, defender, stage, action: melee.Action):
		"""Calculates if an attack is in range of a given defender

		Args:
				attacker (gamestate.PlayerState): The attacking player
				defender (gamestate.PlayerState): The defending player
				stage (enums.Stage): The stage being played on

		Returns:
				integer with the frame that the specified attack will hit the defender
				0 if it won't hit

		Note:
				This considers the defending character to have a single hurtbox, centered
				at the x,y coordinates of the player (adjusted up a little to be centered)
		"""

		# Adjust the defender's hurtbox up a little, to be more centered.
		#		the game keeps y coordinates based on the bottom of a character, not
		#		their center. So we need to move up by one radius of the character's size
		defender_size = float(self.frameData.characterdata[defender.character]["size"])
		defender_y = defender.position.y + defender_size

		# Running totals of how far the attacker will travel each frame
		attacker_x = attacker.position.x
		attacker_y = attacker.position.y

		attackingframe = self.frameData._getframe(attacker.character, melee.enums.Action(action), self.frameData.first_hitbox_frame(attacker.character, melee.enums.Action(action)))
		if attackingframe is None:
			return False

		if attackingframe['hitbox_1_status'] or attackingframe['hitbox_2_status'] or \
				attackingframe['hitbox_3_status'] or attackingframe['hitbox_4_status']:
			# Calculate the x and y positions of all 4 hitboxes for this frame
			hitbox_1_x = float(attackingframe["hitbox_1_x"])
			hitbox_1_y = float(attackingframe["hitbox_1_y"]) + attacker_y
			hitbox_2_x = float(attackingframe["hitbox_2_x"])
			hitbox_2_y = float(attackingframe["hitbox_2_y"]) + attacker_y
			hitbox_3_x = float(attackingframe["hitbox_3_x"])
			hitbox_3_y = float(attackingframe["hitbox_3_y"]) + attacker_y
			hitbox_4_x = float(attackingframe["hitbox_4_x"])
			hitbox_4_y = float(attackingframe["hitbox_4_y"]) + attacker_y

			# Flip the horizontal hitboxes around if we're facing left
			if not attacker.facing:
				hitbox_1_x *= -1
				hitbox_2_x *= -1
				hitbox_3_x *= -1
				hitbox_4_x *= -1

				hitbox_1_x += attacker_x
				hitbox_2_x += attacker_x
				hitbox_3_x += attacker_x
				hitbox_4_x += attacker_x

				# Now see if any of the hitboxes are in range
				distance1 = math.sqrt((hitbox_1_x - defender.position.x)**2 + (hitbox_1_y - defender_y)**2)
				distance2 = math.sqrt((hitbox_2_x - defender.position.x)**2 + (hitbox_2_y - defender_y)**2)
				distance3 = math.sqrt((hitbox_3_x - defender.position.x)**2 + (hitbox_3_y - defender_y)**2)
				distance4 = math.sqrt((hitbox_4_x - defender.position.x)**2 + (hitbox_4_y - defender_y)**2)

				if distance1 < defender_size + float(attackingframe["hitbox_1_size"]):
					return True
				if distance2 < defender_size + float(attackingframe["hitbox_2_size"]):
					return True
				if distance3 < defender_size + float(attackingframe["hitbox_3_size"]):
					return True
				if distance4 < defender_size + float(attackingframe["hitbox_4_size"]):
					return True
		return False
