# Sweeper #
Graphical User Interface for mine sweeper competition

## Overview ##
a `Tkinter` based interface designed to be integrated with any software/hardware you use.

### features ###

* customizable robot, playground dimensions to fit training purposes 
* pause utility for time outs
* you can import/export playground state any time to json

![screenshot](https://raw.github.com/myaser/sweeper/master/screenshot.png "screenshot")

## usage ##
here is a snippet 


```python

from sweeper.gui import App
from sweeper import Robot, PlayGround
from sweeper.client import Client

class MyClient(Client):
    def set_up(self):
        #  do your magic here

    def process(self):
        #  do your magic here

my_robot = Robot(0.5)  # initialize with distance between robot's center of math and the metal detector sensor
delta_playground = PlayGround(400)  # initialize with the Area of the playground

app = App(my_robot, delta_playground)
MyClient(app)
app.start()
```
