import json
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.tagging import LowercaseTagger
from chatterbot.trainers import ListTrainer

load_dotenv()


class CellBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chatbot = ChatBot('Cellbit', tagger=LowercaseTagger)
        self.trainer = ListTrainer(self.chatbot)

        self.anger = 0

        with open('textos.json') as f:
            self.texts = json.load(f)
        self.achieved_percentages = []

    def load_extensions(self):
        extensions = [
            c[:-3] for c in os.listdir('cogs') if not c.startswith('_')
        ]

        for extension in extensions:
            try:
                self.load_extension('cogs.' + extension)
            except Exception as e:
                print(f'[{extension}] {type(e).__name__}: {e}')
            else:
                print(f'[{extension}] Carregado')
        self.load_extension('jishaku')

    async def on_ready(self):
        print(f'Logado como: {self.user}')


bot = CellBot(
    command_prefix='!',
    status=discord.Status.dnd
    #    activity=discord.Streaming(
    #        name='UM DETETIVE', url='https://twitch.tv/cellbit'
    #    ),
)
bot.load_extensions()

bot.run(os.environ['TOKEN'])
