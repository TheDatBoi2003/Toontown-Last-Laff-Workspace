from direct.directnotify import DirectNotifyGlobal
import GlobalQuests
import random

class GlobalQuestManagerAI:

    notify = DirectNotifyGlobal.directNotify.newCategory('GlobalQuestManagerAI')

    def __init__(self, air):
        self.air = air
        self.globalQuestDict = {}

    def toonContributed(self, questType, ammount):
        quests = self.globalQuestDict
        for questId in quests:
            quest = quests[questId]
            if quest['active'] == 1 and quest['type'] == questType:
                quest['ammount'] -= ammount
                if quest['ammount'] <= 0:
                    quest['active'] = 0
                    self.notify.info('Quest %s completed!' % questId)
                    self.air.newsManager.sendUpdate('sendSystemMessage', [quest['shoutOutMessage'], 1])

    def addGlobalQuest(self, questType, ammount):
        quest = {'type': questType,
                 'ammount': ammount,
                 'active': 1,
                 'shoutOutMessage': 'The Toons have defeated %s Cogs!' % ammount}
        self.globalQuestDict[0] = quest

    def addRandomGlobalQuest(self):
        ammount = random.randint(2, 30)
        quest = {'type': 0,
                 'ammount': ammount,
                 'active': 1,
                 'shoutOutMessage': 'The Toons have defeated %s Cogs!' % ammount}
        self.globalQuestDict[0] = quest
    
    def sendGlobalQuestMessage(self):
        from toontown.globalquests import GlobalQuests
        global_quests = self.globalQuestDict
        for questId in global_quests:
            quest = global_quests[questId]
            if quest['active']:
                if quest['type'] == 0:
                    self.air.newsManager.sendUpdate('sendSystemMessage', [("A global Toontask is in progress! Defeat %s Cogs!" % quest['ammount']), 1])