from enum import Enum

import melee

class Coup:
	def __init__(self, bouton, stick_x, stick_y, hitbox: tuple[melee.Position, melee.Position]):
		self.bouton = bouton
		self.stick_x = stick_x
		self.stick_y = stick_y
		self.hitbox = hitbox

	# Fonction qui détermine si une cible est à portée du coup (hitbox par de la position de l'attaquant.)
	def est_à_portée(self, position_attaquant: melee.Position, position_cible: melee.Position):
		est_à_portée_x = position_cible.x <= position_attaquant.x + self.hitbox[1].x and position_cible.x >= position_attaquant.x + self.hitbox[0].x
		est_à_portée_y = position_cible.y <= position_attaquant.y + self.hitbox[1].y and position_cible.y >= position_attaquant.y + self.hitbox[0].y
		if(est_à_portée_x and est_à_portée_y):
			return True
		else:
			return False