from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models.enigma_I_models import EnigmaIRequest, EnigmaIResponse
from enigmapython.SwappablePlugboard import SwappablePlugboard
from enigmapython.Rotor import Rotor 
from enigmapython.Reflector import Reflector
from enigmapython.EtwPassthrough import EtwPassthrough
from enigmapython.Enigma import Enigma


import app.config

root_path = "enigma-api"
api_version = "v1"

router = APIRouter(prefix="/{root_path}/{api_version}/enigma".format(root_path = root_path, api_version = api_version))


@router.post("/{model}/encrypt")
async def encrypt(model: str, request: EnigmaIRequest) -> EnigmaIResponse:
    

    rotors = []
    for i in range(len(request.rotors)):
        rotor = Rotor.get_instance_from_tag("I_"+request.rotors[i].type)
        rotor.position = request.rotors[i].position
        rotor.ring = request.rotors[i].ring
        rotors.append(rotor)
    rotors.reverse()
    
    reflector = Reflector.get_instance_from_tag(request.reflector)

    etw = EtwPassthrough()

    plugboard = SwappablePlugboard()   
    for plugboard_wiring in request.plugboard.wirings:
        plugboard.swap(plugboard_wiring.from_letter.lower(),plugboard_wiring.to_letter.lower())

    enigma = Enigma(
        plugboard = plugboard,
        rotors = rotors,
        reflector = reflector,
        etw = etw,
        auto_increment_rotors = request.auto_increment_rotors
        )

    return EnigmaIResponse(cyphertext=enigma.input_string(request.cleartext.lower()).upper())
