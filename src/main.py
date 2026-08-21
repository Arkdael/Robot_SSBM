#!/usr/bin/env python3
import argparse
import signal
import sys
import melee

from typing import NoReturn
from Modules.approche import ModuleApproche
#from Modules.attaque import ModuleAttaque
#from Modules.recovery import ModuleRecovery
#from Modules.survie import ModuleSurvie
from Modules.attaque import ModuleAttaque
from Modules.recovery import ModuleRecovery
from Modules.survie import ModuleSurvie
from classes import personnage
from classes.coup import Coup, Coordonnées
from classes.input import Input, TypeInput
from classes.personnage import Personnage

# This example program demonstrates how to use the Melee API to run a console,
# setup controllers, and send button presses over to a console.
class Robot:
	def __init__(self, debug: bool = False, address: str = "127.0.0.1", dolphin_executable_path: str = "", connect_code: str = "", iso: str = "", ports: list[int] = [1, 2]) -> None:
		self.debug = debug
		self.address = address
		self.dolphin_executable_path = dolphin_executable_path
		self.connect_code = connect_code
		self.iso = iso
		self.ports = ports
		self.pile_exécution: list[Input] = []

		# This logger object is useful for retroactively debugging issues in your bot.
		# You can write things to it each frame, and it will create a CSV file describing the match.
		self.log = None
		if debug:
			self.log = melee.Logger()

		# Create our Console object.
		# 	This will be one of the primary objects that we will interface with.
		# 	The Console represents the virtual or hardware system Melee is playing on.
		# 	Through this object, we can get "GameState" objects per-frame so that your
		# 	bot can actually "see" what's happening in the game.
		self.console = melee.Console(
			path=args.dolphin_executable_path,
			slippi_address=args.address,
			logger=self.log,
			save_replays=args.debug,
			fullscreen=False,
		)

		# Create our Controller object.
		# 	The controller is the second primary object your bot will interact with
		# 	Your controller is your way of sending button presses to the game, whether
		# 	virtual or physical.
		self.controllers = {
			port: melee.Controller(
				console=self.console,
				port=port,
				type=melee.ControllerType.STANDARD)
			for port in self.ports
		}
		signal.signal(signal.SIGINT, self.signal_handler)

	def check_port(value) -> int:
		ivalue = int(value)
		if ivalue < 1 or ivalue > 4:
			raise argparse.ArgumentTypeError("%s is an invalid controller port (Must be between 1 and 4)." % value)
		return ivalue
		
	# This isn't necessary, but makes it so that Dolphin will get killed when you ^C.
	def signal_handler(self, sig, frame) -> NoReturn:
		for controller in self.controllers.values():
			controller.disconnect()
		self.console.stop()
		if self.debug:
			self.log.writelog()
			print("") # because the ^C will be on the terminal.
			print("Log file created: " + self.log.filename)
		print("Shutting down cleanly...")
		sys.exit(0)

	def run(self) -> NoReturn:
		# Run the console.
		self.console.run(iso_path=self.iso)

		# Connect to the console.
		print("Connecting to console...")
		if not self.console.connect():
			print("ERROR: Failed to connect to the console.")
			sys.exit(-1)
		print("Console connected")

		# Plug our controller in.
		# 	Due to how named pipes work, this has to come AFTER running dolphin.
		# 	NOTE: If you're loading a movie file, don't connect the controller,
		# 	dolphin will hang waiting for input and never receive it.
		print("Connecting controller to console...")
		for controller in self.controllers.values():
			if not controller.connect():
				print("ERROR: Failed to connect the controller.")
				sys.exit(-1)
		print("Controller connected")

		self.menu_helper = melee.MenuHelper()

		self.personnage = Personnage(controller=self.controllers.get(self.ports[0]))
		self.moduleApproche = ModuleApproche(controller=self.controllers.get(self.ports[0]))
		self.moduleAttaque = ModuleAttaque(controller=self.controllers.get(self.ports[0]))
		self.moduleRecovery = ModuleRecovery(controller=self.controllers.get(self.ports[0]))
		self.moduleSurvie = ModuleSurvie(controller=self.controllers.get(self.ports[0]))

		# Main loop
		while(True):
			# "step" to the next frame.
			gamestate = self.console.step()
			if gamestate is None:
				continue

			# The console object keeps track of how long your bot is taking to process frames.
			# 	And can warn you if it's taking too long.
			if self.console.processingtime * 1000 > 12:
				print("WARNING: Last frame took " + str(self.console.processingtime*1000) + "ms to process.")
	
			# What menu are we in?
			if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
				self.gérer_frame_jeu(gamestate=gamestate)
			else:
				self.gérer_frame_menu(gamestate=gamestate)

	def gérer_frame_jeu(self, gamestate: melee.GameState) -> None:
		for port, controller in self.controllers.items():
			if(gamestate.players[port].cpu_level <= 0):
				# NOTE: This is where your AI does all of its stuff!
				# This line will get hit once per frame, so here is where you read
				# in the gamestate and decide what buttons to push on the controller.

				# Considère n'importe quel joueur qui ne partage pas son port comme son opposant.
				opposant = gamestate.players[list(filter(lambda key: key is not port, gamestate.players.keys()))[-1]]
				if(self.pile_exécution.__len__() > 0):
					print(self.pile_exécution)
					#self.personnage.effectuer_coup(self.personnage.coups[self.pile_exécution[0][0]], self.pile_exécution[0][1])
					if(self.pile_exécution[0] is not None):
						match self.pile_exécution[0].type:
							case TypeInput.APPUYER:
								self.pile_exécution.pop(0).exécuter_input(controller)
							case TypeInput.RELACHER:
								self.pile_exécution.pop(0).exécuter_input_inverse(controller)
							case _:
								self.pile_exécution.pop(0)
					else:
						self.pile_exécution.pop(0)

				if(self.moduleRecovery.doit_recover(gamestate=gamestate)):
					séquence_input = self.moduleRecovery.recover(gamestate=gamestate)
					for input in séquence_input:
						self.pile_exécution.append(input)

				elif(self.moduleSurvie.doit_survivre(gamestate=gamestate, opposant=opposant)):
					self.moduleSurvie.survivre(gamestate=gamestate, opposant=opposant)

				elif(self.moduleAttaque.doit_attaquer(gamestate=gamestate, opposant=opposant)):
					séquence_input = self.moduleAttaque.choisir_attaque(gamestate=gamestate, opposant=opposant)
					for input in séquence_input:
						self.pile_exécution.append(input)

				elif(self.moduleApproche.doit_approcher(gamestate=gamestate, opposant=opposant)):
					séquence_input = self.moduleApproche.approcher(gamestate=gamestate, opposant=opposant)
					for input in séquence_input:
						self.pile_exécution.append(input)

		# Log this frame's detailed info if we're in game.
		if self.log:
			self.log.logframe(gamestate)
			self.log.writeframe()

	def gérer_frame_menu(self, gamestate: melee.GameState) -> None:
		for port, controller in self.controllers.items():
			self.menu_helper.menu_helper_simple(
				gamestate=gamestate,
				controller=controller,
				character_selected=melee.Character.LUIGI if(port==self.ports[0]) else melee.Character.FOX,
				stage_selected=melee.Stage.RANDOM_STAGE,
				connect_code=self.connect_code,
				cpu_level=0 if(port==self.ports[0]) else 9,
				costume=port,
				autostart=(port==self.ports[0]),
				swag=False)

		# If we're not in game, don't log the frame.
		if self.log:
			self.log.skipframe()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Example of libmelee in action')
	parser.add_argument('--debug', '-d', action='store_true', help='Debug mode. Creates a CSV of all game states')
	parser.add_argument('--address', '-a', default="127.0.0.1", help='IP address of Slippi/Wii')
	parser.add_argument('--dolphin_executable_path', '-e', default='', help='The directory where dolphin is')
	parser.add_argument('--connect_code', '-t', default="", help='Direct connect code to connect to in Slippi Online')
	parser.add_argument('--iso', default='', type=str, help='Path to melee iso.')
	parser.add_argument('--ports', nargs="+", default=[1, 2], type=Robot.check_port, help='Ports the bots will use.')
	args = parser.parse_args()

	robot = Robot(
		debug=args.debug,
		address=args.address,
		dolphin_executable_path=args.dolphin_executable_path,
		connect_code=args.connect_code,
		iso=args.iso,
		ports=args.ports
	)

	robot.run()
