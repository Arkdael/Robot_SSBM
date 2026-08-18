import melee

class Coordonnées:
	def __init__(self, x: float|None = None, y: float|None = None, z: float|None = None):
		self.x = x
		self.y = y
		self.z = z

class Coup:
	def __init__(self, bouton, stick_input: Coordonnées, action: melee.Action):
		self.bouton = bouton
		self.stick_input = stick_input
		self.action = action