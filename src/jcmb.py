import sys
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *


class EscapeFromJCMB(object,DirectObject):

  def __init__(self):
    self.init_window()
    self.init_music()
    self.init_collision()
    self.init_key()
    self.load_world()
    self.init_player()
    self.init_objects()
       

  def init_window(self):
    # Hide the mouse cursor
    props = WindowProperties()
    props.setCursorHidden(True)
    base.win.requestProperties(props)

  def init_music(self):
    music = base.loader.loadSfx("../data/snd/Bent_and_Broken.mp3")
    music.play()
    self.playferscream = base.loader.loadSfx("../data/snd/deadscrm.wav")

  def init_collision(self):
    base.cTrav = CollisionTraverser()
    base.cTrav.setRespectPrevTransform(True)
  
    self.pusher = PhysicsCollisionHandler()
    base.enableParticles()

    gravityFN=ForceNode('world-forces')
    gravityFNP=render.attachNewNode(gravityFN)
    gravityForce=LinearVectorForce(0,0,-9.81)
    gravityFN.addForce(gravityForce)
    base.physicsMgr.addLinearForce(gravityForce)
  
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
    
    # Esc
    self.accept('escape', sys.exit)

  def set_key_state(self, key, state):
    self.key_state[key] = state


  def load_world(self):
    self.world = loader.loadModel('../data/mod/jcmbstairs.egg')
    self.world.reparentTo(render)
    self.world.setPos(0,0,0)
    self.world.setH(90);

  def init_player(self):
    # Make our character node
    self.player = render.attachNewNode(ActorNode('playerNode'))
    self.player.reparentTo(render)
    self.player.setPos(0,0,0)
    self.player.setH(180)
    
    base.physicsMgr.attachPhysicalNode(self.player.node())
    
    # Tie the camera to the player
    base.camera.reparentTo(self.player)
    base.camera.setPos(0,0,0)
    
    # Stop the annoying default behaviour
    base.disableMouse()
    
    # Character has a collision sphere
    col_node = CollisionNode('player')
    col_node.addSolid(CollisionSphere(0, 0, -1, 1.4))
    col_node.addSolid(CollisionSphere(0, 0, -3, 1.4))
    col_node.addSolid(CollisionSphere(0, 0, -6, 1.4))
    col_node_path = self.player.attachNewNode(col_node)
    base.cTrav.addCollider(col_node_path, self.pusher)
    self.pusher.addCollider(col_node_path, self.player, base.drive.node())
          
    # Make the torch and attach it to our character
    torch = Spotlight('torch')

    torch.setColor(VBase4(1, 1, 1, 1))
    lens = PerspectiveLens()
    lens.setFov(120)
    lens.setNearFar(40, 300)
    torch.setLens(lens)
    self.torchnp = base.camera.attachNewNode(torch)
    self.torchnp.setPos(0, 0, 0)
    render.setLight(self.torchnp)
    
    # Allow the world to be illuminated by our torch
    self.world.setLight(self.torchnp)
    
    # Add the player update task
    taskMgr.add(self.update, 'update_player_task')
    
  def init_objects(self):
    self.playferbox = render.attachNewNode(ActorNode('playferbox'))
    self.playferbox.reparentTo(render)
    self.playferbox.setPos(-6,-170, 0)
    base.physicsMgr.attachPhysicalNode(self.playferbox.node())

    col_node = CollisionNode('playferbox')
    col_node.addSolid(CollisionSphere(-.5, -.5, -.5, .35))
    col_node.addSolid(CollisionSphere(.5, -.5, -.5, .35))
    col_node.addSolid(CollisionSphere(-.5, .5, -.5, .35))
    col_node.addSolid(CollisionSphere(.5, .5, -.5, .35))
    col_node.addSolid(CollisionSphere(-.5, -.5, .5, .35))
    col_node.addSolid(CollisionSphere(.5, -.5, .5, .35))
    col_node.addSolid(CollisionSphere(-.5, .5, .5, .35))
    col_node.addSolid(CollisionSphere(.5, .5, .5, .35))
    col_node_path = self.playferbox.attachNewNode(col_node)
    base.cTrav.addCollider(col_node_path, self.pusher)
    self.pusher.addCollider(col_node_path, self.playferbox, base.drive.node())

    playferboxmodel = loader.loadModel('../data/mod/playferbox.egg')
    playferboxmodel.setH(90)
    playferboxmodel.reparentTo(self.playferbox)

#    self.playferbox = render.attachNewNode (ActorNode("playferbox"))
#    playferboxmodel = loader.loadModel('../data/mod/playferbox.egg')
#    playferboxmodel.reparentTo(self.playferbox)
#    base.physicsMgr.attachPhysicalNode(self.playferbox.node())

#    base.cTrav.addCollider(self.playferbox, self.pusher)
#    self.pusher.addCollider(self.playferbox, self.playferbox, base.drive.node())

  def update(self,task):
       
    # Update camera orientation
    md = base.win.getPointer(0)
    x = md.getX()
    y = md.getY()
    if base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2):
      self.player.setH(self.player.getH() - (x - base.win.getXSize()/2) * 0.25)
      base.camera.setP(base.camera.getP() - (y - base.win.getYSize()/2) * 0.25)
    
    # Update player position
    self.player_speed = 40
    new_x = 0.0
    new_y = 0.0
    if (self.key_state["left"] == 1):
      new_x = -self.player_speed
    if (self.key_state["right"] == 1):
      new_x = self.player_speed
    if (self.key_state["up"] == 1):
      new_y = self.player_speed
    if (self.key_state["down"] == 1):
      new_y = -self.player_speed

    dt = globalClock.getDt()
    new_pos = Vec3(new_x, new_y, 0) * dt
    self.player.setFluidPos(self.player, new_pos)
    
    # Update steve
    new_pos = (self.player.getPos() - self.playferbox.getPos())
    if new_pos.length() < 50:
      new_pos.normalize()
      new_pos *= 40 * dt
      self.playferbox.setFluidPos(self.playferbox, new_pos)
      self.playferscream.setVolume(50.0/new_pos.length())
      if self.playferscream.status() == self.playferscream.READY:
        self.playferscream.play()
    else:
      self.playferscream.setVolume(0.0)

    return task.cont

base.setFrameRateMeter(True)
EscapeFromJCMB()
render.setShaderAuto()
run() 
