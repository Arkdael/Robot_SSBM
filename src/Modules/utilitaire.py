import melee
from classes.personnage import Personnage

class ModuleUtilitaire():
	def peut_agir(player_state: melee.PlayerState):
		if(melee.enums.Action.STANDING.value <= player_state.action.value <= melee.enums.Action.FALLING_AERIAL_BACKWARD.value):
			return True
		return False
