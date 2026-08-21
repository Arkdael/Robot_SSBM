import melee

from classes.input import Coordonnées

class Coup:
	def __init__(self, bouton: melee.enums.Button, stick_input: Coordonnées, action: melee.Action):
		self.bouton = bouton
		self.stick_input = stick_input
		self.action = action
