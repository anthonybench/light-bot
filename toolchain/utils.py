# stdlib
from datetime import datetime
from pprint import pprint
from statistics import mode, mean
from os import path
from pathlib import Path
from typing import List, Dict, Union
from sys import argv, exit, getsizeof
from subprocess import call, check_output
# 3rd party
try:
  import requests
  from yaml import safe_load, YAMLError
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


#───Utils────────────────────
# if more logic breakout is needed...