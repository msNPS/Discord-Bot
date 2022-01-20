import discord
from discord.ext import commands
from discord.role import Role
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components as Components
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType as permision_type
import configparser

client = commands.Bot(command_prefix='', intents=discord.Intents.all())

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')
role_admin = int(config['Role']['admin'])
role_everyone = int(config['Role']['everyone'])
role_muted = int(config['Role']['muted'])
channel_goshik = int(config['Channel']['goshik'])
channel_chat = int(config['Channel']['chat'])
guild_id = int(config['Main']['guild_id'])
guild_ids = [guild_id]
admin_only = {guild_id: [
  create_permission(role_admin, permision_type.ROLE, True),
  create_permission(role_everyone, permision_type.ROLE, False),
]}

file_answer_welcome = open('answer_welcome.txt', 'rb')
answer_welcome = file_answer_welcome.read().decode('utf-8')
file_answer_welcome.close()

class Admin(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener('on_command_error')
  async def error_handler(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return
    channel = self.client.get_channel(channel_goshik)
    await channel.send(error)
    raise error

  @cog_ext.cog_slash(name='Clear', description='Удалить последние x сообщений', guild_ids=guild_ids,
    options=[
      create_option(name='amount', description='Кол-во удалённых сообщений', required=True, option_type=4)
    ],
    permissions=admin_only
  )
  @commands.has_any_role(role_admin)
  @client.command()
  async def clear(self, ctx, amount: int):
    await ctx.send('...')
    await ctx.channel.purge(limit = amount + 1)

  @cog_ext.cog_slash(name='MemeClear', description='Очистить не мемы', guild_ids=guild_ids,
    options=[
      create_option(name='limit', description='Количество просмотренных сообщений', required=True, option_type=4)
    ],
    permissions=admin_only
  )
  @commands.has_any_role(role_admin)
  @client.command()
  async def memeclear(self, ctx, limit: int):
    await ctx.send('...')
    amount = 0
    async for message in ctx.channel.history(limit=limit + 1):
      if len(message.reactions) > 0 and str(message.reactions[0]) == '🤍':
        break
      amount += 1
    await ctx.channel.purge(limit=int(amount))

  @cog_ext.cog_slash(name='SendMessage', description='Отправить сообщение', guild_ids=guild_ids,
    options=[
      create_option(name='канал', description='Канал назначения', required=True, option_type=3),
      create_option(name='контент', description='Текст сообщения', required=True, option_type=3),
    ],
    permissions=admin_only
  )
  async def sendmessage(self, ctx, канал: str, контент: str):
    target = self.client.get_user(int(канал))
    if target == None:
      user = self.client.get_channel(int(канал))
    if target != None:
      await target.send(контент)
      embed = discord.Embed(color=discord.Color.dark_blue())
      embed.title = f'📨 \"{контент}\"'
    else:
      embed = discord.Embed(color=discord.Color.red())
      embed.title = '❌ ' + 'Ошибка'
      embed.description = f'Контент: \"{контент}\"'
    embed.set_footer(text=str(канал))
    await ctx.send(embed=embed)

  @commands.Cog.listener('on_message')
  async def direct_message(self, message):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author.name != 'Гошик':
      author = message.author
      embed = discord.Embed(color=discord.Color.blue())
      embed.title = f'📩 \"{message.content}\"'
      embed.set_author(name = author.name, icon_url = author.avatar_url)
      embed.set_footer(text=str(message.author.id))
      channel = self.client.get_channel(channel_goshik)
      await channel.send(embed=embed)

  @commands.Cog.listener('on_member_join')
  async def member_enter(self, member):
    await member.send(answer_welcome)
    channel = self.client.get_channel(channel_chat)
    embed = discord.Embed(color = 0)
    embed.title = f'🥳{member.name} подключается!'
    embed.description = 'Теперь на сервере на одного дебила больше!'
    await channel.send(embed=embed)

  @commands.Cog.listener('on_member_remove')
  async def member_exit(self, member):
    channel = self.client.get_channel(channel_chat)
    embed = discord.Embed(color = 0)
    embed.title = f'😪{member.name} куда-то ушёл...'
    embed.description = 'Press F'
    message = await channel.send(embed=embed)
    await message.add_reaction('🇫')

def setup(client):
  client.add_cog(Admin(client))
