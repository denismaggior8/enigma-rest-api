from pydantic import BaseModel, Field
from enum import Enum

class EnigmaIRotorsEnum(str, Enum):
    rotor_I = 'I'
    rotor_II = 'II'
    rotor_III = 'III'

class EnigmaIConfig(BaseModel):
    rotor1: EnigmaIRotorsEnum
    rotor2: EnigmaIRotorsEnum
    rotor3: EnigmaIRotorsEnum
    cleartext: str = Field(pattern=r'^[A-Z]+$', max_length=512)  