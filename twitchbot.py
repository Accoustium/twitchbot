import os
from dotenv import load_dotenv
from twitchio.ext import commands
import twitchio


dotenv_path = os.path.join(os.path.dirname('__file__'), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')
NICK = os.getenv('NICK')
CHANNEL = os.getenv('CHANNEL')


class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(irc_token=TOKEN, nick=NICK, prefix='!',
                         initial_channels=[CHANNEL])

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='test')
    async def my_command(self, ctx: twitchio.Context):
        await ctx.send(f"Hello {ctx.author.name}")

    @commands.command(name='hello')
    async def hello_command(self, ctx: twitchio.Context):
        await ctx.send(f"Hello {ctx.author.name}!")


twitch = TwitchBot()
twitch.run()
