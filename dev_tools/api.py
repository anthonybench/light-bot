#!/usr/bin/env python

'''README
Usage:
  ./dev_tools/api.py <input>

  <input>
  # primitives
    get-lights
    get-rooms
    get-devices
    get-light
    get-grouped-light
    get-room
    light-on-off
    grouped-light-on-off
    set-light-brightness-color
    set-grouped-light-brightness-color
    set-grouped-light-brightness
    set-grouped-light-color
  # composites
    toggle-light
    toggle-room
    set-room-brightness-color

Requirements:
  - get hue bridge ip address (see references)
  - generate api user (see official docs)

Overview:
  primitives :: (utils) a single endpoint
  composites :: (commands) an assembly of primitives to support an end-user use-case

References:
  - https://discovery.meethue.com
  - https://developers.meethue.com/develop/hue-api-v2/getting-started/
'''

from subprocess import call, check_output
from pprint import pprint
from sys import argv, exit
import json
from typing import List, Dict
from primitives import *


#───Parameters───────────────
command = argv[1]
# test vals
grouped_light_rid    = '62e73f1a-9a45-43c1-b0f1-c5284aa77f98'
individual_light_rid = '429414b6-1fdb-4627-8ec8-da13b36f8470'
room_rid             = 'f511fdfe-66c0-4939-aa3c-2e46a97d7373'
brightness           = 100
color                = 'soft-white'
on_off               = False
write_output = False # dev_tools/output.json


#───Globals──────────────────
colors = {
  'purple'     : {'x':0.2682, 'y':0.1334},
  'soft-white' : {'x':0.4475, 'y':0.4076}
}


#───Composites───────────────
def toggleLight(rid:str) -> str:
  state = json.loads(getLight(rid))['data'][0]['on']['on']
  lightOnOff(rid, not state) 

def toggleRoom(rid:str) -> str:
  state = json.loads(getGroupedLight(rid))['data'][0]['on']['on']
  groupedLightOnOff(rid, not state) 

def setRoomBrightnessColor(rid:str, brightness:int, color:Dict[str,float]) -> str:
  groupedLightOnOff(rid, True)
  setGroupedLightBrightnessColor(rid, brightness, color)
  return f

def setRoomBrightness(rid:str, brightness:int) -> str:
  groupedLightOnOff(rid, True)
  setGroupedLightBrightness(rid, brightness)

def setRoomColor(rid:str, color:Dict[str,float]) -> str:
  groupedLightOnOff(rid, True)
  setGroupedLightColor(rid, color)


#───Exec─────────────────────
if command == 'get-lights':
  res = getLights()
elif command == 'get-rooms':
  res = getRooms()
elif command == 'get-devices':
  res = getDevices()
elif command == 'get-light':
  res = getLight(individual_light_rid)
elif command == 'get-grouped-light':
  res = getGroupedLight(grouped_light_rid)
elif command == 'get-room':
  res = getRoom(room_rid)
elif command == 'light-on-off':
  res = lightOnOff(individual_light_rid, on_off)
elif command == 'grouped-light-on-off':
  res = groupedLightOnOff(grouped_light_rid, on_off)
elif command == 'toggle-light': # composite
  res = toggleLight(individual_light_rid)
elif command == 'toggle-room': # composite
  res = toggleRoom(grouped_light_rid)
elif command == 'set-light-brightness-color':
  res = setLightBrightnessColor(individual_light_rid, brightness, colors[color])
elif command == 'set-grouped-light-brightness-color':
  res = setGroupedLightBrightnessColor(grouped_light_rid, brightness, colors[color])
elif command == 'set-room-brightness-color': # composite
  res = setRoomBrightnessColor(grouped_light_rid, brightness, colors[color])
elif command == 'set-grouped-light-brightness':
  res = setGroupedLightBrightness(grouped_light_rid, brightness)
elif command == 'set-grouped-light-color':
  res = setGroupedLightColor(grouped_light_rid, colors[color])
elif command == 'set-room-brightness': # composite
  res = setRoomBrightness(grouped_light_rid, brightness)
elif command == 'set-room-color': # composite
  res = setRoomColor(grouped_light_rid, colors[color])
else:
  print(f'Error. Command no recognized')
  exit(1)

if write_output:
  with open('dev_tools/output.json', 'w') as o:
    o.write(res)
  call('cd dev_tools; prettier -w output.json', shell=True, executable='/bin/zsh')
