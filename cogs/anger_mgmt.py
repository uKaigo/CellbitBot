import asyncio

from discord.ext import commands


class AngerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accumulator = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and message.guild.me in message.mentions:
            self.accumulator += 1

            if self.accumulator != 50:
                return

            self.bot.anger += 1

            self.accumulator = 0

            anger = self.bot.anger

            if anger % 5 == 0:
                await self.notify_anger()

            if anger == 100:
                await self.delete_guild(message.guild)

            if anger % 10 == 0 and len(self.bot.achieved_percentages) != 7:
                self.bot.achieved_percentages.append(str(anger))

    async def notify_anger(self):
        channel = self.bot.get_channel(858065167035924490)

        txt = f'Nivel de raiva em {self.bot.anger}%!'

        if self.bot.anger > 90:
            await channel.send(txt.upper())
        else:
            await channel.send(txt)

    async def delete_guild(self, guild):
        channel = self.bot.get_channel(858065167035924490)

        for i in range(5, 0, -1):
            S = '' if i == 1 else 'S'

            await channel.send(f'DELETANDO O SERVIDOR EM {i} SEGUNDO{S}!')
            await asyncio.sleep(1)

        await guild.delete()


def setup(bot):
    bot.add_cog(AngerManagement(bot))
