from ..EventType import EventType
from .AEventBase import AEventBase
from .AEventAdvanced import AEventAdvanced
from .A2EventDamage import A2EventDamage
from ..EventParser import EventParser
from ..EnvironmentalType import getEnvironmentalTypeName

class EventEnvironmentalDamage(AEventAdvanced, A2EventDamage):
    def __init__(self, time, parser: EventParser):
        AEventBase.__init__(self, time, EventType.ENVIRONMENTAL_DAMAGE, parser)
        AEventAdvanced.__init__(self, parser)
        self.environmentalType = parser.getEnvironmentalType()
        A2EventDamage.__init__(self, EventType.ENVIRONMENTAL_DAMAGE, parser)

    def encode(self, encoder) -> bytes:
        return AEventBase.encode(encoder) + \
               AEventAdvanced.encode(encoder) + \
               encoder.environmentalType(self.environmentalType) + \
               A2EventDamage.encode(encoder)

    def __str__(self):
        return AEventBase.__str__(self) + AEventAdvanced.__str__(self) + ',{0:s}'.format(
            getEnvironmentalTypeName(self.environmentalType)
        ) + A2EventDamage.__str__(self)

    def __eq__(self, other):
        return AEventAdvanced.__eq__(other) and \
               A2EventDamage.__eq__(other) and \
               self.environmentalType == other.environmentalType
        
    def __ne__(self, other):
        return not self.__eq__(other)

