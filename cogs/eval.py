from time import time
from discord.ext import commands
from inspect import getsource
import discord
import asyncio
import os


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif not var_length:
                return f"<an empty {type(variable).__name__} iterable>"

        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (
            variable
            if (len(f"{variable}") <= 1000)
            else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>"
        )

    def prepare(self, string):
        arr = (
            string.strip("```")
            .replace("py\n", "")
            .replace("python\n", "")
            .split("\n")
        )
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)

    @commands.command(name="eval")
    @commands.has_role(976446281033580564)
    async def _eval(self, ctx, *, code: str):
        show_info = "--info" in code
        code = self.prepare(code.replace("--info", "").replace("```", ""))
        args = {
            "discord": discord,
            "self": self,
            "ctx": ctx,
            "asyncio": asyncio,
            "os": os,
        }

        try:
            exec(f"async def func():{code}", args)
            a = time()
            response = await eval("func()", args)
            if show_info == True:
                e = discord.Embed(
                    title="Evaluated", color=discord.Color.dark_purple()
                )
                e.add_field(
                    name="Code:", value=f"```py\n{code}```", inline=False
                )
                e.add_field(
                    name="Language:", value="```Python```", inline=False
                )
                e.add_field(
                    name="Executed by:",
                    value=f"```{ctx.author}```",
                    inline=False,
                )
                e.add_field(
                    name="Executed in:",
                    value=f"```{(time() - a) / 1000}ms```",
                    inline=False,
                )
                await ctx.send(embed=e, delete_after=15)
                await ctx.message.add_reaction("✅")
                del args, code
                return

            await ctx.message.add_reaction("✅")
        except Exception as e:
            await ctx.send(
                f"Error occurred:```\n{type(e).__name__}: {str(e)}```"
            )

        del args, code, show_info


def setup(bot):
    bot.add_cog(Eval(bot))
