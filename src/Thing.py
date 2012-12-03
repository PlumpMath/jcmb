import util
from pandac.PandaModules import *
from panda3d.bullet import *

class Thing:

	name = 'Unnamed'
	nodepath = None
	collision_node = None

	def get_name(self):
		return self.name

	def get_nodepath(self):
		return self.nodepath

	def get_collision_node(self):
		return self.collision_node

	def is_grabbable(self):
		raise NotImplementedError("This method has not been implemented and it damn well should have.")

	def on_grab(self):
		raise NotImplementedError("This method has not been implemented and it damn well should have.")

	def on_drop(self):
		raise NotImplementedError("This method has not been implemented and it damn well should have.")

