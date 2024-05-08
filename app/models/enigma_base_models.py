from pydantic import BaseModel, Field, constr, validator, ConfigDict
from typing import Optional
from typing import List
from typing import Dict
from typing import Union, Annotated
from typing_extensions import TypedDict

allowed_chars_regex = r"^[A-Z]+$"


class RequestRotorConfig (BaseModel):
    position: int = Field(ge=0, le=25, default=0)
    ring: int = Field(ge=0, le=25, default=0)

class ResponseRotorConfig (BaseModel):
    position: int = Field(ge=0, le=25, default=0)

class PlugboardWiring(BaseModel):
    from_letter: str = Field(regex=allowed_chars_regex, min_length=1, max_length=1)
    to_letter: str = Field(regex=allowed_chars_regex, min_length=1, max_length=1)

class Plugboard (BaseModel):
    wirings: List[PlugboardWiring] = Field(max_items=10)

class EnigmaBaseRequest (BaseModel):
    plugboard: Optional[Plugboard]
    auto_increment_rotors: bool = Field(default=True)
    cleartext: str = Field(regex=allowed_chars_regex, min_length=1, max_length=128)

class EnigmaBaseResponse (BaseModel):
    cyphertext: str
    rotors: List[ResponseRotorConfig]