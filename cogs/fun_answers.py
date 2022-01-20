import discord
from discord.ext import commands
import asyncio
import random

client = commands.Bot(command_prefix='', intents = discord.Intents.all())

class FunAnswers(commands.Cog):
  def __init__(self, client):
    self.client = client

  @client.command(aliases=['спасибо', 'Спасибо', 'СПАСИБО'])
  async def thank_you(self, ctx):
    await ctx.send('да пожалуйста')

  @client.command(aliases=['Короче', 'КОРОЧЕ', 'короче'])
  async def short(self, ctx):
    await ctx.send('длиннее')

  @client.command(aliases=['Го', 'ГО', 'го'])
  async def go(self, ctx):
    await ctx.send(
      random.choice(['го - годен', 'го - говно', 'го - Гошик, да, это я']))

  @client.command(aliases=['Ладно', 'ладно', 'Ладно,', 'ладно,'])
  async def ok2(self, ctx):
    await ctx.send('прохладно')

  @client.command(aliases=['Чётко', 'чётко', 'Четко', 'четко'])
  async def good1(self, ctx):
    await ctx.send('размыто')

  @client.command(aliases=['Размыто', 'размыто'])
  async def good2(self, ctx):
    await ctx.send('чётко')

  @client.command(aliases=['Крутой', 'крутой'])
  async def cool(self, ctx):
    await ctx.send('Вытри сперму под губой')

  @client.command(aliases=['!rank'])
  async def rank(self, ctx):
    if ctx.message.content == '!rank <@!702472488600207371>':
      await asyncio.sleep(1)
      await ctx.send('Иди нахуй')


def setup(client):
  client.add_cog(FunAnswers(client))