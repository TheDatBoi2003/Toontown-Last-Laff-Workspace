from panda3d.core import *
from libotp import *
from direct.interval.IntervalGlobal import *
from BattleBase import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
import DistributedBattleBase
from direct.directnotify import DirectNotifyGlobal
import MovieUtil
from toontown.suit import Suit
from direct.actor import Actor
from toontown.toon import TTEmote
from otp.avatar import Emote
import SuitBattleGlobals
import BattleProps
from toontown.distributed import DelayDelete
import random

class DistributedBattle(DistributedBattleBase.DistributedBattleBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattle')
    camFOFov = ToontownBattleGlobals.BattleCamFaceOffFov
    camFOPos = ToontownBattleGlobals.BattleCamFaceOffPos
    PlayGameSetPlaceEvent = 'playGameSetPlace'

    def __init__(self, cr):
        townBattle = cr.playGame.hood.loader.townBattle
        DistributedBattleBase.DistributedBattleBase.__init__(self, cr, townBattle)
        self.setupCollisions(self.uniqueBattleName('battle-collide'))

    def generate(self):
        DistributedBattleBase.DistributedBattleBase.generate(self)

    def announceGenerate(self):
        DistributedBattleBase.DistributedBattleBase.generate(self)

    def disable(self):
        DistributedBattleBase.DistributedBattleBase.disable(self)
        self.ignore(self.PlayGameSetPlaceEvent)

    def delete(self):
        DistributedBattleBase.DistributedBattleBase.delete(self)
        self.ignore(self.PlayGameSetPlaceEvent)
        self.removeCollisionData()

    def setInteractivePropTrackBonus(self, trackBonus):
        DistributedBattleBase.DistributedBattleBase.setInteractivePropTrackBonus(self, trackBonus)
        if self.interactivePropTrackBonus >= 0:
            if base.cr.playGame.hood:
                self.calcInteractiveProp()
            else:
                self.acceptOnce(self.PlayGameSetPlaceEvent, self.calcInteractiveProp)

    def calcInteractiveProp(self):
        if base.cr.playGame.hood:
            loader = base.cr.playGame.hood.loader
            if hasattr(loader, 'getInteractiveProp'):
                self.interactiveProp = loader.getInteractiveProp(self.zoneId)
                self.notify.debug('self.interactiveProp = %s' % self.interactiveProp)
            else:
                self.notify.warning('no loader.getInteractiveProp self.interactiveProp is None')
        else:
            self.notify.warning('no hood  self.interactiveProp is None')

    def setMembers(self, suits, suitsJoining, suitsPending, suitsActive, suitsLured, suitTraps, toons, toonsJoining, toonsPending, toonsActive, toonsRunning, timestamp):
        if self.battleCleanedUp():
            return
        oldtoons = DistributedBattleBase.DistributedBattleBase.setMembers(self, suits, suitsJoining, suitsPending, suitsActive, suitsLured, suitTraps, toons, toonsJoining, toonsPending, toonsActive, toonsRunning, timestamp)
        if len(self.toons) == 4 and len(oldtoons) < 4:
            self.notify.debug('setMembers() - battle is now full of toons')
            self.closeBattleCollision()
        elif len(self.toons) < 4 and len(oldtoons) == 4:
            self.openBattleCollision()

    def __faceOff(self, ts, name, callback):
        if len(self.suits) == 0:
            self.notify.warning('__faceOff(): no suits.')
            return
        if len(self.toons) == 0:
            self.notify.warning('__faceOff(): no toons.')
            return
        suit = self.suits[0]
        point = self.suitPoints[0][0]
        suitPos = point[0]
        suitHpr = VBase3(point[1], 0.0, 0.0)
        toon = self.toons[0]
        point = self.toonPoints[0][0]
        toonPos = point[0]
        toonHpr = VBase3(point[1], 0.0, 0.0)
        p = toon.getPos(self)
        toon.setPos(self, p[0], p[1], 0.0)
        toon.setShadowHeight(0)
        suit.setState('Battle')
        suitTrack = Sequence()
        toonTrack = Sequence()
        suitTrack.append(Func(suit.loop, 'neutral'))
        suitTrack.append(Func(suit.headsUp, toon))
        suitTrack.append(Func(suit.wrtReparentTo, self))
        taunt = SuitBattleGlobals.getFaceoffTaunt(suit.getStyleName(), suit.doId)
        suitTrack.append(Func(suit.setChatAbsolute, taunt, CFSpeech | CFTimeout))
        toonTrack.append(Func(toon.loop, 'neutral'))
        toonTrack.append(Func(toon.headsUp, suit))
        suitHeight = suit.getHeight()
        suitOffsetPnt = Point3(0, 0, suitHeight)
        faceoffTime = self.calcFaceoffTime(self.getPos(), self.initialSuitPos)
        faceoffTime = max(faceoffTime, BATTLE_SMALL_VALUE)
        delay = FACEOFF_TAUNT_T
        if self.hasLocalToon():
            MidTauntCamHeight = suitHeight * 0.66
            MidTauntCamHeightLim = suitHeight - 1.8
            if MidTauntCamHeight < MidTauntCamHeightLim:
                MidTauntCamHeight = MidTauntCamHeightLim
            TauntCamY = 16
            TauntCamX = random.choice((-5, 5))
            TauntCamHeight = random.choice((MidTauntCamHeight, 1, 11))
            camTrack = Sequence()
            camTrack.append(Func(camera.wrtReparentTo, suit))
            camTrack.append(Func(base.camLens.setMinFov, self.camFOFov / (4. / 3.)))
            camTrack.append(Func(camera.setPos, TauntCamX, TauntCamY, TauntCamHeight))
            camTrack.append(Func(camera.lookAt, suit, suitOffsetPnt))
            camTrack.append(Wait(delay))
            camTrack.append(Func(base.camLens.setMinFov, self.camFov / (4. / 3.)))
            camTrack.append(Func(camera.wrtReparentTo, self))
            camTrack.append(Func(camera.setPos, self.camFOPos))
            camTrack.append(Func(camera.lookAt, suit.getPos(self)))
            camTrack.append(Wait(faceoffTime))
            if self.interactiveProp:
                camTrack.append(Func(camera.lookAt, self.interactiveProp.node.getPos(self)))
                camTrack.append(Wait(FACEOFF_LOOK_AT_PROP_T))
        suitTrack.append(Wait(delay))
        toonTrack.append(Wait(delay))
        if faceoffTime >= 8.0:
            suitTrack.append(Func(suit.headsUp, self, suitPos))
            suitTrack.append(Func(suit.clearChat))
            destPos, h = self.suitPoints[0][0]
            toonTrack.append(Func(toon.enterTeleportOut))
            toonTrack.append(Wait(4))
            toonTrack.append(Func(toon.hide))
            moveIval = Sequence(Func(suit.headsUp, self), Func(suit.pose, 'landing', 0),
                                ProjectileInterval(suit, duration=faceoffTime / 3, endPos=destPos, gravityMult=0.1),
                                ActorInterval(suit, 'landing'), Func(suit.loop, 'neutral'))
            if suit.prop is None:
                suit.prop = BattleProps.globalPropPool.getProp('propeller')
            suit.prop.hide()
            propDur = suit.prop.getDuration('propeller')
            landingDur = suit.getDuration('landing')
            lastSpinFrame = 8
            fr = suit.prop.getFrameRate('propeller')
            spinTime = lastSpinFrame / fr
            openTime = (lastSpinFrame + 1) / fr
            suit.attachPropeller()
            propTrack = Parallel(Func(suit.prop.show),
                                 SoundInterval(suit.propInSound, duration=faceoffTime / 3, node=suit), Sequence(
                    ActorInterval(suit.prop, 'propeller', constrainedLoop=1, duration=faceoffTime / 3 + 1,
                                  startTime=0.0,
                                  endTime=spinTime),
                    ActorInterval(suit.prop, 'propeller', duration=landingDur, startTime=openTime),
                    Func(suit.detachPropeller)))
            result = Parallel(moveIval, propTrack)
            suitTrack.append(Func(suit.setHpr, h))
            suitTrack.append(result)
            toonTrack.append(Func(toon.setHpr, self, toonHpr))
            toonTrack.append(Func(toon.setPos, self, toonPos))
            toonTrack.append(Func(toon.show))
            toonTrack.append(Func(toon.enterTeleportIn))
            if base.localAvatar == toon:
                soundTrack = Sequence(Wait(delay))
            else:
                soundTrack = Wait(delay + faceoffTime)
            mtrack = Parallel(suitTrack, toonTrack, soundTrack)
            if self.hasLocalToon():
                NametagGlobals.setMasterArrowsOn(0)
                mtrack = Parallel(mtrack, camTrack)
            done = Func(callback)
            track = Sequence(mtrack, done, name=name)
            track.delayDeletes = [DelayDelete.DelayDelete(toon, '__faceOff'),
                                  DelayDelete.DelayDelete(suit, '__faceOff')]
            track.start(ts)
            self.storeInterval(track, name)
        else:
            suitTrack.append(Func(suit.headsUp, self, suitPos))
            suitTrack.append(Func(suit.clearChat))
            toonTrack.append(Func(toon.headsUp, self, toonPos))
            suitTrack.append(Func(suit.loop, 'walk'))
            suitTrack.append(LerpPosInterval(suit, faceoffTime, suitPos, other=self))
            suitTrack.append(Func(suit.loop, 'neutral'))
            suitTrack.append(Func(suit.setHpr, self, suitHpr))
            toonTrack.append(Func(toon.loop, 'run'))
            toonTrack.append(LerpPosInterval(toon, faceoffTime, toonPos, other=self))
            toonTrack.append(Func(toon.loop, 'neutral'))
            toonTrack.append(Func(toon.setHpr, self, toonHpr))
            if base.localAvatar == toon:
                soundTrack = Sequence(Wait(delay),
                                      SoundInterval(base.localAvatar.soundRun, loop=1, duration=faceoffTime,
                                                    node=base.localAvatar))
            else:
                soundTrack = Wait(delay + faceoffTime)
            mtrack = Parallel(suitTrack, toonTrack, soundTrack)
            if self.hasLocalToon():
                NametagGlobals.setMasterArrowsOn(0)
                mtrack = Parallel(mtrack, camTrack)
            done = Func(callback)
            track = Sequence(mtrack, done, name=name)
            track.delayDeletes = [DelayDelete.DelayDelete(toon, '__faceOff'),
                                  DelayDelete.DelayDelete(suit, '__faceOff')]
            track.start(ts)
            self.storeInterval(track, name)

    def enterFaceOff(self, ts):
        self.notify.debug('enterFaceOff()')
        self.delayDeleteMembers()
        if len(self.toons) > 0 and base.localAvatar == self.toons[0]:
            Emote.globalEmote.disableAll(self.toons[0], 'dbattle, enterFaceOff')
        self.__faceOff(ts, self.faceOffName, self.__handleFaceOffDone)
        if self.interactiveProp:
            self.interactiveProp.gotoFaceoff()

    def __handleFaceOffDone(self):
        self.notify.debug('FaceOff done')
        if len(self.toons) > 0 and base.localAvatar == self.toons[0]:
            self.d_faceOffDone(base.localAvatar.doId)

    def exitFaceOff(self):
        self.notify.debug('exitFaceOff()')
        if len(self.toons) > 0 and base.localAvatar == self.toons[0]:
            Emote.globalEmote.releaseAll(self.toons[0], 'dbattle exitFaceOff')
        self.finishInterval(self.faceOffName)
        self.clearInterval(self.faceOffName)
        self._removeMembersKeep()

    def enterReward(self, ts):
        self.notify.debug('enterReward()')
        self.disableCollision()
        self.delayDeleteMembers()
        Emote.globalEmote.disableAll(base.localAvatar, 'dbattle, enterReward')
        if self.hasLocalToon():
            NametagGlobals.setMasterArrowsOn(0)
            if self.localToonActive() == 0:
                self.removeInactiveLocalToon(base.localAvatar)
        for toon in self.toons:
            toon.startSmooth()

        self.accept('resumeAfterReward', self.handleResumeAfterReward)
        if self.interactiveProp:
            self.interactiveProp.gotoVictory()
        self.playReward(ts)

    def playReward(self, ts):
        self.movie.playReward(ts, self.uniqueName('reward'), self.handleRewardDone)

    def handleRewardDone(self):
        self.notify.debug('Reward done')
        if self.hasLocalToon():
            self.d_rewardDone(base.localAvatar.doId)
        self.movie.resetReward()
        messenger.send('resumeAfterReward')

    def handleResumeAfterReward(self):
        self.fsm.request('Resume')

    def exitReward(self):
        self.notify.debug('exitReward()')
        self.ignore('resumeAfterReward')
        self.movie.resetReward(finish=1)
        self._removeMembersKeep()
        NametagGlobals.setMasterArrowsOn(1)
        Emote.globalEmote.releaseAll(base.localAvatar, 'dbattle, exitReward')

    def enterResume(self, ts = 0):
        self.notify.debug('enterResume()')
        if self.hasLocalToon():
            self.removeLocalToon()
        if self.interactiveProp:
            self.interactiveProp.requestIdleOrSad()

    def exitResume(self):
        pass

    def enterNoLocalToon(self):
        self.notify.debug('enterNoLocalToon()')
        self.enableCollision()

    def exitNoLocalToon(self):
        self.disableCollision()

    def enterWaitForServer(self):
        self.notify.debug('enterWaitForServer()')

    def exitWaitForServer(self):
        pass
