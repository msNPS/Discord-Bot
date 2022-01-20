import discord
from discord.ext import commands, tasks
import configparser
import pickle
from datetime import datetime
from cogs.mute import Mute

client = commands.Bot(command_prefix='', intents=discord.Intents.all())

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')
guild_id = int(config['Main']['guild_id'])
memes_cof = float(config['Main']['memes_cof'])
memes_max = int(config['Main']['memes_max'])
channel_memes = int(config['Channel']['memes'])
role_admin = int(config['Role']['admin'])
role_meman = int(config['Role']['meman'])

answer_likeWarning = list(config['Answer']['like_warning'].split('; '))
with open('stats.pickle', 'rb') as f:
  data = pickle.load(f)

class Memes(commands.Cog):
  def __init__(self, client):
    self.client = client

  async def get(self, authorID):
    guild = self.client.get_guild(guild_id)
    author = guild.get_member(authorID)
    role = guild.get_role(role_meman)
    return author, role

  async def plus(self, authorID):
    if authorID not in data:
      data[authorID] = [0, 0, 0, 0, 0]
    data[authorID][-1] = min(data[authorID][-1] + 1, memes_max)
    if sum(data[authorID]) >= memes_cof:
      author, role = self.get(authorID)
      await author.add_roles(role)
    with open('stats.pickle', 'wb') as f:
      pickle.dump(data, f)

  async def clear(self, authorID):
    data[authorID] = [0, 0, 0, 0, 0]
    author, role = self.get(authorID)
    await author.remove_roles(role)
    with open('stats.pickle', 'wb') as f:
      pickle.dump(data, f)

  async def shift(self):
    new_data = {}
    for el in data:
      data[el].pop(0)
      data[el].append(0)
      sum(data[el])
      if sum(data[el]) / 5 < memes_cof:
        member, role = self.get(el)
        await member.remove_roles(role)
      if (data[el] != [0, 0, 0, 0, 0]):
        new_data[el] = data[el]
    with open('stats.pickle', 'wb') as f:
      pickle.dump(new_data, f)

  @commands.has_any_role(role_admin)
  @client.command()
  async def statsplus(self, ctx, authorID):
    await self.plus(int(authorID))
    await ctx.message.add_reaction('✅')

  @commands.has_any_role(role_admin)
  @client.command()
  async def statsclear(self, ctx, authorID):
    await self.clear(int(authorID))
    await ctx.message.add_reaction('✅')

  @commands.has_any_role(role_admin)
  @client.command()
  async def statsshift(self, ctx):
    await self.shift()
    await ctx.message.add_reaction('✅')

  @client.command()
  async def statsget(self, ctx):
    with open('stats.pickle', 'rb') as f:
      data = pickle.load(f)
    embed = discord.Embed(colour=0x3498db, title='💾 Meme stats')
    for i in data:
      values = ''
      for j in data[i]:
        values += str(j) + ' '
      embed.add_field(name=str(i), value=values, inline=False)
    await ctx.send(embed=embed)

  @commands.Cog.listener('on_message')
  async def new_meme(self, message):
    if message.channel.id == channel_memes and not message.author.bot:
      if len(message.attachments) > 0 or 'https://' in message.content or 'http://' in message.content:
        await message.add_reaction('🤍')
        await self.plus(message.author.id)

  @commands.has_any_role(role_admin)
  @client.command()
  async def animeme(self, ctx):
    if (ctx.message.reference != None):
      guild = self.client.get_guild(guild_id)
      role = guild.get_role(role_meman)
      author = ctx.message.reference.resolved.author
      if (role in author.roles):
        embed = discord.Embed(color = 0xe91e63)
        embed.title = '📵 Никакого ониме!'
        embed.description = f'{str(author)[:-5]}, иди в #anime'
        await ctx.message.reference.resolved.reply(embed=embed)
        await self.clear(author.id)
      else:
        await Mute.tempmute(self, ctx, author, 15)

  @commands.Cog.listener('on_ready')
  async def start_checker(self):
    self.new_day.start()

  @tasks.loop(hours = 1)
  async def new_day(self):
    if datetime.now().hour + 3 == 24:
      
      print("NEW DAY")
      await self.shift()

def setup(client):
  client.add_cog(Memes(client))
