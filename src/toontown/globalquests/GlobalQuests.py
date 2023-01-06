from otp.otpbase import OTPGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import ToontownGlobals
from toontown.battle import SuitBattleGlobals
from toontown.coghq import CogDisguiseGlobals
import random
from toontown.toon import NPCToons
import copy, string
from toontown.hood import ZoneUtil
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
import time, types, random

GLOBAL_QUEST_COGS = 0
GLOBAL_QUEST_COGS_DEPARTMENT = 1
GLOBAL_QUEST_COGS_SPECIFIC = 2

GlobalQuestDict = {}