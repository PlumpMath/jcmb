
import util
from pandac.PandaModules import *
from panda3d.bullet import *
from Things import *

class PropFactory:
  def __init__(self, pos):
    pass

class PlayferBox(Thing):

	# Creates a new PlayferBox at the specified position
	def __init__(self, pos):

		shape = BulletBoxShape(Vec3(0.25, 0.25, 0.25))
		bulletnode = BulletRigidBodyNode('Playfer Box')
		bulletnode.setMass(110.0)
		bulletnode.setFriction(1.0)
		bulletnode.addShape(shape)
		bulletnode.setAngularDamping(0.0)

		np = NodePath(bulletnode)
		np.setPos(pos)

		playferboxmodel = loader.loadModel('../data/mod/playferbox.egg')
		playferboxmodel.reparentTo(np)

		self.nodepath = np
		self.collision_node = bulletnode

	# The playfer box can be grabbed
	def is_grabbable(self):
		return True
