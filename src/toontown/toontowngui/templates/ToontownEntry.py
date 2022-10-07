from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

class ToontownEntry(DirectFrame):
    def __init__(self, FuncCommand, scale):
        DirectFrame.__init__(self, frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        self.item = DirectEntry(text="", scale=scale, command=FuncCommand, initialText="", numLines = 2, focus=1)

    def getButton(self):
        return self.button
