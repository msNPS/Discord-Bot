import discord
from discord.ext import commands
import configparser

client = commands.Bot(command_prefix='', intents=discord.Intents.all())

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')
guild_id = int(config['Main']['guild_id'])
message_roles = int(config['Message']['roles'])
react_roles  = config['React_roles']

class Roles(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener('on_raw_reaction_add')
  async def role_reaction_add(self, reaction):
    if reaction.message_id == message_roles:
      guild = self.client.get_guild(guild_id)
      emoji = reaction.emoji.name
      role = guild.get_role(int(react_roles[emoji]))
      member = guild.get_member(reaction.user_id)
      await member.add_roles(role)

  @commands.Cog.listener('on_raw_reaction_remove')
  async def role_reaction_remove(self, reaction):
    if reaction.message_id == message_roles:
      guild = self.client.get_guild(guild_id)
      emoji = reaction.emoji.name
      role = guild.get_role(int(react_roles[emoji]))
      member = guild.get_member(reaction.user_id)
      await member.remove_roles(role)

def setup(client):
  client.add_cog(Roles(client))