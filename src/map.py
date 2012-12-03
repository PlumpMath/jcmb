"""
Classes and methods for setting up a map.

"""

import util
import props
from pandac.PandaModules import *
from panda3d.bullet import *

class Map:

  def __init__(self, loader, map_path, blt_world):
    self.np = loader.loadModel(util.dirs["map"]+map_path)
    self.bw = blt_world
    self.init_walls()
    self.init_props()         # self.props
    self.init_lights()        # self.lights
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
      prop_node = prop_np.node()
      ptype = prop_node.getTag("class")
      # Create a prop object by looking up the type map (this should be nicer
      #  than a massive if/elif block.)
      #  But note this might cause the very gods themselves to rain pain and 
      #  suffering down upon our tormented souls for millenia to come.
      # Pass the node path as well so it can position itself/sort out bullet
      #  collision stuff.
      self.props.append(getattr(props, props.types[ptype])(prop_np))
      
  def init_lights():
    """
    Initialise all the dynamic lighting. Defining which (static) props
    get lit by dynamic lighting should happen here as well.
    """

    self.lights = []
