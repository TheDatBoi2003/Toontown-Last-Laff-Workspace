from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger

class DistributedSuitListener(DistributedObject.DistributedObject, DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuitListener')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        DirectObject.__init__(self)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        DistributedObject.DistributedObject.disable(self)