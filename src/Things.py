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
        def updateAI(self):
                raise NotImplementedError("This method has not been implemented.")

class NPC(Thing, Sentient):
        alive = True
        def is_alive(self):
                return alive

