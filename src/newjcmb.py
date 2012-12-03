import sys
import math
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from panda3d.bullet import *
from direct.gui import *
from Room import *
from Player import *

class EscapeFromJCMB(object,DirectObject):

	def __init__(self):
		self.init_window()
		self.init_bullet_world()
		self.load_game_world()
		self.load_player()
		self.start_physics()
	
	def init_window(self):
		# Hide the mouse cursor and set a title
		props = WindowProperties()
		props.setCursorHidden(True)
		props.setTitle('EscapeFromJCMB')
		base.win.requestProperties(props)
	
		# Allow us to exit the game at any time with Esc
		self.accept('escape', sys.exit)
	
	def init_bullet_world(self):
		self.bullet_world = BulletWorld()
		self.bullet_world.setGravity(Vec3(0, 0, -9.81))		

	def load_game_world(self):
		stairwell = Room('../data/mod/jcmbstairs.egg')
		stairwell.add_all_visibles_and_collidables(render, self.bullet_world)

	def load_player(self):
		self.player = Player(base.camera, base.camLens, self.bullet_world, render, taskMgr)
#		self.player.add_all_visibles_and_collidables(render, self.bullet_world)

	def update_physics(self, task):
		dt = globalClock.getDt()
		self.bullet_world.doPhysics(dt)
		return task.cont

	def start_physics(self):
		taskMgr.add(self.update_physics, 'update_physics')


# Get this show on the road
base.setFrameRateMeter(True)
EscapeFromJCMB()
render.setShaderAuto()
run()
