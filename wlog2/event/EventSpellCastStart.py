
from ..types import EventType

from ..EventParser import EventParser

from .AEventBaseSpell import AEventBaseSpell

class EventSpellCastStart(AEventBaseSpell):
    def __init__(self, time, parser: EventParser):
        AEventBaseSpell.__init__(self, time, EventType.SPELL_CAST_START, parser)
