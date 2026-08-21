import melee
from Modules.utilitaire import ModuleUtilitaire
from classes.input import Input, TypeInput, Coordonnées
from classes.personnage import Personnage

class ModuleRecovery():
	""" Module pour gérer le retour sur le stage après s'être fait éjecté. """

	def __init__(self, controller: melee.Controller):
		self.controller = controller
		self.personnage = Personnage(controller)

	def doit_recover(self, gamestate: melee.GameState):
		return gamestate.players[self.controller.port].off_stage

	def recover(self, gamestate: melee.GameState) -> list[Input]:
		# TODO Implémenter des options aux ledges (roll, jump, ledgedash)
		positionJoueur = gamestate.players[self.controller.port].position
		estCotéGauche = positionJoueur.x < 0
		positionRebord = melee.stages.EDGE_POSITION[gamestate.stage]

		séquence_input: list[Input] = []

		if(estCotéGauche):
			positionRebord -= positionRebord * 2 # Position du bord gauche est la même que le bord droit en négatif.

		# Si on peut attraper le rebord, ne fait rien.
		# TODO vérifié qu'on peut bien grab le rebord (est au dessus, est entrain de tomber)
		if(estCotéGauche and positionJoueur.x + gamestate.players[self.controller.port].ecb_right[0] >= positionRebord and gamestate.players[self.controller.port].facing):
			return séquence_input
		if(positionJoueur.x - gamestate.players[self.controller.port].ecb_left[0] <= positionRebord and not gamestate.players[self.controller.port].facing):
			return séquence_input

		distanceRebord = abs(positionRebord - positionJoueur.x)
		if(gamestate.players[self.controller.port].jumps_left > 0 and distanceRebord < 15 and ModuleUtilitaire.peut_agir(gamestate.players[self.controller.port])):
			séquence_input.append(Input(melee.enums.Button.BUTTON_Y, Coordonnées(int(estCotéGauche) or int(estCotéGauche), 0.5), TypeInput.APPUYER))
			séquence_input.append(Input(melee.enums.Button.BUTTON_Y, Coordonnées(int(estCotéGauche) or int(estCotéGauche), 0.5), TypeInput.RELACHER))

		# TODO Permettre de maintenir le side-b
		elif(distanceRebord > 20 and ModuleUtilitaire.peut_agir(gamestate.players[self.controller.port])):
			input = self.personnage.coups[melee.enums.Action.SWORD_DANCE_1_AIR]
			séquence_input.append(Input(input.bouton, Coordonnées(input.stick_input.x or int(estCotéGauche), 0.5), TypeInput.APPUYER))
			séquence_input.append(Input(input.bouton, Coordonnées(input.stick_input.x or int(estCotéGauche), 0.5), TypeInput.RELACHER))

		# TODO  Améliorer l'intelligence des up-b (souvent pas de retour ou choisi side-b à la place.)
		elif(distanceRebord < 5 and ModuleUtilitaire.peut_agir(gamestate.players[self.controller.port])):
			input = self.personnage.coups[melee.enums.Action.UP_B_GROUND]
			séquence_input.append(Input(input.bouton, Coordonnées(input.stick_input.x, input.stick_input.y), TypeInput.APPUYER))
			séquence_input.append(Input(input.bouton, Coordonnées(input.stick_input.x, input.stick_input.y), TypeInput.RELACHER))
			séquence_input.append( Input(melee.enums.Button.BUTTON_MAIN, Coordonnées(int(estCotéGauche), 0.5), TypeInput.APPUYER))
		else:
			self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(estCotéGauche), 0.5) # drift vers le stage.
		return séquence_input
