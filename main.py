#!/usr/bin/env python

'''README
<summary>

Usage:
  ./main.py run

References:
  https://typer.tiangolo.com/
  https://discordpy.readthedocs.io/en/stable/api.html
'''

# stdlib
from os import path
from pathlib import Path
from typing import List, Dict, Union
from sys import argv, exit, getsizeof
from subprocess import call, check_output
from typing import List, Dict, Optional
from datetime import datetime
import json
# custom modules
from toolchain.commands import example_command_logic
# 3rd party
try:
  import typer
  from yaml import safe_load, YAMLError
  from discord import Client, Intents, File, app_commands, Object, Interaction
  import discord.ext
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


#───Globals──────────────────
app = typer.Typer()
with open('creds.yml', 'r') as raw_config:
  config_dict   = safe_load(raw_config)
  app_id        = config_dict['app_id']
  public_key    = config_dict['public_key']
  perms_int     = config_dict['perms_int']
  token         = config_dict['token']
  client_id     = config_dict['client_id']
  client_secret = config_dict['client_secret']
  guild_id      = config_dict['guild_id']


#───Commands─────────────────
@app.command()
def run() -> None:
  '''TITLE

  DESCRIPTION

  ───Params\n
  my_param:type :: description

  ───Return\n
  type :: description
  '''
  ## Init
  guild = discord.Object(id=guild_id)
  class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
      super().__init__(intents=intents)
      self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
      self.tree.copy_global_to(guild=guild)
      await self.tree.sync(guild=guild)
  intents = Intents(messages=True, guilds=True, members=True)
  client  = MyClient(intents=intents)


  ## Commands
  @client.event
  async def on_ready():
    '''Print successful login.'''
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('──────')
  #───
  @client.tree.command()
  async def example_command(interaction: discord.Interaction):
    '''This becomes the command description in Discord.'''
    message = example_command_logic()
    await interaction.response.send_message(message)
  #───


  ## Login
  try:
    client.run(token)
  except Exception as e:
    print(f'Error on attempted login:\n{e}')
  return None


#───Entry────────────────────
if __name__ == "__main__":
  app()
