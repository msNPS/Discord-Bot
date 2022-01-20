import discord
from discord.ext import commands, tasks
import configparser

client = commands.Bot(command_prefix='', intents=discord.Intents.all())

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')
guild_id = int(config['Main']['guild_id'])
vc_start = int(config['VChannel']['start'])
vc_chill = int(config['VChannel']['chill'])

def is_gaming(channel):
  global vc_start
  return channel.id != vc_start and channel.id != vc_chill

def is_game(activity):
  return isinstance(activity, discord.Game) or isinstance(activity, discord.Activity)


class Voice(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener('on_voice_state_update')
  async def vc_update(self, member, before, after):
    global vc_start
    if before.channel != None and is_gaming(before.channel) and len(before.channel.members) == 0:
      await before.channel.delete()
    if after.channel != None and after.channel.id == vc_start:
      new_name = 'Gaming'
      for activity in member.activities:
        if (is_game(activity)):
          new_name = activity.name
          break
      channel = await after.channel.category.create_voice_channel(name = new_name, position = 1)
      await member.move_to(channel)

  @commands.Cog.listener('on_ready')
  async def start_checker(self):
    self.check_sessions.start()

  @tasks.loop(minutes = 4)
  async def check_sessions(self):
    channel_chill = self.client.get_channel(vc_chill)
    for channel in channel_chill.category.voice_channels:
      if not is_gaming(channel):
        continue

      new_name = 'Gaming'
      for member in channel.members:
        if member.bot:
          continue
        other = False
        the_same = False
        for activity in member.activities:
          if is_game(activity):
            if new_name == 'Gaming':
              new_name = activity.name
            if activity.name == new_name:
              the_same = True
            else:
              other = True
        if not the_same and other:
          new_name = 'Gaming'
          break

      if channel.name != new_name:
        await channel.edit(name = new_name)


def setup(client):
  client.add_cog(Voice(client))