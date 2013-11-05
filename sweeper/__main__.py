from sweeper.gui import App
from sweeper import Robot, PlayGround
from sweeper.client import Client

my_robot = Robot(0.5)
delta_playground = PlayGround(400)

app = App(my_robot, delta_playground)
Client(app)
app.start()
