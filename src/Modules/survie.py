import math
import melee
from classes.personnage import Personnage

class ModuleSurvie():
	""" Module pour gérer l'influence directionnel après s'être fait frappé. """

	def __init__(self, controller: melee.Controller):
		self.controller = controller
		self.personnage = Personnage(controller)
		self.frameData = melee.framedata.FrameData()
		
	def doit_survivre(self, gamestate: melee.GameState, opposant: melee.PlayerState):
		if(gamestate.players[self.controller.port].action.value >= melee.enums.Action.DAMAGE_FLY_HIGH.value and gamestate.players[self.controller.port].action.value <= melee.enums.Action.DAMAGE_FLY_ROLL.value):
			return True

	def survivre(self, gamestate: melee.GameState, opposant: melee.PlayerState):
		angle_projection = (math.degrees(-math.atan2(gamestate.players[self.controller.port].speed_x_attack, gamestate.players[self.controller.port].speed_y_attack)) + 90) % 360

		if(self.frameData.project_hit_location(gamestate.players[self.controller.port], gamestate.stage)[0] or 0 > melee.stages.BLASTZONES[gamestate.stage][0]):
			return self.DI_survie(gamestate=gamestate, angle_projection=angle_projection, opposant=opposant)
		else:
			return self.DI_combo(gamestate=gamestate, angle_projection=angle_projection, opposant=opposant)

	def DI_survie(self, gamestate: melee.GameState, angle_projection: float, opposant: melee.PlayerState):
		angle_di = angle_projection
		if 0 <= angle_projection <= 40:
			angle_di = (angle_projection - 90) % 360
		elif 40 < angle_projection <= 90:
			angle_di = (angle_projection + 90) % 360
		elif 90 < angle_projection <= 140:
			angle_di = (angle_projection - 90) % 360
		elif 140 < angle_projection <= 180:
			angle_di = (angle_projection + 90) % 360

		cardinaux = ModuleSurvie.angle_to_cardinal(angle_di)
		self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, cardinaux[0], cardinaux[1])
		return

	def DI_combo(self, gamestate: melee.GameState,  angle_projection: float, opposant: melee.PlayerState):
		onleft = gamestate.players[self.controller.port].position.x < opposant.position.x
		self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(not onleft), 0.5)
		return

	def angle_to_cardinal(angle: float):
		""" For the given angle, return the nearest cardinal (8 directions) direction. """
		if angle <= 22.5 or 337.5 < angle:
			return 1, 0.5
		if 22.5 < angle <= 67.5:
			return 1, 1
		if 67.5 < angle <= 112.5:
			return 0.5, 1
		if 112.5 < angle <= 157.5:
			return 0, 1
		if 157.5 < angle <= 202.5:
			return 0, 0.5
		if 202.5 < angle <= 247.5:
			return 0, 0
		if 247.5 < angle <= 292.5:
			return 0.5, 0
		if 292.5 < angle <= 337.5:
			return 1, 0

		# This shouldn't be possible, but just in case.
		return 1, 1
