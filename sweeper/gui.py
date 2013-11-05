import json
import re
from os import path as pt
from datetime import datetime
import Image
from PIL import ImageTk
from Tkinter import (Frame, Button, Canvas, NW, Entry, END, NE, Tk)
from tkFileDialog import askopenfilename

from sweeper import Robot, PlayGround

BACKUP_DIR = pt.abspath(pt.join(__file__, pt.pardir, pt.pardir, 'backup'))
ARROW = Image.open(pt.join(BACKUP_DIR, pt.pardir, 'arrow.png'))
robot_states = []


class App():

    def __init__(self, robot, playground, canvas_size=600,
                 storage=BACKUP_DIR):

        self.robot = robot
        self.playground = playground
        self.robot.bound_to_palyground(playground)

        self.storage = storage

        self.master = Tk()
        self.canvas_size = canvas_size

        self.frame = Frame(self.master)
        self.frame.grid(row=0)

        self.canvas = Canvas(self.master, width=canvas_size, height=canvas_size,
                             borderwidth=2, highlightthickness=1)
        self.canvas.grid(row=1, columnspan=4)
        robot_states.append(ImageTk.PhotoImage(ARROW.copy()))

        # display & edit robot coordinates
        self.txt = Entry(self.master)
        self.txt.grid(row=3, column=2, sticky=NW)

        import_button = Button(self.master, text="edit robot position",
                               command=self.edit_robot_position)
        import_button.grid(row=3, column=2, sticky=NE)

        # start button
        import_button = Button(self.master, text="start", command=self.start_thread)
        import_button.grid(row=2, column=0, sticky=NW)

        # pause button
        import_button = Button(self.master, text="pause", command=self.pause_thread)
        import_button.grid(row=2, column=1, sticky=NW)

        # stop button
        import_button = Button(self.master, text="stop", command=self.end_prog)
        import_button.grid(row=2, column=2, sticky=NW)

        # import button
        import_button = Button(self.master, text="import", command=self.import_state)
        import_button.grid(row=3, column=0, sticky=NW)

        # export button
        export_button = Button(self.master, text="export", command=self.export_state)
        export_button.grid(row=3, column=1, sticky=NW)

        self.draw()

    def start(self):
        self.master.mainloop()

    def set_client(self, client):
        self.client = client

    def start_thread(self):
        self.client.allow_working.set()
        if not self.client.is_alive():
            self.client.start()

    def pause_thread(self):
        self.client.allow_working.clear()

    def end_prog(self):
        self.client.stop()
        self.frame.quit()

    def edit_robot_position(self):
        def is_valid(pos):
            if len(pos) != 3:
                return False
            else:
                return True

        pos = tuple(int(v) for v in re.findall("[0-9]+", self.txt.get()))

        if is_valid(pos):
            self.robot.set_position(pos)
            self.draw()

    def export_state(self):
        data = {'robot': self.robot.__dict__,
                'playground': self.playground.to_dict()}
        file_name = str(datetime.now()) + ".json"
        _file = open(pt.join(self.storage, file_name), 'w')
        _file.write(json.dumps(data, indent=4))

    def import_state(self):
        file_name = askopenfilename(parent=self.master)
        data = json.load(open(file_name))
        self.robot = Robot.from_dict(data['robot'])
        self.playground = PlayGround.from_dict(data['playground'])

    def draw(self):
        scale = self.canvas_size / self.playground.grid.shape[0]
        for row in self.playground.grid:
            for cell in row:
                x, y = [i * scale for i in cell.start_point]
                x1, y1 = x + scale, y + scale
                if cell.has_serface_mine:
                    self.canvas.create_rectangle(x, y, x1, y1, fill="red")
                elif cell.has_buried_mine:
                    self.canvas.create_rectangle(x, y, x1, y1, fill="black")
                else:
                    self.canvas.create_rectangle(x, y, x1, y1, fill="LightYellow2")

        x, y, t = self.robot.position
        robot_icon = ARROW.copy()
        robot_icon = robot_icon.rotate(t)
        robot_states.pop(0)
        robot_states.append(ImageTk.PhotoImage(robot_icon))
        self.canvas.create_image(x * scale, y * scale, image=robot_states[0])

        self.txt.delete(0, END)
        self.txt.insert(0, str(self.robot.position))
