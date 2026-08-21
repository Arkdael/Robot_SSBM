import melee

class TypeInput(melee.Enum):
	APPUYER = 0,
	RELACHER = 1,
	MAINTENIR = 2

class Coordonnées:
	def __init__(self, x: float|None = None, y: float|None = None, z: float|None = None):
		self.x = x
		self.y = y
		self.z = z

class Input:
	def __init__(self, bouton: melee.enums.Button, stick_input: Coordonnées|None, type: TypeInput):
		self.bouton = bouton
		self.stick_input = stick_input
		self.type = type

	def exécuter_input(self, controller: melee.Controller):
		if(self.bouton in [melee.enums.Button.BUTTON_MAIN, melee.enums.Button.BUTTON_C]):
			controller.tilt_analog(melee.enums.Button.BUTTON_C, self.stick_input.x, self.stick_input.y)
		else:
			controller.simple_press(self.stick_input.x, self.stick_input.y, self.bouton)
				
	def exécuter_input_inverse(self, controller: melee.Controller):
		controller.release_button(self.bouton)
		if(self.bouton in [melee.enums.Button.BUTTON_MAIN, melee.enums.Button.BUTTON_C]):
			controller.tilt_analog(melee.enums.Button.BUTTON_C, 0.5, 0.5)
		else:
			controller.release_button(self.bouton)
