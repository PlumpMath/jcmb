
import util
from pandac.PandaModules import *
from panda3d.bullet import *
from Things import *

class DynamicProp(Thing):

  @classmethod
  def DynamicPropFactory(node):
    name       = node.getTag("name")
    str_flags  = node.getTag("flags")
    str_mass   = node.getTag("mass")
    str_fric   = node.getTag("fric")
    str_shape  = node.getTag("bullet_shape")
    str_model  = node.getTag("model")

    model_file = str_model if str_model else None
    mass = float(str_mass) if str_mass else 1.0
    fric = float(str_fric) if str_fric else 1.0
    flags = str_flags.split(",")

    # Decide on the collision geometry
    if str_shape == "sphere":
      r = node.getBounds().getRadius()
      shape = BulletSphereShape(r)
    elif str_shape == "box":
      pmin, pmax = node.getTightBounds()
      shape = BulletBoxShape(pmax-pmin)

    trans = node.getTransform()
      
    # Make the shiz
    return DynamicProp(name, trans, shape, mass, fric, flags, model_file)

  def __init__(self, name, transform, bullet_shape, mass, fric, set_flags, model_file=None):
    self.name = name
    self.trans = transform

    shape = bullet_shape
    bnode = BulletRigidBodyNode(name)
    bnode.setMass(mass)
    bnode.setFriction(fric)
    bnode.addShape(shape, self.trans)
    bnode.setAngularDamping(0.0) #?    

    np = NodePath(bnode)
    np.setPos(self.trans.getPos())

    print "BALLS POS:", np.getPos()
    
    if model_file:
      self.model = loader.loadModel(model_file)
      self.model.reparentTo(np)

    self.nodepath = np
    self.collision_node = bnode

    self.flags = set_flags

class NewPlayferBox(DynamicProp):
  def __init__(self, pos):
    DynamicProp.__init__(self, 'Playfer Box', TransformState.makePos(pos), BulletBoxShape(Vec3(0.25,0.25,0.25)), 110.0, 1.0, ['grab'], '../data/mod/playferbox.egg')

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
    print "BALLS POS:", np.getPos()

    playferboxmodel = loader.loadModel('../data/mod/playferbox.egg')
    playferboxmodel.reparentTo(np)

    self.nodepath = np
    self.collision_node = bulletnode

  # The playfer box can be grabbed
  def is_grabbable(self):
    return True
