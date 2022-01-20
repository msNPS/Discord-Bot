import discord
from discord.ext import commands
from discord_slash import SlashCommand
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')
token = config['Main']['token']
bot_status = config['Main']['bot_status']
channel_goshik = int(config['Channel']['goshik'])

intents = discord.Intents.all()
client = commands.Bot(command_prefix='', intents=discord.Intents.all(),help_command=None)
slash = SlashCommand(client, sync_commands=True)

cogs = ['admin',
'fun_answers',
'fun_commands',
'mute',
'roles',
'memes',
'voice',
]
for cog in cogs:
  client.load_extension('cogs.' + cog)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=bot_status))
  channel = client.get_channel(channel_goshik)
  await channel.send('I\'m ready')
  print('Bot is ready')


client.run(token)