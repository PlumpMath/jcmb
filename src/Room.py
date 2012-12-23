"""
Classes and methods for setting up a Room.
"""

import util
from pandac.PandaModules import *
from panda3d.bullet import *
from Things import *
from Props import *

class Room(Thing):

  props = []
  lights = []

  # Creates a new Room based on the information in the specified egg file
  def __init__(self, room_egg_fname):

    # Load in the egg file and create this room's nodepath
    self.model = loader.loadModel(room_egg_fname)
    self.nodepath = NodePath(self.model)

    # Extract the Room's properties and apply them to the nodepath
    self.extract_collision_poly()
    self.extract_walls()
    self.extract_lights()
    self.extract_props()

    self.apply_lights()

  # Extracts the Collidable geometry from the egg model and creates the Bullet collision shape for this Room
  # Obviously you can replace the code in this function to make it read tags and create box walls etc etc
  def extract_collision_poly(self):
    mesh = BulletTriangleMesh()
    for collisionNP in self.model.findAllMatches('**/+CollisionNode'):
      collisionNode = collisionNP.node()
      for collisionPolygon in collisionNode.getSolids():
        tri_points = collisionPolygon.getPoints()
        mesh.addTriangle(tri_points[0],tri_points[1],tri_points[2])
        shape = BulletTriangleMeshShape(mesh, dynamic=False) 

    self.collision_node = BulletRigidBodyNode('stairwell')
    self.collision_node.addShape(shape)

  # Extract all the wall geometry and convert it to collision boxes
  def extract_walls(self):
    self.wall_rigid_node = BulletRigidBodyNode('walls')
    wall_npc = self.nodepath.findAllMatches("**/=class=wall")
    for wall_np in wall_npc:
      wall_node = wall_np.node()
      wall_trans = wall_node.getTransform()
      # Get the bounding box maximum and minimum points
      pmin, pmax = wall_node.getTightBounds()
      size = pmax-pmin
      # Generate a BulletBoxShape and attach to the Walls rigid body node
      blt_box = BulletBoxShape(size)
      self.wall_rigid_node.addShape(blt_box, wall_trans)

  # Extract the light positions, types and orientations
  def extract_lights(self):

    # Here I'm just setting some lights, but you should change this to use your system of reading lights from the egg file
    self.lights = []

    light1 = AmbientLight('ambientlight')
    light1.setColor(VBase4(0.05, 0.05, 0.05, 1))
    self.lights.append(light1)

    light2 = PointLight('pointlight')
    light2.setColor(VBase4(1.0, 0.0, 0.0, 1))
    self.lights.append(light2)

  def apply_lights(self):
    # Add and apply all lights to the room's nodepath and all the props
    for light in self.lights:
      lightnp = self.nodepath.attachNewNode(light)
      self.nodepath.setLight(lightnp)
      for prop in self.props:
        prop.get_nodepath().setLight(lightnp)

  # Extract the Prop types and positions and create this room's prop list
  def extract_props(self):
    self.props = []
    self.prop_rigid_node = BulletRigidBodyNode('static_props')
    prop_npc = self.nodepath.findAllMatches("**/=class=prop")
    for prop_np in prop_npc:
      prop_node = prop_np.node()
      ptype = prop_node.getTag("type")
      # Static props get added to the rigid body node
      if ptype == "static":
        pmin, pmax = prop_node.getTightBounds()
        size = pmax-pmin
        self.prop_rigid_node.addShape(BulletBoxShape(size), prop_node.getTransform())
      # Actual props get added to the list via a factory
      else:
        self.props.append(PropFactory(ptype))
    # Make up some random props for illustration purposes
#    self.props.append(PlayferBox(Vec3(-1.4, 1.7, -1.7)))


    self.props.append(NewPlayferBox(Vec3(-0.25, 1.44, -1)))
#    self.props.append(NewPlayferBox(Vec3(0, 0, 0)))

    # Make Pendlepot
#   shape = BulletBoxShape(Vec3(0.2, 0.15, 0.1))
#   node = BulletRigidBodyNode('Pendlepot')
#   node.setMass(5.0)
#   node.setFriction(1.0)
#   node.addShape(shape)
#   node.setAngularDamping(0.0)
#   np = render.attachNewNode(node)
#   np.setPos(-1.4, 1.7, -1.5)
#   self.world.attachRigidBody(node)
#   pendlepotmodel = loader.loadModel('../data/mod/pendlepot.egg')
#   pendlepotmodel.reparentTo(np)

  # Creatures cannot grab (lift or pull) a Room
  def is_grabbable(self):
    return False

  def add_all_visibles_and_collidables(self, daddy_node, bullet_world):

    # First add this room's visible and collidable geometry
    self.nodepath.reparentTo(daddy_node)
    bullet_world.attachRigidBody(self.collision_node)
    # Add our walls to the bullet world
    bullet_world.attachRigidBody(self.wall_rigid_node)

    # Now add all the props
    for prop in self.props:
      print prop.name
      prop.get_nodepath().reparentTo(daddy_node)
      bullet_world.attachRigidBody(prop.get_collision_node())

  def remove_all_visibles_and_collidables(self, bullet_world):
    self.nodepath.detachNode()
    bullet_world.remove(self.collision_node)
    for prop in props:
      prop.get_nodepath().detachNode()
      bullet_world.remove(prop.get_collision_node())
