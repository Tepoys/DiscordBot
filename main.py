import os
from typing import Final

import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

import shop
from player import Player

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
intents: Intents = Intents.default()
intents.message_content = True  # NOQA

bot: commands.Bot = commands.Bot(command_prefix='/', intents=intents)

shops: dict[str, shop.Shop] = shop.get_all_shops()


class Collection:
    def __init__(self, user_id: str):
        self.view_dictionary = {}
        self.user_id = user_id
        self.player = Player(id=user_id)
        self.view_dictionary['menu'] = Menu(self)
        self.view_dictionary['shop'] = Shop(self)
        self.view_dictionary['leaderboard'] = Leaderboard(self)
        self.view_dictionary['unbox'] = Unbox(self)

    def menu(self):
        return self.view_dictionary['menu']

    def shop(self):
        return self.view_dictionary['shop']

    def leaderboard(self):
        return self.view_dictionary['leaderboard']

    def unbox(self):
        return self.view_dictionary['unbox']


class Menu(discord.ui.View):
    def __init__(self, collection: Collection):
        super().__init__()
        self.collection = collection
        raise NotImplementedError


class Shop(discord.ui.View):
    def __init__(self, collection: Collection):
        super().__init__()
        self.collection = collection
        raise NotImplementedError


class Leaderboard(discord.ui.View):
    def __init__(self, collection: Collection):
        super().__init__()
        self.collection = collection
        raise NotImplementedError


class Unbox(discord.ui.View):
    def __init__(self, collection: Collection):
        super().__init__()
        self.collection = collection
        raise NotImplementedError


# Test and initiation below


# noinspection PyUnresolvedReferences
@bot.tree.command(name='ping', description="Pong!")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Pong (Latency is {round(bot.latency * 1000)}ms)")


@bot.tree.command(name='test', description="Testing pycord features")
async def test(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("This is a response")
    await interaction.followup.send("This is a followup")


class TestView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.interaction_count = 0

    # noinspection PyUnresolvedReferences
    @discord.ui.button(label="Click here!", style=discord.ButtonStyle.blurple)
    async def callback(self, inter: discord.Interaction, button: discord.ui.Button) -> None:
        if self.interaction_count == 0:
            await inter.response.send_message("Hello!")
        elif self.interaction_count == 1:
            button.disabled = True
            await inter.response.edit_message(view=self)
            await inter.followup.send("No more pressing!")
        self.interaction_count += 1
        return


def create_test_embed() -> discord.Embed:
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


@bot.tree.command(name='view', description="Testing Views")
async def view(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(view=TestView(), embed=create_test_embed())


@bot.event
async def on_ready() -> None:
    print(f'{bot.user.name} (id: {bot.user.id}) is now running')

    try:
        await bot.tree.sync()
        print('Commands Synced')
    except Exception as e:
        print(e)

    print('The bot is currently in guilds with id:')
    for guild in bot.guilds:
        print(guild.id)


def main() -> None:
    print('Starting bot...')
    bot.run(TOKEN)

    cleanup()


def cleanup() -> None:
    print('Cleaning up...')
    shop.cleanup()
    print('Cleanup compleat')


if __name__ == "__main__":
    main()
