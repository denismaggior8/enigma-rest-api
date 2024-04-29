from pydantic import BaseModel, Field
from .enigma_base_models import *
from enum import Enum

class EnigmaIRotorsEnum(str, Enum):
    rotor_I = 'I'
    rotor_II = 'II'
    rotor_III = 'III'

class EnigmaIRotorConfig (RotorConfig):
    type: EnigmaIRotorsEnum

class EnigmaIRequest(EnigmaBaseRequest):
    rotors: List[EnigmaIRotorConfig] = Field(min_items=3, max_items=3)
     
class EnigmaIResponse(EnigmaBaseResponse):
    pass