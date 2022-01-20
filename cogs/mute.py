import discord
from discord.ext import commands
import configparser
import asyncio

client = commands.Bot(command_prefix='', intents=discord.Intents.all())

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')
role_admin = int(config['Role']['admin'])
role_muted = int(config['Role']['muted'])

class Mute(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.has_any_role(role_admin)
  @client.command()
  async def mute(self, ctx, member: discord.Member):
    role = ctx.guild.get_role(role_muted)
    await member.add_roles(role)
    embed = discord.Embed(colour=0x95a5a6)
    embed.title = f'🔇 **{str(member)}** был выключен'
    await ctx.send(embed=embed)

  @commands.has_any_role(role_admin)
  @client.command()
  async def unmute(self, ctx, member: discord.Member):
    role = ctx.guild.get_role(role_muted)
    await member.remove_roles(role)
    embed = discord.Embed(colour=0x95a5a6)
    embed.title = f'🔊 **{str(member)}** может продолжать общаться'
    await ctx.send(embed=embed)

  @commands.has_any_role(role_admin)
  @client.command()
  async def tempmute(self, ctx, member: discord.Member, time: int):
    role = ctx.guild.get_role(role_muted)
    await member.add_roles(role)
    embed = discord.Embed(colour=0x95a5a6)
    embed.title = f'🔇 **{str(member)}** был выключен на {time} минут'
    await ctx.send(embed=embed)
    await asyncio.sleep(time * 60)
    await self.unmute(ctx, member)


def setup(client):
  client.add_cog(Mute(client))