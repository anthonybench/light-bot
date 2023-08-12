from subprocess import call, check_output
from pprint import pprint
from sys import argv, exit
import json
from typing import List, Dict
from yaml import safe_load, YAMLError
from pprint import pprint


with open('config.yml') as raw_config:
  config = safe_load(raw_config)
  username   = config['username']
  client_key = config['client_key']
  bridge_ip  = config['bridge_ip']


def getLights() -> str:
  request = f''' \
    curl --insecure \
      -X GET "https://{bridge_ip}/clip/v2/resource/light" \
      -H "hue-application-key: {username}" \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  print(f'Item Count: {len(json.loads(output_str)["data"])}')
  return output_str


def getRooms() -> str:
  request = f''' \
    curl --insecure \
      -X GET "https://{bridge_ip}/clip/v2/resource/room" \
      -H "hue-application-key: {username}" \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  print(f'Item Count: {len(json.loads(output_str)["data"])}')
  return output_str


def getDevices() -> str:
  request = f''' \
    curl --insecure \
      -X GET "https://{bridge_ip}/clip/v2/resource/device" \
      -H "hue-application-key: {username}" \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  print(f'Item Count: {len(json.loads(output_str)["data"])}')
  return output_str


def getLight(rid:str) -> str:
  request = f''' \
    curl --insecure \
      -X GET "https://{bridge_ip}/clip/v2/resource/light/{rid}" \
      -H "hue-application-key: {username}" \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str


def getGroupedLight(rid:str) -> str:
  request = f''' \
    curl --insecure \
      -X GET "https://{bridge_ip}/clip/v2/resource/grouped_light/{rid}" \
      -H "hue-application-key: {username}" \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str


def getRoom(rid:str) -> str:
  request = f''' \
    curl --insecure \
      -X GET "https://{bridge_ip}/clip/v2/resource/room/{rid}" \
      -H "hue-application-key: {username}" \
  '''
  request = request.replace('<rid>', rid)
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str


def lightOnOff(rid:str, on_off:bool) -> str:
  inject = 'true' if on_off else 'false'
  request = f''' \
    curl --insecure \
      -X PUT "https://{bridge_ip}/clip/v2/resource/light/{rid}" \
      -H "hue-application-key: {username}" \
      -d '{{"on":{{"on":{inject}}}}}' \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str


def groupedLightOnOff(rid:str, on_off:bool) -> str:
  inject = 'true' if on_off else 'false'
  request = f''' \
    curl --insecure \
      -X PUT "https://{bridge_ip}/clip/v2/resource/grouped_light/{rid}" \
      -H "hue-application-key: {username}" \
      -d '{{"on":{{"on":{inject}}}}}' \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str


def setGroupedLightBrightness(rid:str, brightness:int) -> str:
  request = f''' \
    curl --insecure \
      -X PUT "https://{bridge_ip}/clip/v2/resource/grouped_light/{rid}" \
      -H "hue-application-key: {username}" \
      -d '{{"dimming":{{"brightness":{brightness}}}}}' \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str


def setGroupedLightColor(rid:str, color:Dict[str,float]) -> str:
  request = f''' \
    curl --insecure \
      -X PUT "https://{bridge_ip}/clip/v2/resource/grouped_light/{rid}" \
      -H "hue-application-key: {username}" \
      -d '{{"color":{{"xy":{{"x":{color["x"]},"y":{color["y"]}}}}}}}' \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str


def setLightBrightnessColor(rid:str, brightness:int, color:Dict[str,float]) -> str:
  request = f''' \
    curl --insecure \
      -X PUT "https://{bridge_ip}/clip/v2/resource/light/{rid}" \
      -H "hue-application-key: {username}" \
      -d '{{"dimming":{{"brightness":{brightness}}},"color":{{"xy":{{"x":{color["x"]},"y":{color["y"]}}}}}}}' \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str


def setGroupedLightBrightnessColor(rid:str, brightness:int, color:Dict[str,float]) -> str:
  request = f''' \
    curl --insecure \
      -X PUT "https://{bridge_ip}/clip/v2/resource/grouped_light/{rid}" \
      -H "hue-application-key: {username}" \
      -d '{{"dimming":{{"brightness":{brightness}}},"color":{{"xy":{{"x":{color["x"]},"y":{color["y"]}}}}}}}' \
  '''
  output = check_output(request, shell=True, executable='/bin/zsh')
  output_str = output.decode("utf-8")
  pprint(json.loads(output_str))
  return output_str
