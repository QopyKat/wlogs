
from ..types import EventType

from ..EventParser import EventParser

from .A2EventDamage import A2EventDamage
from .AEventAdvancedSpell import AEventAdvancedSpell

class EventDamageSplit(AEventAdvancedSpell, A2EventDamage):
    def __init__(self, time, parser: EventParser):
        AEventAdvancedSpell.__init__(self, time, EventType.DAMAGE_SPLIT, parser)
        A2EventDamage.__init__(self, EventType.DAMAGE_SPLIT, parser)

    def encode(self, encoder) -> bytes:
        return AEventAdvancedSpell.encode(self, encoder) + A2EventDamage.encode(self, encoder)

    def __str__(self):
        return AEventAdvancedSpell.__str__(self) + A2EventDamage.__str__(self)

    def __eq__(self, other):
        return AEventAdvancedSpell.__eq__(other) and A2EventDamage.__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)