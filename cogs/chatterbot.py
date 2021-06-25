import re
import random
from functools import partial

from discord.ext import commands


class ChatterBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or not message.guild.me in message.mentions:
            return

        if self.bot.anger >= 90:
            return await message.author.ban()

        if self.bot.anger >= 80:
            if random.random() <= 0.1:
                return await message.author.ban()

        if self.bot.achieved_percentages and random.random() <= 0.3:
            to_choose = []
            for anger in self.bot.achieved_percentages:
                to_choose.extend(self.bot.texts[anger])

            await message.channel.send(random.choice(to_choose))

        text = re.sub(r'<@!?[0-9]{17,22}>', '', message.content).strip()

        to_run = partial(self.bot.chatbot.get_response, text)
        response = await self.bot.loop.run_in_executor(None, to_run)

        await message.reply(response.text)


def setup(bot):
    bot.add_cog(ChatterBot(bot))
