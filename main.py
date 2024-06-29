import os
import sqlite3
from typing import Final

import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
intents: Intents = Intents.default()
intents.message_content = True  # NOQA

bot: commands.Bot = commands.Bot(intents=intents)





@bot.slash_command(name='ping', description="Pong!", guild_ids=['1126289653654360195'])
async def ping(ctx: discord.ApplicationContext) -> None:
    await ctx.respond(f"Pong (Latency is {round(bot.latency * 1000)}ms)")


@bot.slash_command(name='test', description="Testing pycord features", guild_ids=['1126289653654360195'])
async def test(ctx: discord.ApplicationContext) -> None:
    await ctx.send_response("This is a response")
    await ctx.send_followup("This is a followup")


class TestView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.interaction_count = 0

    @discord.ui.button(label="Click here!", style=discord.ButtonStyle.blurple)
    async def click(self, button: discord.ui.Button, inter: discord.Interaction) -> None:
        if self.interaction_count == 0:
            await inter.response.send_message("Hello!")
        elif self.interaction_count == 1:
            button.disabled = True
            await inter.response.edit_message(view=self)
            await inter.followup.send("No more pressing!")
        self.interaction_count += 1
        return


def create_embed() -> discord.Embed:
    embed: discord.Embed = discord.Embed(
        title="My Embed",
        description='Simple embed that definitely took me less than 5 minutes to make',
        color=discord.Color.blurple(),
    )
    embed.set_author(name="Professional Discord Bot Dev",
                     icon_url='https://cdn-icons-png.flaticon.com/256/998/998463.png')
    embed.add_field(name='A Field', value='This is a normal field', inline=False)
    embed.add_field(name='Inline field 1', value='This is an inline field!', inline=True)
    embed.add_field(name='Inline field 2', value='This is an inline field!', inline=True)
    embed.add_field(name='Inline field 3', value='This is an inline field!', inline=True)
    embed.add_field(name='Inline field 4', value='This is an inline field!', inline=True)
    embed.set_footer(text='Brought to you by RAID SHADOW LEGENDS',
                     icon_url='https://cdn-icons-png.flaticon.com/256/998/998463.png')
    embed.set_thumbnail(url="https://ih1.redbubble.net/image.5531844437.1090/st,small,507x507-pad,600x600,f8f8f8.jpg")

    return embed


@bot.slash_command(name='view', description="Testing Views", guild_ids=['1126289653654360195'])
async def view(ctx: discord.ApplicationContext) -> None:
    await ctx.respond(view=TestView(), embed=create_embed())


@bot.event
async def on_ready() -> None:
    print(f'{bot.user.name} (id: {bot.user.id}) is now running')
    '''
    try:
        await bot.sync_commands()
        print('Commands Synced')
    except Exception as e:
        print(e)
    '''
    print('The bot is currently in guilds with id:')
    for guild in bot.guilds:
        print(guild.id)


def main() -> None:
    print('Starting bot...')
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
 