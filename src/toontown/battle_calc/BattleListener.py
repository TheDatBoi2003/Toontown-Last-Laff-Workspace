from direct.showbase.DirectObject import DirectObject

class BattleListener(DirectObject):

    def __init__(self, battle):
        DirectObject.__init__(self)
        self.suitAttacks = []
        self.battle = battle
        self.Id = battle.doId