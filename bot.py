from os import getenv
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext.commands import Bot
from datetime import datetime
from utils.web_scraping import WebScraper


class DiscordBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.web_scraper = WebScraper()

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

        @bot.event
        async def on_message(message: Message):
            # Ignore bot's own messages
            if message.author.bot:
                return

            if bot.user in message.mentions:
                try:
                    args = message.content.split(" ")
                    action = args[1]

                    if action == "all":  # Fetch entire list of insider trading data
                        company_name = args[2]
                        # Placeholder function
                        insider_data = self.web_scraper.fetch_all_insider_data(
                            company_name
                        )
                        await message.channel.send(
                            f"Insider trading data for {company_name}:\n{insider_data}"
                        )

                    elif action == "latest":  # Fetch the latest 5 insider trading data
                        company_name = args[2]
                        # Placeholder function
                        latest_data = self.web_scraperfetch_latest_insider_data(
                            company_name, 5
                        )
                        await message.channel.send(
                            f"Latest 5 insider trading entries for {company_name}:\n{latest_data}"
                        )

                    elif action == "weekday":
                        date_str = args[2]
                        try:
                            # Parse the date string in the format YYYY/MM/DD into a datetime object
                            date_obj = datetime.strptime(date_str, "%Y/%m/%d")
                            # Get the full name of the weekday from the datetime object
                            weekday = date_obj.strftime("%A")

                            await message.channel.send(
                                f"The date {date_str} falls on a {weekday}."
                            )
                        except ValueError:
                            await message.channel.send(
                                "Please provide the date in YYYY/MM/DD format."
                            )

                except IndexError:
                    await message.channel.send(
                        "That command doesn't exist... did you just make it up? 😛"
                    )
            else:
                await bot.process_commands(message)

        bot.run(self.bot_token)


if __name__ == "__main__":
    load_dotenv()
    try:
        token = getenv("DISCORD_BOT_TOKEN")
        bot = DiscordBot(bot_token=token)
        bot.run()
    except ValueError as e:
        print(f"ERROR: {e}")
