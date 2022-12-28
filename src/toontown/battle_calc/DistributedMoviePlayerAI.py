from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from toontown.battle.BattleBase import *
from toontown.battle import MovieSuitAttacks
from direct.interval.IntervalGlobal import *

class DistributedMoviePlayerAI(DistributedObjectAI.DistributedObjectAI, DirectObject):

    def __init__(self, air, battle):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        DirectObject.__init__(self)
        self.air = air
        self.battle = battle

    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)
        DirectObject.delete(self)

    def playMovie(self):
        movie = []
        suitAttacks = []
        for suit in self.battle.activeSuits:
            suitAttacks.append(suit.listener.attack)
        for suitAttack in suitAttacks:
            ival, camIval = MovieSuitAttacks.doSuitAttack(suitAttack)
            movie.append(ival)
        movie.play()

