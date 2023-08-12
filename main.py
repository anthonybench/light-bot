#!/usr/bin/env python

'''README
Control lights on the network.

After setting up the discord application, populate and follow the link below:
  https://discord.com/api/oauth2/authorize?client_id=1136852293577343016&permissions=70368744177655&scope=bot%20applications.commands

Usage:
  ./main.py run

References:
  https://typer.tiangolo.com/
  https://discordpy.readthedocs.io/en/stable/api.html
  https://developers.meethue.com/develop/get-started-2/
  https://www.youtube.com/watch?v=Wz8GnB-LI5w&t=94s
'''

# stdlib
from sys import exit
# custom
from toolchain.commands import lv_logic
# 3rd party
try:
  import typer
  from yaml import safe_load, YAMLError
  from discord import Client, Intents, app_commands, Interaction
  import discord.ext
except ModuleNotFoundError as e:
  print('Error: Missing one or more 3rd-party packages (pip install).')
  exit(1)


#───Globals──────────────────
app = typer.Typer()
with open('config.yml', 'r') as raw_config:
  try:
    config = safe_load(raw_config)
  except YAMLError as e:
    print("Error. YAML input invalid.\n{e}")
    exit(1)
  app_id        = config['app_id']
  public_key    = config['public_key']
  perms_int     = config['perms_int']
  token         = config['token']
  client_id     = config['client_id']
  client_secret = config['client_secret']
  guild_id      = config['guild_id']
  channel_scope = config['channel_scope']
  bridge_ip     = config['bridge_ip']
  username      = config['username']
  client_key    = config['client_key']
  mapping       = config['mapping']


#───Commands─────────────────
@app.command()
def run() -> None:
  '''Light Bot

  Runs Discord bot that interfaces with supported smart lights upon slash-command chat dictation.
  '''
  ## Init
  guild = discord.Object(id=guild_id)
  class MyClient(Client):
    def __init__(self, *, intents: discord.Intents):
      super().__init__(intents=intents)
      self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
      self.tree.copy_global_to(guild=guild)
      await self.tree.sync(guild=guild)
  intents = Intents(messages=True, guilds=True, members=True)
  client  = MyClient(intents=intents)

  @client.event
  async def on_ready():
    '''Print successful login.'''
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('──────')


  ## Commands
  #───
  @client.tree.command()
  async def help(interaction:Interaction):
    '''Explain LightBot usage'''
    if interaction.channel.name in channel_scope:
      message = f'''/`<group>` :: *toggle group*
/`<group>` `<color>` :: *set group color*
/`<group>` `<brightness>` :: *set group brightness*
/`<group>` `<brightness>` `<color>` :: *set group brightness & color, can be in either order*
      
**<group>** 👉 `lv`
**<brightness>** 👉 `0-100` inclusive, leave out "." and "%"
**<color>** 👉 `purple`, `soft-white`'''
      await interaction.response.send_message(message)
    else:
      message = f'Sorry, i only respond in {", ".join(channel_scope)}'
      await interaction.response.send_message(message, ephemeral=True)  
  #───
  @client.tree.command()
  async def lv(interaction:Interaction, dictation:str=''):
    '''Dictate living room lights'''
    if interaction.channel.name in channel_scope:
      message = lv_logic(
        mapping['lv'],
        dictation
      )
      await interaction.response.send_message(message)
    else:
      message = f'Sorry, i only respond in {", ".join(channel_scope)}'
      await interaction.response.send_message(message, ephemeral=True)
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
