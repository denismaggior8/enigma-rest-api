from pydantic import BaseModel, Field
from typing import Optional
from typing import List

class RotorConfig (BaseModel):
    position: int
    ring: int

class Rotors (BaseModel):
    List[RotorConfig] 

class EnigmaBaseRequest (BaseModel):
    cleartext: str = Field(pattern=r'^[A-Z]+$', max_length=128)

class EnigmaBaseResponse (BaseModel):
    cyphertext: str