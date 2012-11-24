"""
Classes and methods for setting up a map.

"""

import util
from pandac.PandaModules import *
from panda3d.bullet import *

class Map:

  def __init__(self, loader, map_path, blt_world):
    self.np = loader.loadModel(util.gDirs["map"]+map_path)
    self.bw = blt_world
    self.init_walls()
    self.init_props()
    self.init_lights()
    self.init_player_spawn()

  def init_walls():
    """Attach Bullet collision geometry to every wall object."""

    self.wall_rigid_node = BulletRigidBodyNode('Walls')
    wall_npc = self.np.findAllMatches("**/=class=wall")
    for wall_np in wall_npc:
      wall_node = wall_np.node()
      # Get the bounding box maximum and minimum points
      pmin, pmax = wall_node.getTightBounds()
      size = pmax-pmin
      # Generate a BulletBoxShape and attach to the Walls rigid body node
      blt_box = BulletBoxShape(size)
      self.wall_rigid_node.addShape(blt_box)
    # Add our walls to the bullet world
    self.bw.attachRigidBody(self.wall_rigid_node)


  def init_props(self):

    # Make Playfer Box
    shape = BulletBoxShape(Vec3(0.25, 0.25, 0.25))
    node = BulletRigidBodyNode('Playfer Box')
    node.setMass(110.0)
    node.setFriction(1.0)
    node.addShape(shape)
    node.setAngularDamping(0.0)
    np = render.attachNewNode(node)
    np.setPos(-1.4, 1.7, -1.7)
    self.world.attachRigidBody(node)
    playferboxmodel = loader.loadModel('../data/mod/playferbox.egg')
    playferboxmodel.reparentTo(np)

    # Make Pendlepot
    shape = BulletBoxShape(Vec3(0.2, 0.15, 0.1))
    node = BulletRigidBodyNode('Pendlepot')
    node.setMass(5.0)
    node.setFriction(1.0)
    node.addShape(shape)
    node.setAngularDamping(0.0)
    np = render.attachNewNode(node)
    np.setPos(-1.4, 1.7, -1.5)
    self.world.attachRigidBody(node)
    pendlepotmodel = loader.loadModel('../data/mod/pendlepot.egg')
    pendlepotmodel.reparentTo(np)

  def init_lights(self):
    alight = AmbientLight('alight')
    alight.setColor(VBase4(0.05, 0.05, 0.05, 1))
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)

