from panda3d.core import *
from toontown.coghq import DistributedHealBarrelAI
from toontown.coghq import DistributedGagBarrelAI
PieToonup = [5, 4, 3, 2, 1]
PieToonupNerfed = [10, 8, 6, 4, 2]
PieDamageMult = 1.0
PieDamageMultNerfed = 2.0
AttackMult = [1.0, 1.2, 1.4, 1.6, 1.8]
AttackMultNerfed = 0.5
VPMaxDamage = [3000, 3500, 4000, 4500, 5000]
HitCountDamage = [60, 55, 50, 40, 35]
HitCountDamageNerfed = 50
BarrelDefs = {8000: {'type': DistributedHealBarrelAI.DistributedHealBarrelAI,
        'pos': Point3(15, 23, 0),
        'hpr': Vec3(-45, 0, 0),
        'rewardPerGrab': 50,
        'rewardPerGrabMax': 0},
 8001: {'type': DistributedGagBarrelAI.DistributedGagBarrelAI,
        'pos': Point3(15, -23, 0),
        'hpr': Vec3(-135, 0, 0),
        'gagLevel': 3,
        'gagLevelMax': 0,
        'gagTrack': 3,
        'rewardPerGrab': 10,
        'rewardPerGrabMax': 0},
 8002: {'type': DistributedGagBarrelAI.DistributedGagBarrelAI,
        'pos': Point3(21, 20, 0),
        'hpr': Vec3(-45, 0, 0),
        'gagLevel': 3,
        'gagLevelMax': 0,
        'gagTrack': 4,
        'rewardPerGrab': 10,
        'rewardPerGrabMax': 0},
 8003: {'type': DistributedGagBarrelAI.DistributedGagBarrelAI,
        'pos': Point3(21, -20, 0),
        'hpr': Vec3(-135, 0, 0),
        'gagLevel': 3,
        'gagLevelMax': 0,
        'gagTrack': 5,
        'rewardPerGrab': 10,
        'rewardPerGrabMax': 0}}

def setBarrelAttr(barrel, entId):
    for defAttr, defValue in BarrelDefs[entId].iteritems():
        setattr(barrel, defAttr, defValue)


BarrelsStartPos = (0, -36, -8)
BarrelsFinalPos = (0, -36, 0)
