from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from toontown.battle.BattleBase import *

class DistributedSuitListenerAI(DistributedObjectAI.DistributedObjectAI, DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuitListenerAI')

    def __init__(self, air, suit):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        DirectObject.__init__(self)
        self.suit = suit
        self.attack = [NO_ID, NO_ATTACK, -1, [], 0, 0, 0]

    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)
        DirectObject.delete(self)

    def calcSuitAttack(self):
        self.attack[SUIT_ID_COL] = self.suit.doId
        self.attack[ATTACK_COL] = 0
        self.attack[SUIT_TGT_COL] = 0
        self.attack[SUIT_HP_COL] = [10, 10, 10, 10]
        self.attack[SUIT_TAUNT_COL] = 0

    def calcSuitAttackDamage(self):
        return 10
