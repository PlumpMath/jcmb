import sys
import math
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
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import ZUp
from panda3d.bullet import BulletConeTwistConstraint
from direct.gui import *

class EscapeFromJCMB(object,DirectObject):

  def __init__(self):
    print "Loading..."
    self.init_window()
    self.init_music()
    self.init_bullet()
    self.init_key()
    self.load_world()
    self.init_player()
    self.init_objects()
    render.prepareScene(base.win.getGsg())
    print "Done"
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
#    debugNode.showBoundingBoxes(False)
#    debugNode.showNormals(False)
#    debugNP = render.attachNewNode(debugNode)
#    debugNP.show()
#    self.world.setDebugNode(debugNP.node())

    alight = AmbientLight('alight')
    alight.setColor(VBase4(0.05, 0.05, 0.05, 1))
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)

  def init_key(self):

    # Stores the state of the keys, 1 for pressed and 0 for unpressed
    self.key_state = {'up':False, 'right':False, 'down':False, 'left':False}

    # Assign the key event handler
    self.accept('w', self.set_key_state, ['up',True])
    self.accept('w-up', self.set_key_state, ['up',False])
    self.accept('d', self.set_key_state, ['right',True])
    self.accept('d-up', self.set_key_state, ['right',False])
    self.accept('s', self.set_key_state, ['down',True])
    self.accept('s-up', self.set_key_state, ['down',False])
    self.accept('a', self.set_key_state, ['left',True])
    self.accept('a-up', self.set_key_state, ['left',False])

    # Stores the state of the mouse buttons, 1 for pressed and 0 for unpressed
    self.mouse_state = {'left_click':False, 'right_click':False}

    # Assign the mouse click event handler
    self.accept('mouse1', self.set_mouse_state, ['left_click',True])
    self.accept('mouse1-up', self.set_mouse_state, ['left_click',False])
    self.accept('mouse2', self.set_mouse_state, ['right_click',True])
    self.accept('mouse2-up', self.set_mouse_state, ['right_click',False])

    self.accept('z', self.print_pos)
    
    # Esc
    self.accept('escape', sys.exit)

  def set_key_state(self, key, state):
    self.key_state[key] = state

  def set_mouse_state(self, button, state):
    self.mouse_state[button] = state

  def print_pos(self):
    print self.playernp.getPos()

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
    stairwell = loader.loadModel('../data/mod/jcmbstairs.egg')
    stairwell.reparentTo(render)
    stairwell_shape = self.egg_to_BulletTriangleMeshShape(stairwell)
    stairwellnode = BulletRigidBodyNode('stairwell')
    stairwellnode.addShape(stairwell_shape)
    self.world.attachRigidBody(stairwellnode)

  def init_player(self):
    # Stop the default mouse behaviour
    base.disableMouse()

    self.oldmx = 0
    self.oldmy = 0
    
    # Character has a capsule shape
    shape = BulletCapsuleShape(0.2, 1, ZUp)
    self.player = BulletRigidBodyNode('Player')
    self.player.setMass(80.0)
    self.player.addShape(shape)
    self.playernp = render.attachNewNode(self.player)
    self.playernp.setPos(0, 0, 1)
    self.world.attachRigidBody(self.player)

    self.player.setLinearSleepThreshold(0.0)
    self.player.setAngularFactor(0.0)

    self.player_speed = 3
    self.player_is_grabbing = False

#    self.head = BulletRigidBodyNode('Player Head')
#    self.head.addShape(BulletSphereShape(0.2))
#    self.head.setMass(10)
#    self.head.setInertia(Vec3(1,1,1))
#    self.head.setAngularFactor(1.0)
#    self.head.setLinearFactor(0.0)
#    self.headnp = self.playernp.attachNewNode(self.head)
#    self.headnp.setPos(0,0,0)
#    self.headnp.setCollideMask(BitMask32.allOff())
#    self.world.attachRigidBody(self.head)
    
    # Attach the camera to the player's head
    base.camera.reparentTo(self.playernp)
#    base.camera.setPos(0,0,.5)
    base.camLens.setFov(80)
    base.camLens.setNear(0.01)
   
    # Make the torch and attach it to our character
    torch = Spotlight('torch')
    torch.setColor(VBase4(1, 1, 1, 1))
    lens = PerspectiveLens()
    lens.setFov(80)
    lens.setNearFar(20, 100)
    torch.setLens(lens)
    self.torchnp = base.camera.attachNewNode(torch)
    self.torchnp.setPos(0, 0, 0)
    
    # Allow the world to be illuminated by our torch
    render.setLight(self.torchnp)
    
    self.cs = None

    # Player's "hand" in the world
    hand_model = loader.loadModel('../data/mod/hand.egg')
    hand_model.setScale(1)
    hand_model.setBillboardPointEye()

    self.hand = BulletRigidBodyNode('Hand') 
    self.hand.addShape(BulletSphereShape(0.1))
    self.hand.setLinearSleepThreshold(0.0)
    self.hand.setLinearDamping(0.9999999)
    self.hand.setAngularFactor(0.0)
    self.hand.setMass(1.0)
    self.world.attachRigidBody(self.hand)
    self.handnp = render.attachNewNode(self.hand)
    self.handnp.setCollideMask(BitMask32.allOff())
#    hand_model.reparentTo(self.handnp)

    # Create a text node to display object identification information and attach it to the player's "hand"
    self.hand_text = TextNode('Hand Text')
    self.hand_text.setText("Ch-ch-chek yoself befo yo rek yoself, bro.")
    self.hand_text.setAlign(TextNode.ACenter)
    self.hand_text.setTextColor(1,1,1,1)
    self.hand_text.setShadow(0.05, 0.05)
    self.hand_text.setShadowColor(0, 0, 0, 1)
    self.hand_text_np = render.attachNewNode(self.hand_text)
    self.hand_text_np.setScale(0.03)
    self.hand_text_np.setBillboardPointEye()
    self.hand_text_np.hide()



    new_hand_pos = LPoint3f(render.getRelativePoint(base.camera, Vec3(0,1,0)))
    self.handnp.setPos(new_hand_pos)

    # Disable the depth testing for the hand and the text - we always want these things on top, with no clipping
    self.handnp.setDepthTest(False)
    self.hand_text_np.setDepthTest(False)

    # Add the player update task
    taskMgr.add(self.update, 'update_player_task')
    

  def init_objects(self):

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

  def update(self,task):       
    # Update camera orientation
#    md = base.win.getPointer(0)
#    mx = md.getX()
#    my = md.getY()
#    around_z = (self.oldmx - mx)
#    around_x = (self.oldmy - my)
#    motion = Vec3(around_x, 0.0, around_z)
#    self.head.setAngularVelocity(motion)
#    self.oldmx = mx
#    self.oldmy = my
#
#    if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2):
#      around_z = (base.win.getXSize()/2 - x)
#      around_x = (base.win.getYSize()/2 - y)
#      motion = Vec3(around_x, 0.0, around_z)
#      self.head.setAngularVelocity(motion)

    md = base.win.getPointer(0)
    mouse_x = md.getX()
    mouse_y = md.getY()
    centre_x = base.win.getXSize()/2
    centre_y = base.win.getYSize()/2
    if base.win.movePointer(0, centre_x, centre_y):
      new_H = base.camera.getH() + (centre_x - mouse_x)
      new_P = base.camera.getP() + (centre_y - mouse_y)
      if new_P < -90:
        new_P = -90
      elif new_P > 90:
        new_P = 90
      base.camera.setH(new_H)
      base.camera.setP(new_P)
   
    # Update player position
    speed = 3
    self.player_is_moving = False
    if (self.key_state["up"] == True):
      self.player_is_moving = True
      dir = 0
    if (self.key_state["down"] == True):
      self.player_is_moving = True
      dir = 180
    if (self.key_state["left"] == True):
      self.player_is_moving = True
      dir = 90
    if (self.key_state["right"] == True):
      self.player_is_moving = True
      dir = 270

    self.player.clearForces()
    old_vel = self.player.getLinearVelocity()
    new_vel = Vec3(0,0,0)
    if self.player_is_moving == True:
      new_vel.setX(-speed * math.sin((base.camera.getH() + dir) * 3.1415/180.0))
      new_vel.setY(speed * math.cos((base.camera.getH() + dir) * 3.1415/180.0))

    if self.player_is_grabbing == True:
      timescale = 0.001
    else:
      timescale = 0.001

    linear_force = (new_vel - old_vel)/(timescale)
    linear_force.setZ(0.0)
    self.player.applyCentralForce(linear_force)

    
    if self.player_is_grabbing == False:
      new_hand_pos = LPoint3f(render.getRelativePoint(base.camera, Vec3(0,0.2,0)))
      self.handnp.setPos(new_hand_pos)
    else:
      new_hand_pos = LPoint3f(render.getRelativePoint(base.camera, Vec3(0,0.5,0)))
      diff = new_hand_pos - self.handnp.getPos()
      self.hand.applyCentralForce(diff * 1000 - self.hand.getLinearVelocity()*100)
      if diff.length() > .6:
        self.player.setLinearVelocity(Vec3(0,0,0))

    # Identify what lies beneath the player's hand (unless player is holding something)
    if self.player_is_grabbing == False:
      ray_from = self.playernp.getPos()
      ray_to = LPoint3f(render.getRelativePoint(base.camera, Vec3(0,1,0)))
      result = self.world.rayTestClosest(ray_from, ray_to)
      if result.hasHit() == True:
        self.hand_text.setText(result.getNode().getName())
        self.hand_text_np.setPos(result.getHitPos())
        self.hand_text_np.show()

        # If player clicks, grab the object by the nearest point (as chosen by ray)
        if self.mouse_state["left_click"] == True:
          if result.getNode().getNumChildren() == 1:
            obj = NodePath(result.getNode().getChild(0))

            if self.player_is_grabbing == False:
              self.player_is_grabbing = True

              # Find the position of contact in terms of the object's local coordinates.
              # Parent the player's hand to the grabbed object at that position.
              pos = obj.getRelativePoint(render, result.getHitPos())

              self.grabbed_node = result.getNode()
              self.grabbed_node.setActive(True)
              print self.grabbed_node

              frameA = TransformState.makePosHpr(Vec3(0,0,0), Vec3(0,0,0))
              frameB = TransformState.makePosHpr(Vec3(0,0,0), Vec3(0,0,0))
 
              swing1 = 20 # degrees
              swing2 = 20 # degrees
              twist = 20 # degrees
 
              self.cs = BulletConeTwistConstraint(self.hand, result.getNode(), frameA, frameB)
              self.cs.setLimit(swing1, swing2, twist)
              self.world.attachConstraint(self.cs)

              # Stop the held object swinging all over the place
              result.getNode().setAngularDamping(1.0)
      else:
        self.hand_text_np.hide()
        self.player_is_grabbing = False

    if self.mouse_state["left_click"] == False:
      self.player_is_grabbing = False
      if self.cs != None:
        self.world.remove_constraint(self.cs)
        self.cs = None
        self.grabbed_node.setAngularDamping(0.0)

    if self.player_is_grabbing == True and self.mouse_state["right_click"] == True:
        self.world.remove_constraint(self.cs)
        self.cs = None
        self.grabbed_node.setAngularDamping(0.0)
        self.grabbed_node.setActive(True)
        self.grabbed_node.applyCentralImpulse(1000,0,0)


    if self.player_is_grabbing == True:
      self.hand_text_np.hide()

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
