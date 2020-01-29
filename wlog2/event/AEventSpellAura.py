
from ..types import EventType
from ..types import getAuraTypeName
from ..encode import *

from ..EventParser import EventParser

from .AEventBaseSpell import AEventBaseSpell

class AEventSpellAura(AEventBaseSpell):
    def __init__(self, time, eventType, parser):
        assert(
            eventType == EventType.SPELL_AURA_APPLIED or \
            eventType == EventType.SPELL_AURA_REMOVED or \
            eventType == EventType.SPELL_AURA_APPLIED_DOSE or \
            eventType == EventType.SPELL_AURA_REMOVED_DOSE or \
            eventType == EventType.SPELL_AURA_REFRESH
        )
        AEventBaseSpell.__init__(self, time, eventType, parser)
        
        if isinstance(parser, EventParser):
            self.auraType = parser.getAuraType()
            if self.eventType == EventType.SPELL_AURA_APPLIED_DOSE or \
               self.eventType == EventType.SPELL_AURA_REMOVED_DOSE:
                self.amount = parser.getInt()
            
        elif isinstance(parser, Decoder):
            self.decode(decode)
        else:
            ValueError('Parser not supported: ' + type(parser))

    def decode(self, decoder: Decoder):
        self.auraType = decoder.auraType()
        if self.eventType == EventType.SPELL_AURA_APPLIED_DOSE or \
           self.eventType == EventType.SPELL_AURA_REMOVED_DOSE:
            self.amount = decoder.integer(size=SizeType.AURA_AMOUNT)

    def encode(self, encoder: Encoder) -> bytes:
        if self.eventType == EventType.SPELL_AURA_APPLIED_DOSE or \
           self.eventType == EventType.SPELL_AURA_REMOVED_DOSE:
            return AEventBaseSpell.encode(self, encoder: Encoder) + \
                   encoder.auraType(self.auraType) + \
                   encoder.integer(self.amount, size=SizeType.AURA_AMOUNT)
        else:
            return AEventBaseSpell.encode(self, encoder: Encoder) + \
                   encoder.auraType(self.auraType)

    def __str__(self):
        if self.eventType == EventType.SPELL_AURA_APPLIED_DOSE or \
           self.eventType == EventType.SPELL_AURA_REMOVED_DOSE:
            return AEventBaseSpell.__str__(self) + ',{0:s},{1:d}'.format(
                getAuraTypeName(self.auraType),
                self.amount
            )
        else:
            return AEventBaseSpell.__str__(self) + ',{0:s}'.format(
                getAuraTypeName(self.auraType)
            )

    def __eq__(self, other):
        if not AEventBaseSpell.__eq__(other):
            return False
        if self.amount != other.amount:
            return False
        if self.eventType == EventType.SPELL_AURA_APPLIED_DOSE or \
           self.eventType == EventType.SPELL_AURA_REMOVED_DOSE:
            return self.auraType == other.auraType
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

