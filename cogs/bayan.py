import discord
from discord.ext import commands
from PIL import Image
import configparser
import pickle

client = commands.Bot(command_prefix='', intents=discord.Intents.all())

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf8')
guild_id = int(config['Main']['guild_id'])
goshik_id = int(config['Main']['goshik_id'])


with open('all_memes.pickle', 'wb') as f:
    pickle.dump({}, f)
with open('all_memes.pickle', 'rb') as f:
    data = pickle.load(f)

class Bayan(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    def closest(self, n):
        if n < 64:
            return 64
        else:
            return 192

    @commands.Cog.listener('on_raw_reaction_add')
    async def new_meme(self, reaction):
        if str(reaction.emoji) == '🤍':
            channel = self.client.get_channel(reaction.channel_id)
            message = await channel.fetch_message(reaction.message_id)
            files = message.attachments
            if len(files) > 0 and 'image' in files[0].content_type:
                await files[0].save('image.png')
                img = Image.open('image.png')
                img = img.resize((64, 64))
                hash = ''
                for x in range(64):
                    for y in range(64):
                        color = img.getpixel((x, y))
                        hash += str(self.closest(color[0]) * 4 + self.closest(color[1]) * 2 + self.closest(color[2]))
                if hash in data:
                    print(data[hash])
                else:
                    data[hash] = message.jump_url
                    with open('all_memes.pickle', 'wb') as f:
                        pickle.dump(data, f)

def setup(client):
  client.add_cog(Bayan(client))