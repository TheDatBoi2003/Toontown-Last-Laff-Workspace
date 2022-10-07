from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

class ToontownButton(DirectFrame):
    def __init__(self, FuncCommand, buttonText, imgScale, otherArgs):
        DirectFrame.__init__(self, frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.item = DirectButton(text=buttonText, relief=None, scale=0.1, text_pos=(0, 0, 0),
                                        image_scale=imgScale, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')),
                                        command=FuncCommand, extraArgs=otherArgs)

    def getButton(self):
        return self.button
