# All objects, animate or not, are Things with a name, a visible geometry (optional), a collision shape,
# and a behaviour if another thing tries to "grab" them
class Thing:
        name = 'Unnamed'
        model = None
        collision_shape = None
        grabbable = False

        def get_name(self):
                return name

        def get_model(self):
                return model

        def get_collision_shape(self):
                return collision_shape

        def is_grabbable(self):
                return grabbable

        def on_grab(self):
                raise NotImplementedError("This method has not been implemented.")

        def on_drop(self):
                raise NotImplementedError("This method has not been implemented.")

class Sentient:
        def update(self):
                raise NotImplementedError("This method has not been implemented.")

	def grab(self, thing):
                raise NotImplementedError("This method has not been implemented.")

class NPC(Thing, Sentient):
        alive = True
        def is_alive(self):
                return alive
