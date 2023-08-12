# stdlib
from pprint import pprint
from typing import List, Dict, Union
from sys import exit
import json
# custom modules
from toolchain.utils import *
# 3rd party
try:
  from yaml import safe_load, YAMLError
  from discord import Interaction
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


#───Globals──────────────────
colors = {
  'purple'     : {'x':0.2682, 'y':0.1334},
  'soft-white' : {'x':0.4475, 'y':0.4076}
}


#───Commands─────────────────
def lv_logic(rid:str, dictation:str) -> str:
  '''TODO.'''

  args = dictation.split(' ')
  if '' in args:
    args = args.remove('')

  ## no args :: toggle
  if not args:
    toggleGroupedLight(rid)
    state = json.loads(getGroupedLight(rid))['data'][0]['on']['on']
    state = 'on' if state else 'off'
    return_message = f'living room `{state}`'

  ## 1 arg :: brightness or color
  elif len(args) == 1:
    print(args)
    # brightness
    if args[0].isnumeric():
      brightness = int(args[0])
      brightness = boundBrightness(brightness)
      setRoomBrightness(rid, brightness)
      return_message = f'living room `{brightness}%`'
    # color
    elif args[0] in colors:
      color = colors[args[0].lower()]
      setRoomColor(rid, color)
      return_message = f'living room `{args[0]}`'
    else:
      return_message = f'Unsupported dictation: {args[0]}'
 
  ## 2 args :: brightness and color
  elif len(args) == 2:
    if not bool(set(args) & set(colors)) and (args[0].isnumeric() or args[1].isnumeric()):
      return_message = f'Unsupported dictation: {args.join(", ")}'
    elif args[0] not in colors:
       brightness, color = int(args[0]), colors[args[1]]
    else:
      color, brightness = colors[args[0]], int(args[1])
    brightness = boundBrightness(brightness)
    setRoomBrightnessColor(rid, brightness, color)
    return_message = f'living room `{args[0]} {args[1]}`'
    
  ## >3 args :: too many
  else:
    return_message = f'Unsupported dictation: too many arguments'

  return return_message
