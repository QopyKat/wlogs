from abc import ABC
from abc import abstractmethod

from ..types import GUIDType

# For players: Player-[server ID]-[player UID] (Example: "Player-970-0002FD64")
# For Unit Type Names: [Unit type]-0-[server ID]-[instance ID]-[zone UID]-[ID]-[spawn UID] 
#   Unit Type Names: "Creature", "Pet", "GameObject", "Vehicle", and "Vignette"
#   (Example: "Creature-0-970-0-11-31146-000136DF91")
# For items: Item-[server ID]-0-[spawn UID] (Example: "Item-970-0-400000076620BFF4")
#   (Please note that this tells you nothing useful about the item, like the ID)


class AGUID(ABC):
    def __init__(self, guidType: GUIDType):
        self.guidType = guidType

    @abstractmethod
    def encode(self, encoder):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __eq__(self, other):
        return self.guidType == other.guidType

    def __ne__(self, other):
        return self.guidType != other.guidType

