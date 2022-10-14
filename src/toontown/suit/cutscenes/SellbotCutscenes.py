from panda3d.core import *
from libotp import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import *
from direct.distributed.ClockDelta import *
from direct.showbase.PythonUtil import Functor
from direct.gui.DirectGui import *
from direct.fsm import FSM
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import TTLocalizer
from toontown.suit import SuitDNA
from toontown.toon import Toon
from toontown.battle import BattleBase
from direct.directutil import Mopath
from direct.showutil import Rope
from toontown.distributed import DelayDelete
from toontown.battle import MovieToonVictory
from toontown.building import ElevatorUtils
from toontown.battle import RewardPanel
from toontown.toon import NPCToons
from direct.task import Task
import random
import math
from toontown.coghq import CogDisguiseGlobals
from toontown.suit import SellbotBossGlobals

class SellbotCutscenes:

    def __init__(self, boss):
        self.boss = boss

    def makeIntroductionMovie(self, delayDeletes):
        track = Parallel()
        camera.reparentTo(render)
        camera.setPosHpr(0, 25, 30, 0, 0, 0)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        dooberTrack = Parallel()
        if self.boss.doobers:
            self.boss.doobersToPromotionPosition(self.boss.doobers[:4], self.boss.battleANode)
            self.boss.doobersToPromotionPosition(self.boss.doobers[4:], self.boss.battleBNode)
            turnPosA = ToontownGlobals.SellbotBossDooberTurnPosA
            turnPosB = ToontownGlobals.SellbotBossDooberTurnPosB
            self.boss.walkDoober(self.boss.doobers[0], 0, turnPosA, dooberTrack, delayDeletes)
            self.boss.walkDoober(self.boss.doobers[1], 4, turnPosA, dooberTrack, delayDeletes)
            self.boss.walkDoober(self.boss.doobers[2], 8, turnPosA, dooberTrack, delayDeletes)
            self.boss.walkDoober(self.boss.doobers[3], 12, turnPosA, dooberTrack, delayDeletes)
            self.boss.walkDoober(self.boss.doobers[7], 2, turnPosB, dooberTrack, delayDeletes)
            self.boss.walkDoober(self.boss.doobers[6], 6, turnPosB, dooberTrack, delayDeletes)
            self.boss.walkDoober(self.boss.doobers[5], 10, turnPosB, dooberTrack, delayDeletes)
            self.boss.walkDoober(self.boss.doobers[4], 14, turnPosB, dooberTrack, delayDeletes)
        toonTrack = Parallel()
        self.boss.toonsToPromotionPosition(self.boss.toonsA, self.boss.battleANode)
        self.boss.toonsToPromotionPosition(self.boss.toonsB, self.boss.battleBNode)
        delay = 0
        for toonId in self.boss.toonsA:
            self.boss.walkToonToPromotion(toonId, delay, self.boss.toonsEnterA, toonTrack, delayDeletes)
            delay += 1

        for toonId in self.boss.toonsB:
            self.boss.walkToonToPromotion(toonId, delay, self.boss.toonsEnterB, toonTrack, delayDeletes)
            delay += 1

        toonTrack.append(Sequence(Wait(delay), self.boss.closeDoors))
        self.boss.rampA.request('extended')
        self.boss.rampB.request('extended')
        self.boss.rampC.request('retracted')
        self.boss.clearChat()
        self.boss.cagedToon.clearChat()
        promoteDoobers = TTLocalizer.BossCogPromoteDoobers % SuitDNA.getDeptFullnameP(self.boss.style.dept)
        doobersAway = TTLocalizer.BossCogDoobersAway[self.boss.style.dept]
        welcomeToons = TTLocalizer.BossCogWelcomeToons
        promoteToons = TTLocalizer.BossCogPromoteToons % SuitDNA.getDeptFullnameP(self.boss.style.dept)
        discoverToons = TTLocalizer.BossCogDiscoverToons
        attackToons = TTLocalizer.BossCogAttackToons
        interruptBoss = TTLocalizer.CagedToonInterruptBoss
        rescueQuery = TTLocalizer.CagedToonRescueQuery
        bossAnimTrack = Sequence(
            ActorInterval(self.boss, 'Ff_speech', startTime=2, duration=10, loop=1),
            ActorInterval(self.boss, 'ltTurn2Wave', duration=2),
            ActorInterval(self.boss, 'wave', duration=4, loop=1),
            ActorInterval(self.boss, 'ltTurn2Wave', startTime=2, endTime=0),
            ActorInterval(self.boss, 'Ff_speech', duration=7, loop=1))
        track.append(bossAnimTrack)
        dialogTrack = Track(
            (0, Parallel(
                camera.posHprInterval(8, Point3(-22, -100, 35), Point3(-10, -13, 0), blendType='easeInOut'),
                IndirectInterval(toonTrack, 0, 18))),
            (5.6, Func(self.boss.setChatAbsolute, promoteDoobers, CFSpeech)),
            (9, IndirectInterval(dooberTrack, 0, 9)),
            (10, Sequence(
                Func(self.boss.clearChat),
                Func(camera.setPosHpr, -23.1, 15.7, 17.2, -160, -2.4, 0))),
            (12, Func(self.boss.setChatAbsolute, doobersAway, CFSpeech)),
            (16, Parallel(
                Func(self.boss.clearChat),
                Func(camera.setPosHpr, -25, -99, 10, -14, 10, 0),
                IndirectInterval(dooberTrack, 14),
                IndirectInterval(toonTrack, 30))),
            (18, Func(self.boss.setChatAbsolute, welcomeToons, CFSpeech)),
            (22, Func(self.boss.setChatAbsolute, promoteToons, CFSpeech)),
            (22.2, Sequence(
                Func(self.boss.cagedToon.nametag3d.setScale, 2),
                Func(self.boss.cagedToon.setChatAbsolute, interruptBoss, CFSpeech),
                ActorInterval(self.boss.cagedToon, 'wave'),
                Func(self.boss.cagedToon.loop, 'neutral'))),
            (25, Sequence(
                Func(self.boss.clearChat),
                Func(self.boss.cagedToon.clearChat),
                Func(camera.setPosHpr, -12, -15, 27, -151, -15, 0),
                ActorInterval(self.boss, 'Ff_lookRt'))),
            (27, Sequence(
                Func(self.boss.cagedToon.setChatAbsolute, rescueQuery, CFSpeech),
                Func(camera.setPosHpr, -12, 48, 94, -26, 20, 0),
                ActorInterval(self.boss.cagedToon, 'wave'),
                Func(self.boss.cagedToon.loop, 'neutral'))),
            (31, Sequence(
                Func(camera.setPosHpr, -20, -35, 10, -88, 25, 0),
                Func(self.boss.setChatAbsolute, discoverToons, CFSpeech),
                Func(self.boss.cagedToon.nametag3d.setScale, 1),
                Func(self.boss.cagedToon.clearChat),
                ActorInterval(self.boss, 'turn2Fb'))),
            (34, Sequence(
                Func(self.boss.clearChat),
                self.boss.loseCogSuits(self.boss.toonsA, self.boss.battleANode, (0, 18, 5, -180, 0, 0)),
                self.boss.loseCogSuits(self.boss.toonsB, self.boss.battleBNode, (0, 18, 5, -180, 0, 0)))),
            (37, Sequence(
                self.boss.toonNormalEyes(self.boss.involvedToons),
                Func(camera.setPosHpr, -23.4, -145.6, 44.0, -10.0, -12.5, 0),
                Func(self.boss.loop, 'Fb_neutral'),
                Func(self.boss.rampA.request, 'retract'),
                Func(self.boss.rampB.request, 'retract'),
                Parallel(self.boss.backupToonsToBattlePosition(self.boss.toonsA, self.boss.battleANode),
                         self.boss.backupToonsToBattlePosition(self.boss.toonsB, self.boss.battleBNode),
                         Sequence(
                             Wait(2),
                             Func(self.boss.setChatAbsolute, attackToons, CFSpeech))))))
        track.append(dialogTrack)
        return Sequence(Func(self.boss.stickToonsToFloor), track, Func(self.boss.unstickToons), name=self.boss.uniqueName('Introduction'))

    def makeRollToBattleTwoMovie(self):
        startPos = Point3(ToontownGlobals.SellbotBossBattleOnePosHpr[0], ToontownGlobals.SellbotBossBattleOnePosHpr[1], ToontownGlobals.SellbotBossBattleOnePosHpr[2])
        if self.boss.arenaSide:
            topRampPos = Point3(*ToontownGlobals.SellbotBossTopRampPosB)
            topRampTurnPos = Point3(*ToontownGlobals.SellbotBossTopRampTurnPosB)
            p3Pos = Point3(*ToontownGlobals.SellbotBossP3PosB)
        else:
            topRampPos = Point3(*ToontownGlobals.SellbotBossTopRampPosA)
            topRampTurnPos = Point3(*ToontownGlobals.SellbotBossTopRampTurnPosA)
            p3Pos = Point3(*ToontownGlobals.SellbotBossP3PosA)
        battlePos = Point3(ToontownGlobals.SellbotBossBattleTwoPosHpr[0], ToontownGlobals.SellbotBossBattleTwoPosHpr[1], ToontownGlobals.SellbotBossBattleTwoPosHpr[2])
        battleHpr = VBase3(ToontownGlobals.SellbotBossBattleTwoPosHpr[3], ToontownGlobals.SellbotBossBattleTwoPosHpr[4], ToontownGlobals.SellbotBossBattleTwoPosHpr[5])
        bossTrack = Sequence()
        bossTrack.append(Func(self.boss.getGeomNode().setH, 180))
        bossTrack.append(Func(self.boss.loop, 'Fb_neutral'))
        track, hpr = self.boss.rollBossToPoint(startPos, None, topRampPos, None, 0)
        bossTrack.append(track)
        track, hpr = self.boss.rollBossToPoint(topRampPos, hpr, topRampTurnPos, None, 0)
        bossTrack.append(track)
        track, hpr = self.boss.rollBossToPoint(topRampTurnPos, hpr, p3Pos, None, 0)
        bossTrack.append(track)
        track, hpr = self.boss.rollBossToPoint(p3Pos, hpr, battlePos, None, 0)
        bossTrack.append(track)
        return Sequence(bossTrack, Func(self.boss.getGeomNode().setH, 0), name=self.boss.uniqueName('BattleTwo'))

    def cagedToonMovieFunction(self, instruct, cageIndex):
        self.boss.notify.debug('cagedToonMovieFunction()')
        if not (hasattr(self.boss, 'cagedToon') and hasattr(self.boss.cagedToon, 'nametag') and hasattr(self.boss.cagedToon, 'nametag3d')):
            return
        if instruct == 1:
            self.boss.cagedToon.nametag3d.setScale(2)
        elif instruct == 2:
            self.boss.cagedToon.setChatAbsolute(TTLocalizer.CagedToonDrop[cageIndex], CFSpeech)
        elif instruct == 3:
            self.boss.cagedToon.nametag3d.setScale(1)
        elif instruct == 4:
            self.boss.cagedToon.clearChat()

    def makeEndOfBattleMovie(self, hasLocalToon):
        name = self.boss.uniqueName('CageDrop')
        seq = Sequence(name=name)
        seq.append(Func(self.boss.cage.setPos, self.boss.cagePos[self.boss.cageIndex]))
        if hasLocalToon:
            seq += [Func(camera.reparentTo, render),
             Func(camera.setPosHpr, self.boss.cage, 0, -50, 0, 0, 0, 0),
             Func(localAvatar.setCameraFov, ToontownGlobals.CogHQCameraFov),
             Func(self.boss.hide)]
        seq += [Wait(0.5),
         Parallel(self.boss.cage.posInterval(1, self.boss.cagePos[self.boss.cageIndex + 1], blendType='easeInOut'), SoundInterval(self.boss.cageLowerSfx, duration=1)),
         Func(self.boss.cagedToonMovieFunction, 1, self.boss.cageIndex),
         Func(self.boss.cagedToonMovieFunction, 2, self.boss.cageIndex),
         Wait(3),
         Func(self.boss.cagedToonMovieFunction, 3, self.boss.cageIndex),
         Func(self.boss.cagedToonMovieFunction, 4, self.boss.cageIndex)]
        if hasLocalToon:
            seq += [Func(self.boss.show),
             Func(camera.reparentTo, localAvatar),
             Func(camera.setPos, localAvatar.cameraPositions[0][0]),
             Func(camera.setHpr, 0, 0, 0)]
        self.boss.cageIndex += 1
        return seq

    def makeBossDamageMovie(self):
        startPos = Point3(ToontownGlobals.SellbotBossBattleTwoPosHpr[0], ToontownGlobals.SellbotBossBattleTwoPosHpr[1], ToontownGlobals.SellbotBossBattleTwoPosHpr[2])
        startHpr = Point3(*ToontownGlobals.SellbotBossBattleThreeHpr)
        bottomPos = Point3(*ToontownGlobals.SellbotBossBottomPos)
        deathPos = Point3(*ToontownGlobals.SellbotBossDeathPos)
        self.boss.setPosHpr(startPos, startHpr)
        bossTrack = Sequence()
        bossTrack.append(Func(self.boss.loop, 'Fb_neutral'))
        track, hpr = self.boss.rollBossToPoint(startPos, startHpr, bottomPos, None, 1)
        bossTrack.append(track)
        track, hpr = self.boss.rollBossToPoint(bottomPos, startHpr, deathPos, None, 1)
        bossTrack.append(track)
        duration = bossTrack.getDuration()
        return bossTrack

    def talkAboutPromotion(self, speech):
        if not self.boss.localToonPromoted:
            pass
        elif self.boss.prevCogSuitLevel < ToontownGlobals.MaxCogSuitLevel:
            speech += TTLocalizer.CagedToonPromotion
            newCogSuitLevel = localAvatar.getCogLevels()[CogDisguiseGlobals.dept2deptIndex(self.boss.style.dept)]
            if newCogSuitLevel == ToontownGlobals.MaxCogSuitLevel:
                speech += TTLocalizer.CagedToonLastPromotion % (ToontownGlobals.MaxCogSuitLevel + 1)
            if newCogSuitLevel in ToontownGlobals.CogSuitHPLevels:
                speech += TTLocalizer.CagedToonHPBoost
        else:
            speech += TTLocalizer.CagedToonMaxed % (ToontownGlobals.MaxCogSuitLevel + 1)
        return speech

    def makeCageOpenMovie(self):
        speech = TTLocalizer.CagedToonThankYou
        speech = self.boss.talkAboutPromotion(speech)
        name = self.boss.uniqueName('CageOpen')
        seq = Sequence(
            Func(self.boss.cage.setPos, self.boss.cagePos[4]),
            Func(self.boss.cageDoor.setHpr, VBase3(0, 0, 0)),
            Func(self.boss.cagedToon.setPos, Point3(0, -2, 0)),
            Parallel(
                self.boss.cage.posInterval(0.5, self.boss.cagePos[5], blendType='easeOut'),
                SoundInterval(self.boss.cageLowerSfx, duration=0.5)),
            Parallel(
                self.boss.cageDoor.hprInterval(0.5, VBase3(0, 90, 0), blendType='easeOut'),
                Sequence(SoundInterval(self.boss.cageDoorSfx), duration=0)),
            Wait(0.2),
            Func(self.boss.cagedToon.loop, 'walk'),
            self.boss.cagedToon.posInterval(0.8, Point3(0, -6, 0)),
            Func(self.boss.cagedToon.setChatAbsolute, TTLocalizer.CagedToonYippee, CFSpeech),
            ActorInterval(self.boss.cagedToon, 'jump'),
            Func(self.boss.cagedToon.loop, 'neutral'),
            Func(self.boss.cagedToon.headsUp, localAvatar),
            Func(self.boss.cagedToon.setLocalPageChat, speech, 0),
            Func(camera.reparentTo, localAvatar),
            Func(camera.setPos, 0, -9, 9),
            Func(camera.lookAt, self.boss.cagedToon, Point3(0, 0, 2)), name=name)
        return seq