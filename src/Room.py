"""
Classes and methods for setting up a Room.
"""

import util
from pandac.PandaModules import *
from panda3d.bullet import *
from Thing import *
from PlayferBox import *

class Room(Thing):

	prop_list = []
	lights_list = []

	# Creates a new Room based on the information in the specified egg file
	def __init__(self, room_egg_fname):

		# Load in the egg file and create this room's nodepath
		room_model = loader.loadModel(room_egg_fname)
		self.nodepath = NodePath(room_model)

		# Extract the Room's properties and apply them to the nodepath
		self.extract_collision_node(room_model)
		self.extract_lights(room_model)
		self.extract_props(room_model)

		self.apply_lights()

	# Extracts the Collidable geometry from the egg model and creates the Bullet collision shape for this Room
	# Obviously you can replace the code in this function to make it read tags and create box walls etc etc
	def extract_collision_node(self, room_model):
		mesh = BulletTriangleMesh()
		for collisionNP in room_model.findAllMatches('**/+CollisionNode'):
			collisionNode = collisionNP.node()
			for collisionPolygon in collisionNode.getSolids():
				tri_points = collisionPolygon.getPoints()
				mesh.addTriangle(tri_points[0],tri_points[1],tri_points[2])
				shape = BulletTriangleMeshShape(mesh, dynamic=False) 

		self.collision_node = BulletRigidBodyNode('stairwell')
		self.collision_node.addShape(shape)

	# Extract the light positions, types and orientations
	def extract_lights(self, room_model):

		# Here I'm just setting some lights, but you should change this to use your system of reading lights from the egg file
		self.lights_list = []

		light1 = AmbientLight('ambientlight')
		light1.setColor(VBase4(0.05, 0.05, 0.05, 1))
		self.lights_list.append(light1)

		light2 = PointLight('pointlight')
		light2.setColor(VBase4(1.0, 0.0, 0.0, 1))
		self.lights_list.append(light2)

	def apply_lights(self):
		# Add and apply all lights to the room's nodepath and all the props
		for light in self.lights_list:
			lightnp = self.nodepath.attachNewNode(light)
			self.nodepath.setLight(lightnp)
			for prop in self.prop_list:
				prop.get_nodepath().setLight(lightnp)

	# Extract the Prop types and positions and create this room's prop list
	def extract_props(self, room_model):

		# Make up some random props for illustration purposes
		playferbox = PlayferBox(Vec3(-1.4, 1.7, -1.7))

		self.prop_list = [playferbox]

		# Make Pendlepot
#		shape = BulletBoxShape(Vec3(0.2, 0.15, 0.1))
#		node = BulletRigidBodyNode('Pendlepot')
#		node.setMass(5.0)
#		node.setFriction(1.0)
#		node.addShape(shape)
#		node.setAngularDamping(0.0)
#		np = render.attachNewNode(node)
#		np.setPos(-1.4, 1.7, -1.5)
#		self.world.attachRigidBody(node)
#		pendlepotmodel = loader.loadModel('../data/mod/pendlepot.egg')
#		pendlepotmodel.reparentTo(np)

	# Creatures cannot grab (lift or pull) a Room
	def is_grabbable(self):
		return False

	def add_all_visibles_and_collidables(self, daddy_node, bullet_world):

		# First add this room's visible and collidable geometry
		self.nodepath.reparentTo(daddy_node)
		bullet_world.attachRigidBody(self.collision_node)

		# Now add all the props
		for prop in self.prop_list:
			prop.get_nodepath().reparentTo(daddy_node)
			bullet_world.attachRigidBody(prop.get_collision_node())

	def remove_all_visibles_and_collidables(self, bullet_world):
		self.nodepath.detachNode()
		bullet_world.remove(self.collision_node)
		for prop in prop_list:
			prop.get_nodepath().detachNode()
			bullet_world.remove(prop.get_collision_node())

