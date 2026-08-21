import melee
from Modules.utilitaire import ModuleUtilitaire
from classes.coup import Coordonnées
from classes.input import Input, TypeInput
from classes.personnage import Personnage

class ModuleAttaque():
	def __init__(self, controller: melee.Controller):
		self.controller = controller
		self.personnage = Personnage(controller)
		
	def doit_attaquer(self, gamestate: melee.GameState, opposant: melee.PlayerState):
		if(self.peut_attaquer(gamestate.players[self.controller.port]) is not True):
			return False
		
		for coup in self.personnage.coups:
			if(self.personnage.in_range(gamestate.players[self.controller.port], opposant, gamestate.stage, coup)):
				return True
			

	def peut_attaquer(self, player_state: melee.PlayerState):
		return ModuleUtilitaire.peut_agir(player_state)

	def choisir_attaque(self, gamestate: melee.GameState, opposant: melee.PlayerState) -> list[Input]:
		séquence_input: list[Input] = []
		print("attacking)")
		# Essaye chaque coup, prend le premier que devrais toucher.
		for coup in self.personnage.coups:
			if(self.personnage.in_range(gamestate.players[self.controller.port], opposant, gamestate.stage, coup)):
				onleft = gamestate.players[self.controller.port].position.x < opposant.position.x
				input = self.personnage.coups[coup]
				séquence_input.append(Input(input.bouton, Coordonnées(input.stick_input.x or int(onleft), input.stick_input.y), TypeInput.APPUYER))
				séquence_input.append(Input(input.bouton, Coordonnées(input.stick_input.x or int(onleft), input.stick_input.y), TypeInput.RELACHER))
				return séquence_input
		return séquence_input
