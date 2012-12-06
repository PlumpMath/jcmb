# All objects, animate or not, are Things with a name, a visible geometry (optional), a collision shape,
# and a behaviour if another thing tries to "grab" them
class Thing:
  name = 'Unnamed'
  model = None
  nodepath = None
  collision_node = None
  flags = []

  def get_name(self):
    return self.name

  def get_model(self):
    return self.model

  def get_nodepath(self):
    return self.nodepath

  def get_collision_node(self):
    return self.collision_node

  def is_grabbable(self):
    return ("grab" in self.flags)

  def on_grab(self):
    raise NotImplementedError("This method has not been implemented and it damn well should have.")

  def on_drop(self):
    raise NotImplementedError("This method has not been implemented and it damn well should have.")


class Sentient:
  def update(self):
          raise NotImplementedError("This method has not been implemented.")

  def grab(self, thing):
          raise NotImplementedError("This method has not been implemented.")

class NPC(Thing, Sentient):
  alive = True
  def is_alive(self):
    return alive



