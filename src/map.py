"""
Classes and methods for setting up a map.

"""

import util
from props import *
from pandac.PandaModules import *
from panda3d.bullet import *

class Map:

  def __init__(self, loader, map_path, blt_world):
    self.np = loader.loadModel(util.dirs["map"]+map_path)
    self.bw = blt_world
    self.init_walls()
    self.init_props()
    self.init_lights()
    self.init_player_spawn()

  def init_walls():
    """Attach Bullet collision geometry to every wall object."""

    self.wall_rigid_node = BulletRigidBodyNode('Walls')
    wall_npc = self.np.findAllMatches("**/=class=wall")
    for wall_np in wall_npc.asList():
      wall_node = wall_np.node()
      wall_trans = wall_node.getTransform()
      # Get the bounding box maximum and minimum points
      pmin, pmax = wall_node.getTightBounds()
      size = pmax-pmin
      # Generate a BulletBoxShape and attach to the Walls rigid body node
      blt_box = BulletBoxShape(size)
      self.wall_rigid_node.addShape(blt_box, wall_trans)
    # Add our walls to the bullet world
    self.bw.attachRigidBody(self.wall_rigid_node)


  def init_props():
    """Initialise all props in the map."""
    
    self.props = []
    prop_npc = self.np.findAllMatches("**/=class=prop*")
    for prop_np in prop_npc.asList():
      self.props.append(
      
