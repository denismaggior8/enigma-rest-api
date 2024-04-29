from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models.enigma_I_models import EnigmaIRequest, EnigmaIResponse
from enigmapython.PlugboardPassthrough import PlugboardPassthrough
from enigmapython.Utils import Utils
from enigmapython.Rotor import Rotor
from enigmapython.EtwPassthrough import EtwPassthrough
from enigmapython.EnigmaI import EnigmaI
from enigmapython.EnigmaIRotorI import EnigmaIRotorI

import app.config

root_path = "enigma-api"
api_version = "v1"

router = APIRouter(
            prefix="/{root_path}/{api_version}/enigma/I".format(root_path = root_path, api_version = api_version)
        )


@router.post("/encrypt")
async def encrypt(request: EnigmaIRequest) -> EnigmaIResponse:
    plugboard = PlugboardPassthrough()
    rotor1Class = Utils.get_class_instance(Rotor.lookup["I_"+request.rotors[0].type].__module__+"."+Rotor.lookup["I_"+request.rotors[0].type].__name__)
    rotor2Class = Utils.get_class_instance(Rotor.lookup["I_"+request.rotors[1].type].__module__+"."+Rotor.lookup["I_"+request.rotors[1].type].__name__)
    rotor3Class = Utils.get_class_instance(Rotor.lookup["I_"+request.rotors[2].type].__module__+"."+Rotor.lookup["I_"+request.rotors[2].type].__name__)
    reflectorClass = Utils.get_class_instance(Rotor.lookup[request.reflector].__module__+"."+Rotor.lookup[request.reflector].__name__)
    etw = EtwPassthrough()
    enigma = EnigmaI(plugboard, rotor3Class(position=request.rotors[0].position,ring=request.rotors[0].ring), rotor2Class(position=request.rotors[1].position,ring=request.rotors[1].ring), rotor1Class(position=request.rotors[2].position,ring=request.rotors[2].ring), reflectorClass(), etw, True)
    return EnigmaIResponse(cyphertext=enigma.input_string(request.cleartext.lower()).upper())
