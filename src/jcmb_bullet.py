import sys
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import ZUp

class EscapeFromJCMB(object,DirectObject):

  def __init__(self):
    self.init_window()
    self.init_music()
    self.init_bullet()
    self.init_key()
    self.load_world()
    self.init_player()
    self.init_objects()
    self.start_physics()

  def init_window(self):
    # Hide the mouse cursor
    props = WindowProperties()
    props.setCursorHidden(True)
    base.win.requestProperties(props)

  def init_music(self):
    music = base.loader.loadSfx("../data/snd/Bent_and_Broken.mp3")
    music.play()
    self.playferscream = base.loader.loadSfx("../data/snd/deadscrm.wav")

  def init_bullet(self):
    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))

#    debugNode = BulletDebugNode('Debug')
#    debugNode.showWireframe(True)
#    debugNode.showConstraints(True)
#    debugNode.showBoundingBoxes(True)
#    debugNode.showNormals(True)
#    debugNP = render.attachNewNode(debugNode)
#    debugNP.show()
#    self.world.setDebugNode(debugNP.node())

#    alight = AmbientLight('alight')
#    alight.setColor(VBase4(1.0, 1.0, 1.0, 1))
#    alnp = render.attachNewNode(alight)
#    render.setLight(alnp)

  def init_key(self):

    # Stores the state of the keys, 1 for pressed and 0 for unpressed
    self.key_state = {'up':0, 'right':0, 'down':0, 'left':0}

    # Assign the key event handler
    self.accept('w', self.set_key_state, ['up',1])
    self.accept('w-up', self.set_key_state, ['up',0])
    self.accept('d', self.set_key_state, ['right',1])
    self.accept('d-up', self.set_key_state, ['right',0])
    self.accept('s', self.set_key_state, ['down',1])
    self.accept('s-up', self.set_key_state, ['down',0])
    self.accept('a', self.set_key_state, ['left',1])
    self.accept('a-up', self.set_key_state, ['left',0])

    self.accept('z', self.print_pos)
    
    # Esc
    self.accept('escape', sys.exit)

  def set_key_state(self, key, state):
    self.key_state[key] = state

  def print_pos(self):
    print self.player.getPos()

  def egg_to_BulletTriangleMeshShape(self, modelnp):
    mesh = BulletTriangleMesh()
    for collisionNP in modelnp.findAllMatches('**/+CollisionNode'):
      collisionNode = collisionNP.node()
    for collisionPolygon in collisionNode.getSolids():
	tri_points = collisionPolygon.getPoints()
        mesh.addTriangle(tri_points[0],tri_points[1],tri_points[2])
    shape = BulletTriangleMeshShape(mesh, dynamic=False) 
    return shape

  def load_world(self):
#    stairwell = loader.loadModel('../data/mod/boxroom.egg')
    stairwell = loader.loadModel('../data/mod/jcmbstairs.egg')
    stairwell.reparentTo(render)
    stairwell.setPos(0,0,0)
    stairwell_shape = self.egg_to_BulletTriangleMeshShape(stairwell)
    stairwellnode = BulletRigidBodyNode('stairwell')
    stairwellnode.addShape(stairwell_shape)
    self.world.attachRigidBody(stairwellnode)

  def init_player(self):
    # Stop the default mouse behaviour
    base.disableMouse()
    
    # Character has a collision sphere
    shape = BulletCapsuleShape(0.8, 4.5, ZUp)
    self.player = BulletRigidBodyNode('Player')
    self.player.setMass(1.0)
    self.player.addShape(shape)
    self.playernp = render.attachNewNode(self.player)
    self.playernp.setPos(0, 0, 10)
    self.world.attachRigidBody(self.player)

    self.player.setLinearSleepThreshold(0.0)
    self.player.setAngularFactor(0.0)

    # Tie the camera to the player
    base.camera.reparentTo(self.playernp)
    base.camera.setPos(0,0,4.5)
    base.camLens.setFov(80)
    
    # Make the torch and attach it to our character
    torch = Spotlight('torch')
    torch.setColor(VBase4(1, 1, 1, 1))
    lens = PerspectiveLens()
    lens.setFov(80)
    lens.setNearFar(20, 100)
    torch.setLens(lens)
    self.torchnp = base.camera.attachNewNode(torch)
    self.torchnp.setPos(0, 0, 0)
    render.setLight(self.torchnp)
    
    # Allow the world to be illuminated by our torch
    render.setLight(self.torchnp)
    
    # Add the player update task
    taskMgr.add(self.update, 'update_player_task')
    
  def init_objects(self):
    shape = BulletBoxShape(Vec3(1.0, 1.0, 1.0))
    node = BulletRigidBodyNode('PlayferBox')
    node.setMass(1.0)
    node.addShape(shape)
    np = render.attachNewNode(node)
    np.setPos(-10, -13, -10)
    self.world.attachRigidBody(node)

    playferboxmodel = loader.loadModel('../data/mod/playferbox.egg')
    playferboxmodel.reparentTo(np)

  def update(self,task):
       
    # Update camera orientation
    md = base.win.getPointer(0)
    x = md.getX()
    y = md.getY()
    if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2):
      base.camera.setH(base.camera.getH() - (x - base.win.getXSize()/2) * 0.25)
      base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2) * 0.25)
    
    # Update player position
    self.player.clearForces()
    vel = self.player.getLinearVelocity()
    direction = Vec3(0,0, vel.getZ())
    if (self.key_state["left"] == 1):
      direction.setX(-10.0)
    if (self.key_state["right"] == 1):
      direction.setX(10.0)
    if (self.key_state["up"] == 1):
      direction.setY(10.0)
    if (self.key_state["down"] == 1):
      direction.setY(-10.0)

    direction = render.getRelativeVector(base.camera, direction)
    linear_force = (direction - vel)/(0.01)
    self.player.applyCentralForce(linear_force)

    return task.cont

  def update_physics(self, task):
    dt = globalClock.getDt()
    self.world.doPhysics(dt)
    return task.cont

  def start_physics(self):
    taskMgr.add(self.update_physics, 'update_physics')

base.setFrameRateMeter(True)
EscapeFromJCMB()
render.setShaderAuto()

run() 
