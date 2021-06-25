import re
from functools import partial

from discord.ext import commands
from chatterbot.conversation import Statement


class Trainer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accumulator = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if not (
            message.guild and message.reference and not message.author.bot
        ):
            return

        cached = message.reference.cached_message
        if not cached:
            return

        itext = re.sub(r'<@!?[0-9]{17,22}>', '', cached.content).strip()

        input_statement = Statement(text=itext, search_text=itext.lower())

        rtext = re.sub(r'<@!?[0-9]{17,22}>', '', message.content).strip()

        response_statement = Statement(text=rtext, search_text=rtext.lower())

        to_run = partial(
            self.bot.chatbot.learn_response,
            response_statement,
            input_statement,
        )
        await self.bot.loop.run_in_executor(None, to_run)


def setup(bot):
    bot.add_cog(Trainer(bot))
