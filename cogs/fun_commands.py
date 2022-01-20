import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components as Components
from discord_slash.model import ButtonStyle
import configparser
import random

client = commands.Bot(command_prefix='', intents=discord.Intents.all())

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')
answer_ball = list(config['Answer']['ball'].split('; '))
answer_money = list(config['Answer']['money'].split('; '))
guild_id = int(config['Main']['guild_id'])
guild_ids = [guild_id]


class FunCommands(commands.Cog):

  def __init__(self, client):
    self.client = client


  @cog_ext.cog_slash(name='Ping', description='Sends bot\'s latency', guild_ids=guild_ids)
  async def ping(self, ctx):
    embed = discord.Embed(colour=discord.Color.blue())
    embed.title = '📶 Задержка: ' + str(int(self.client.latency * 1000)) + 'ms'
    await ctx.send(embed=embed)


  @cog_ext.cog_slash(name='Ball', description='Магический шар', guild_ids=guild_ids,
    options=[
      create_option(name='вопрос', description='Вопрос Магическому шару', required=False, option_type=3)
    ]
  )
  async def ball(self, ctx, вопрос: str):
    embed = discord.Embed(colour=discord.Color.purple())
    embed.title = '🔮 ' + random.choice(answer_ball)
    if вопрос:
      embed.description = f'Вопрос: {вопрос}'
    await ctx.send(embed=embed)


  @cog_ext.cog_slash(name='Roll', description='Случайное число', guild_ids=guild_ids,
    options=[
      create_option(name='число', description='Максимальное число', required=True, option_type=4)
    ]
  )
  async def roll(self, ctx, число: int):
    embed = discord.Embed(colour=discord.Color.dark_blue())
    embed.title = '🔘 Результат: ' + str(random.randint(1, число))
    embed.description = f'Среди чисел от 1 до {str(число)}'
    await ctx.send(embed=embed)


  @cog_ext.cog_slash(name='Pick', description='Выбор одного из вариантов', guild_ids=guild_ids,
    options=[
      create_option(name='варианты', description='Через запятую', required=True, option_type=3)
    ]
  )
  async def pick(self, ctx, варианты: str):
    embed = discord.Embed(colour=discord.Color.dark_teal())
    embed.title = '💠 Результат: ' + str(random.choice(варианты.split(',')))
    embed.description = f'Варианты: {варианты}'
    await ctx.send(embed=embed)


  @cog_ext.cog_slash(name='Coin', description='Орёл или решка', guild_ids=guild_ids)
  async def fun_money(self, ctx):
    embed = discord.Embed(colour=discord.Color.gold())
    embed.title = random.choice(answer_money)
    await ctx.send(embed=embed)


  @cog_ext.cog_slash(name='Rock', description='Камень, ножницы, бумага', guild_ids=guild_ids)
  async def rock(self, ctx):
    while True:
      buttons = [
        Components.create_button(label='🗿Камень', style=ButtonStyle.blurple, custom_id='0'),
        Components.create_button(label='✂️Ножницы', style=ButtonStyle.blurple, custom_id='1'),
        Components.create_button(label='🧻Бумага', style=ButtonStyle.blurple, custom_id='2')
      ]
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.title = '👊 Камень, ножницы, бумага'
      embed.description = 'Каждый игрок должен выбрать один из вариантов'
      actionrow = Components.create_actionrow(*buttons)
      await ctx.send(embed=embed, components=[actionrow])

      first = await Components.wait_for_component(self.client, components=actionrow)
      await first.edit_origin()
      second = await Components.wait_for_component(self.client, components=actionrow)
      if first.custom_id == second.custom_id:
        embed.title = '👊 __Ничья__'
      elif (first.custom_id=='0' and second.custom_id=='1') or (first.custom_id=='1' and second.custom_id=='2') or (first.custom_id=='2' and second.custom_id=='0'):
        embed.title = f'👊 __{first.author.name}__ победил!'
      else:
        embed.title = f'👊 __{second.author.name}__ победил!'

      embed.description = ''
      buttons = [Components.create_button(label='🔁Заново', style=ButtonStyle.blurple, custom_id='replay')]
      actionrow = Components.create_actionrow(*buttons)
      chooser = {'0': '🗿Камень', '1': '✂️Ножницы', '2': '🧻Бумага'}
      embed.add_field(name=first.author.name+':', value=chooser[first.custom_id], inline=False)
      embed.add_field(name=second.author.name+':', value=chooser[second.custom_id], inline=False)
      await second.edit_origin(embed=embed, components=[actionrow])

      replay = await Components.wait_for_component(self.client, components=actionrow)
      await replay.edit_origin()


def setup(client):
  client.add_cog(FunCommands(client))