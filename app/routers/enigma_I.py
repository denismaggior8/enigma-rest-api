from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models.enigma_I_models import EnigmaIRequest, EnigmaIResponse
from EnigmaIRotorI import EnigmaIRotorI
from EnigmaIRotorII import EnigmaIRotorII
from EnigmaIRotorIII import EnigmaIRotorIII
from PlugboardPassthrough import PlugboardPassthrough
from ReflectorUKWA import ReflectorUKWA
from EtwPassthrough import EtwPassthrough
from EnigmaI import EnigmaI

root_path = "enigma-api"
api_version = "v1"

router = APIRouter(
            prefix="/{root_path}/{api_version}/enigma/I".format(root_path = root_path, api_version = api_version)
        )


@router.post("/encrypt")
async def encrypt(request: EnigmaIRequest) -> EnigmaIResponse:
    plugboard = PlugboardPassthrough()
    rotor1 = EnigmaIRotorI(0)
    rotor2 = EnigmaIRotorI(0)
    rotor3 = EnigmaIRotorI(0)
    reflector = ReflectorUKWA()
    etw = EtwPassthrough()
    enigma = EnigmaI(plugboard, rotor3, rotor2, rotor1, reflector, etw, True)
    return EnigmaIResponse(cyphertext=enigma.input_string(request.cleartext.lower()).upper())
