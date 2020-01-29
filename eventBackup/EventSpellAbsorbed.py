from .AEvent import string
from ..EventType import EventType
from .AEventBase import AEventBase
from ..EventParser import EventParser
from wlog.GUID import GUID
from ..Encode import SizeType

# BASE,                          Player-4701-0094E8DE,"Beemo-Mograine",0x514,0x0, 10193,"Mana Shield",0x40, 570,1593
# BASE, 21333,"Lava Breath",0x4, Player-4701-00B48D7F,"Qopy-Mograine",0x511,0x0,  13033,"Ice Barrier",0x10, 524,722

class EventSpellAbsorbed(AEventBase):
    def __init__(self, time, parser: EventParser):
        AEventBase.__init__(self, time, EventType.SPELL_ABSORBED, parser)

        value = parser.readValue()
        try:
            self.extraGUID = GUID(value)
            self.hasBaseSpell = False
        except ValueError:
            self.spellId = int(value)
            self.spellName = parser.getString()
            self.spellSchool = parser.getInt(base=16)
            self.extraGUID = parser.getGUID()
            self.hasBaseSpell = True

        self.extraName = parser.getString()
        self.extraFlags = parser.getInt(base=16)
        self.extraRaidFlags = parser.getInt(base=16)
        self.extraSpellId = parser.getInt()
        self.extraSpellName = parser.getString()
        self.extraSpellSchool = parser.getInt(base=16)
        self.amount = parser.getInt()
        self.p5 = parser.getInt()

    def encode(self, encoder) -> bytes:
        code = AEventBase.encode(encoder)
        if self.hasBaseSpell:
            code += encoder.spell(self.spellId, self.spellName, self.spellSchool)
        return code + \
               encoder.entity(self.extraGUID, self.extraName, self.extraFlags, self.extraRaidFlags) + \
               encoder.spell(self.extraSpellId, self.extraSpellName, self.extraSpellSchool) + \
               encoder.integer(self.amount, size=SizeType.SPELL_ABSORBED_AMOUNT) + \
               encoder.integer(self.p5, size=SizeType.SPELL_ABSORBED_P5)

    def __str__(self):
        if self.hasBaseSpell:
            return AEventBase.__str__(self) + \
                ',{0:d},{1:s},{2:#x},{3:s},{4:s},{5:#x},{6:#x},{7:d},{8:s},{9:#x},{10:d},{11:d}'.format(
                    self.spellId,
                    string(self.spellName),
                    self.spellSchool,
                    str(self.extraGUID),
                    string(self.extraName),
                    self.extraFlags,
                    self.extraRaidFlags,
                    self.extraSpellId,
                    string(self.extraSpellName),
                    self.extraSpellSchool,
                    self.amount,
                    self.p5
                )
        else:
            return AEventBase.__str__(self) + ',{0:s},{1:s},{2:#x},{3:#x},{4:d},{5:s},{6:#x},{7:d},{8:d}'.format(
                str(self.extraGUID),
                string(self.extraName),
                self.extraFlags,
                self.extraRaidFlags,
                self.extraSpellId,
                string(self.extraSpellName),
                self.extraSpellSchool,
                self.amount,
                self.p5
            )

    def __eq__(self, other):
        if self.hasBaseSpell and ( \
           not other.hasBaseSpell or \
           self.spellId != other.spellId):
            return False
        return AEventBase.__eq__(other)          and \
               self.extraGUID == other.extraGUID and \
               self.spellId == other.spellId     and \
               self.amount == other.amount       and \
               self.p5 == other.p5

    def __ne__(self, other):
        return not self.__eq__(other)

