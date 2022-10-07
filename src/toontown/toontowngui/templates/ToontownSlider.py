from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

class ToontownSlider(DirectFrame):
    def __init__(self, FuncCommand, valRange, value, pageSize, scale):
        DirectFrame.__init__(self, frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))

        self.item = DirectSlider(range=valRange, value=value, pageSize=pageSize, command=FuncCommand, scale=scale)

    def getButton(self):
        return self.button
