from os import getenv
from dotenv import load_dotenv
from discord import Intents
from discord.ext.commands import Bot
from commands.bot_commands import BotCommands


class DiscordBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    def run(self):
        # Set up intents for the bot
        intents = Intents.default()
        intents.message_content = True
        bot = Bot(
            command_prefix="!",
            intents=intents,
            help_command=None,
            case_insensitive=True,
        )

        @bot.event
        async def on_ready():
            # Print in the terminal when the bot is ready
            print(f"{bot.user} is ready!")

            # Iterate through all servers
            for guild in bot.guilds:
                # Iterate through all text channels
                for channel in guild.text_channels:
                    # Verify bot's permission to send messages
                    if channel.permissions_for(guild.me).send_messages:
                        await channel.send(
                            "Alright, enough with the chaos. I'm here to bring some order... or add to the madness. Your call. Type !help if you dare."
                        )
                        break

        bot.add_cog(BotCommands(bot))
        bot.run(self.bot_token)


if __name__ == "__main__":
    load_dotenv()
    try:
        token = getenv("DISCORD_BOT_TOKEN")
        bot = DiscordBot(bot_token=token)
        bot.run()
    except ValueError as e:
        print(f"ERROR: {e}")
