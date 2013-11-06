from threading import Thread, Event


class Client(Thread):

    def __init__(self, gui, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.gui = gui
        self.gui.set_client(self)
        self.allow_working = Event()
        self.stop_flag = Event()
        self.setDaemon(True)

    def move_robot_to(self, (x, y, theta)):
        self.gui.robot.set_position((x, y, theta))

    def mark_current_block_as_buried_mine_block(self):
        pos = self.gui.robot.metal_detector_position
        blk = self.gui.playground.get_block(pos)
        blk.put_buried_mine()

    def mark_current_block_as_surface_mine_block(self):
        pos = self.gui.robot.metal_detector_position
        blk = self.gui.playground.get_block(pos)
        blk.put_serface_mine()

    def redraw_gui(self):
        self.gui.draw()

    def stop(self):
        self.stop_flag.set()

    def set_up(self):
        raise NotImplementedError()

    def process(self):
        raise NotImplementedError()

    def run(self):
        self.set_up()
        while True:
            self.allow_working.wait()
            if self.stop_flag.is_set():
                break
            self.process()
