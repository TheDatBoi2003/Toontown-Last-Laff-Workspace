from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from toontown.toontowngui.ToontownGuiGlobals import *
from toontown.toontowngui.templates.ToontownSlider import ToontownSlider
from toontown.toontowngui.templates.ToontownButton import ToontownButton
from toontown.toontowngui.templates.ToontownEntry import ToontownEntry

class devPannel(DirectFrame):
    def __init__(self, toon):
        DirectFrame.__init__(self, frameColor=(0, 0, 0, 0.5), frameSize=(-1, 1, -1, 1))

        self.accept('q', self.destroy)

        self.catagory = 0

        self.backGround = OnscreenImage(image='phase_3/maps/tt_t_gui_ups_panelBg.png', pos=(0, 0, 0.0), scale=(1.50, 1.25, 0.75))
        self.backGround.reparentTo(self)
        self.backGround.setTransparency(TransparencyAttrib.MAlpha)
        self.backGround.setBin("BT_front_to_back", 0)

        self.generalButton = ToontownButton(self.setCatagory, 'General', toontown_general_button_image_scale, [0])
        self.generalButton.item.setPos(-1, 0, 0.70)
        self.generalButton.reparentTo(self)

        self.otherButton = ToontownButton(self.setCatagory, 'Cog', toontown_general_button_image_scale,
                                            [1])
        self.otherButton.item.setPos(-0.5, 0, 0.70)
        self.otherButton.reparentTo(self)

        self.otherButton1 = ToontownButton(self.setCatagory, 'Activity', toontown_general_button_image_scale,
                                          [2])
        self.otherButton1.item.setPos(-0.0, 0, 0.70)
        self.otherButton1.reparentTo(self)

        self.otherButton2 = ToontownButton(self.setCatagory, 'Funny', toontown_general_button_image_scale,
                                           [3])
        self.otherButton2.item.setPos(0.5, 0, 0.70)
        self.otherButton2.reparentTo(self)
        self.buttons=[self.generalButton, self.otherButton, self.otherButton1, self.otherButton2]

        self.button1 = ToontownButton(self.setCatagory, 'Activity', toontown_general_button_image_scale,
                                           [2])
        self.otherButton1.item.setPos(-0.0, 0, 0.70)
        self.otherButton1.reparentTo(self)

        self.entry = ToontownEntry(self.giveTickets, 0.05)
        self.entry.item.setPos(-1, 0, 0.0)
        self.entry.reparentTo(self)

        self.toon = toon

        self.hpSlider = ToontownSlider(self.changeToonHealth, (1, 137), 137, 1, 0.25)
        self.hpSlider.reparentTo(self)
        self.hpSlider.item.setPos(-1, 0, .40)

        self.maxhpSlider = ToontownSlider(self.changeMaxToonHealth, (1, 137), 137, 1, 0.25)
        self.maxhpSlider.reparentTo(self)
        self.maxhpSlider.item.setPos(-1, 0, .20)

        self.generalGUI = [self.hpSlider, self.maxhpSlider, self.entry]
        self.other1GUI = []
        self.other2GUI = []
        self.other3GUI = []

        self.allGUI = [self.generalGUI, self.other1GUI, self.other2GUI, self.other3GUI]

    def changeToonHealth(self):
        self.toon.changeHPtoAI(int(self.hpSlider.item['value']))

    def changeMaxToonHealth(self):
        self.toon.changeMAXHPtoAI(int(self.maxhpSlider.item['value']))

    def giveTickets(self, enteredNum):
        self.toon.ticketToAI(int(enteredNum))

    def setCatagory(self, catagory):
        if catagory == 0:
            self.showGUIfromList(self.allGUI[catagory])
            self.hideGUIfromList(self.allGUI[1])
            self.hideGUIfromList(self.allGUI[2])
            self.hideGUIfromList(self.allGUI[3])
        elif catagory == 1:
            self.showGUIfromList(self.allGUI[catagory])
            self.hideGUIfromList(self.allGUI[0])
            self.hideGUIfromList(self.allGUI[2])
            self.hideGUIfromList(self.allGUI[3])
        elif catagory == 2:
            self.showGUIfromList(self.allGUI[catagory])
            self.hideGUIfromList(self.allGUI[0])
            self.hideGUIfromList(self.allGUI[1])
            self.hideGUIfromList(self.allGUI[3])
        elif catagory == 3:
            self.showGUIfromList(self.allGUI[catagory])
            self.hideGUIfromList(self.allGUI[0])
            self.hideGUIfromList(self.allGUI[1])
            self.hideGUIfromList(self.allGUI[2])

    def hideGUIfromList(self, guiList):
        for gui in guiList:
            gui.item.hide()
        print('hiding guiList')

    def showGUIfromList(self, guiList):
        for gui in guiList:
            gui.item.show()
        print('showing guiList')

    def destroy(self):
        for guiList in self.allGUI:
            for gui in guiList:
                gui.item.destroy()
        for button in self.buttons:
            button.item.destroy()
        self.backGround.destroy()