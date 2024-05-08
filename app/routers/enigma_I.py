from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models.enigma_I_models import EnigmaIRequest, EnigmaIResponse, RequestRotorConfig, ResponseRotorConfig
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
    #request.rotors.reverse()
    #for i in range(len(request.rotors)):
    for index,rotorConfig in enumerate(request.rotors):
        print(rotorConfig)
        rotor = Rotor.get_instance_from_tag("I_"+rotorConfig.type)
        rotor.position = rotorConfig.position
        rotor.ring = rotorConfig.ring
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

    cypher_text = enigma.input_string(request.cleartext.lower()).upper()

    new_rotors : ResponseRotorConfig = []
    
    for index,rotorConfig in enumerate(rotors):
        responseRotorConfig = ResponseRotorConfig(position=enigma.rotors[index].position,ring=enigma.rotors[index].ring)
        new_rotors.append(responseRotorConfig)
    new_rotors.reverse()

    return EnigmaIResponse(cyphertext=cypher_text,rotors=new_rotors)
