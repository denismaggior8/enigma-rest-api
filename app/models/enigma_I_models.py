from pydantic import BaseModel, Field
from .enigma_base_models import *
from enum import Enum

class EnigmaIRotorsEnum(str, Enum):
    rotor_I = 'I'
    rotor_II = 'II'
    rotor_III = 'III'

class EnigmaIReflectorsEnum(str, Enum):
    reflector_A = 'A'
    reflector_B = 'B'
    reflector_C = 'C'

class EnigmaIRotorConfig (RotorConfig):
    type: EnigmaIRotorsEnum

class EnigmaIReflectorConfig (ReflectorConfig):
    type: EnigmaIReflectorsEnum

class EnigmaIRequest(EnigmaBaseRequest):
    rotors: List[EnigmaIRotorConfig] = Field(min_items=3, max_items=3)
    reflector: Optional[EnigmaIReflectorConfig]
     
class EnigmaIResponse(EnigmaBaseResponse):
    pass