from traceback import print_exc

from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            return
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.TooManyArguments):
            return

        print_exc()


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
