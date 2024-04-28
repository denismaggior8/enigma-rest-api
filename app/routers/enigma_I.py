from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models import EnigmaIConfig
from EnigmaIRotorI import EnigmaIRotorI
from EnigmaIRotorII import EnigmaIRotorII
from EnigmaIRotorIII import EnigmaIRotorIII
from PlugboardPassthrough import PlugboardPassthrough
from ReflectorUKWA import ReflectorUKWA
from EtwPassthrough import EtwPassthrough
from EnigmaI import EnigmaI



router = APIRouter()


root_path = "api"
api_version = "v1"

@router.post("/{root_path}/{api_version}/enigma/I/encrypt".format(root_path = root_path, api_version = api_version))
async def update_item(config: EnigmaIConfig):
    plugboard = PlugboardPassthrough()
    rotor1 = EnigmaIRotorI(0)
    rotor2 = EnigmaIRotorI(0)
    rotor3 = EnigmaIRotorI(0)
    reflector = ReflectorUKWA()
    etw = EtwPassthrough()
    enigma = EnigmaI(plugboard, rotor3, rotor2, rotor1, reflector, etw, True)
    my_encrypted_string = enigma.input_string(config.cleartext.lower())
    return my_encrypted_string.upper()