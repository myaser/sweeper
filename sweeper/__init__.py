from math import sin, cos
from gmpy import is_square, sqrt
from numpy import asarray
from threading import Semaphore

n = 20


class Robot(object):
    def __init__(self, length, *args, **kwargs):
        self.length = length
        self.bound_to_palyground(None)
        self.set_position((0, 0, 0))
        object.__init__(self, *args, **kwargs)

    def bound_to_palyground(self, playground):
        self.playground = playground

    def is_bound_to_playground(self):
        if self.playground:
            return True
        else:
            return False

    def set_position(self, position):
        if self.is_bound_to_playground():
            threshold = lambda num: min(max(0, num), self.playground.length)
            x, y, thta = position
            position = (threshold(x), threshold(y), thta)
        self.position = position

    @property
    def metal_detector_position(self):
        x, y, t = self.position
        x_dim = x + (self.length * cos(t))
        y_dim = y + (self.length * sin(t))
        return x_dim, y_dim

    @classmethod
    def from_dict(cls, data):
        obj = cls(data['length'])
        obj.set_position(tuple(data['position']))
        return obj


class Block(object):
    '''playground block with 1*1 meter area
    '''
    def __init__(self, start_point, *args, **kwargs):
        self.start_point = start_point
        self.has_serface_mine = False
        self.has_buried_mine = False
        object.__init__(self, *args, **kwargs)

    def put_serface_mine(self):
        self.has_serface_mine = True
        self.has_buried_mine = False

    def put_buried_mine(self):
        self.has_buried_mine = True
        self.has_serface_mine = False


class PlayGround(object):
    def __init__(self, size=400, *args, **kwargs):
        '''initializes a square playground. size must be a perfect square
        '''
        if is_square(size):
            self.size = size
            self.length = int(sqrt(self.size))
            self.set_grid()
        else:
            raise ValueError("size must be a perfect square")
        object.__init__(self, *args, **kwargs)

    def set_grid(self, blocks_iterable=None):
        '''build a 2-dim grid of block objects
        '''
        n = self.length
        if not blocks_iterable:
            blocks_iterable = map(Block,
                                  [(i, j) for i in range(n) for j in range(n)])

        self.grid = asarray(blocks_iterable, object)
        self.grid = self.grid.reshape((n, n))

    def in_play_ground(self, (x, y)):
        if 0 < x < self.length and 0 < y < self.length:
            return True
        else:
            return False

    def get_block(self, (x, y)):
        ''' given a point return the block it lies in
        '''
        if not self.in_play_ground((x, y)):
            raise ValueError("block is outside the playground")
        return self.grid[x][y]

    def to_dict(self):
        grid_dict = [block.__dict__ for block in self.grid.reshape(self.size)]
        data = self.__dict__.copy()
        data['grid'] = grid_dict
        return data

    @classmethod
    def from_dict(cls, data):
        blocks_iterable = map(lambda blk: Block(**blk), data['grid'])
        obj = cls(size=data['size'])
        obj.set_grid(blocks_iterable)
        return obj
