import sys
import math
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from panda3d.bullet import *
from direct.gui import *
from Room import *

class Player(DirectObject):
  camera = None
  speed = 3
  player_is_grabbing = False
  cs = None
  node = None
  nodepath = None
  bulletworld = None

  def __init__(self, camera, camLens, bulletworld, render, taskMgr):

    # Player is called Player...
    self.name = 'Player'

    self.camera = camera

    self.bulletworld = bulletworld

    # Stop the default mouse behaviour
    base.disableMouse()


    # Character has a capsule shape
    collision_shape = BulletCapsuleShape(0.2, 1, ZUp)

    self.node = BulletRigidBodyNode('Player')
    self.node.setMass(80.0)
    self.node.addShape(collision_shape)
    self.node.setLinearSleepThreshold(0.0)
    self.node.setAngularFactor(0.0)
    self.nodepath = render.attachNewNode(self.node)
    self.nodepath.setPos(0, 0, 1)
    bulletworld.attachRigidBody(self.node)

    # Attach the camera to the player's head
    camera.reparentTo(self.nodepath)
    camLens.setFov(80)
    camLens.setNear(0.01)
   
    # Make the torch and attach it to our character
    torch = Spotlight('torch')
    torch.setColor(VBase4(1, 1, 1, 1))
    lens = PerspectiveLens()
    lens.setFov(80)
    lens.setNearFar(20, 100)
    torch.setLens(lens)
    self.torchnp = camera.attachNewNode(torch)
    self.torchnp.setPos(0, 0, 0)
    
    # Allow the world to be illuminated by our torch
    render.setLight(self.torchnp)
    
    # Player's "hand" in the world
    self.hand = BulletRigidBodyNode('Hand') 
    self.hand.addShape(BulletSphereShape(0.1))
    self.hand.setLinearSleepThreshold(0.0)
    self.hand.setLinearDamping(0.9999999)
    self.hand.setAngularFactor(0.0)
    self.hand.setMass(1.0)
    bulletworld.attachRigidBody(self.hand)
    self.handnp = render.attachNewNode(self.hand)
    self.handnp.setCollideMask(BitMask32.allOff())

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

    # Disable the depth testing for the hand and the text - we always want these things on top, with no clipping
    self.hand_text_np.setDepthTest(False)

    self.init_key()

    # Add the player update task
    taskMgr.add(self.update, 'update_player_task')


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

  def set_key_state(self, key, state):
    self.key_state[key] = state

  def set_mouse_state(self, button, state):
    self.mouse_state[button] = state

  def update(self,task):       

    # Update camera orientation
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
    player_is_moving = False
    if (self.key_state["up"] == True):
      player_is_moving = True
      dir = 0
    if (self.key_state["down"] == True):
      player_is_moving = True
      dir = 180
    if (self.key_state["left"] == True):
      player_is_moving = True
      dir = 90
    if (self.key_state["right"] == True):
      player_is_moving = True
      dir = 270

    self.node.clearForces()
    old_vel = self.node.getLinearVelocity()
    new_vel = Vec3(0,0,0)
    if player_is_moving == True:
      new_vel.setX(-self.speed * math.sin((camera.getH() + dir) * 3.1415/180.0))
      new_vel.setY(self.speed * math.cos((camera.getH() + dir) * 3.1415/180.0))

    timescale = 0.001
    linear_force = (new_vel - old_vel)/(timescale)
    linear_force.setZ(0.0)
    self.node.applyCentralForce(linear_force)
    
    if self.player_is_grabbing == False:
      new_hand_pos = LPoint3f(render.getRelativePoint(camera, Vec3(0,0.2,0)))
      self.handnp.setPos(new_hand_pos)
    else:
      new_hand_pos = LPoint3f(render.getRelativePoint(camera, Vec3(0,0.5,0)))
      diff = new_hand_pos - self.handnp.getPos()
      self.hand.applyCentralForce(diff * 1000 - self.hand.getLinearVelocity()*100)
      if diff.length() > .5:
        self.node.setLinearVelocity(Vec3(0,0,0))

    # Identify what lies beneath the player's hand (unless player is holding something)
    if self.player_is_grabbing == False:
      ray_from = self.nodepath.getPos()
      ray_to = LPoint3f(render.getRelativePoint(camera, Vec3(0,1,0)))
      result = self.bulletworld.rayTestClosest(ray_from, ray_to)
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
              self.bulletworld.attachConstraint(self.cs)

              # Stop the held object swinging all over the place
              result.getNode().setAngularDamping(0.7)
      else:
        self.hand_text_np.hide()
        self.player_is_grabbing = False

    if self.mouse_state["left_click"] == False:
      self.player_is_grabbing = False
      if self.cs != None:
        self.bulletworld.remove_constraint(self.cs)
        self.cs = None
        self.grabbed_node.setAngularDamping(0.0)

    if self.player_is_grabbing == True and self.mouse_state["right_click"] == True:
        self.bulletworld.remove_constraint(self.cs)
        self.cs = None
        self.grabbed_node.setAngularDamping(0.0)
        self.grabbed_node.setActive(True)
        self.grabbed_node.applyCentralImpulse(1000,0,0)


    if self.player_is_grabbing == True:
      self.hand_text_np.hide()

    return task.cont
