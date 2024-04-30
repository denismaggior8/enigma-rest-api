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
    plugboard = SwappablePlugboard()

    rotor1 = Rotor.get_instance_from_tag("I_"+request.rotors[0].type)
    rotor1.position = request.rotors[0].position
    rotor1.ring = request.rotors[0].ring

    rotor2 = Rotor.get_instance_from_tag("I_"+request.rotors[1].type)
    rotor2.position = request.rotors[1].position
    rotor2.ring = request.rotors[1].ring

    rotor3 = Rotor.get_instance_from_tag("I_"+request.rotors[2].type)
    rotor3.position = request.rotors[2].position
    rotor3.ring = request.rotors[2].ring
    
    reflector = Reflector.get_instance_from_tag(request.reflector)

    etw = EtwPassthrough()

    enigma = Enigma(
        plugboard = plugboard,
        rotors = [rotor3,rotor2,rotor1],
        reflector = reflector,
        etw = etw,
        auto_increment_rotors = request.auto_increment_rotors
        )
    
    for plugboard_wiring in request.plugboard.wirings:
        plugboard.swap(plugboard_wiring.from_letter.lower(),plugboard_wiring.to_letter.lower())
    
    return EnigmaIResponse(cyphertext=enigma.input_string(request.cleartext.lower()).upper())
