from discord.ext.commands import Cog, command
from datetime import datetime
from ..utils.web_scraping import WebScraper


class BotCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.web_scraper = WebScraper()

    @command(name="all")
    async def fetch_all(self, ctx, company_name: str):
        """Fetches the entire insider trading data for a company."""
        try:
            insider_data = self.web_scraper.fetch_all_insider_data(company_name)
            await ctx.send(f"Insider trading data for {company_name}:\n{insider_data}")
        except Exception as e:
            await ctx.send(f"Error fetching data: {e}")

    @command(name="latest")
    async def fetch_latest(self, ctx, company_name: str):
        """Fetches the latest 5 insider trading data points for a company."""
        try:
            latest_data = self.web_scraper.fetch_latest_insider_data(company_name, 5)
            await ctx.send(
                f"Latest 5 insider trading entries for {company_name}:\n{latest_data}"
            )
        except Exception as e:
            await ctx.send(f"Error fetching data: {e}")

    @command(name="weekday")
    async def get_weekday(self, ctx, date_str: str):
        """Fetches the day of the week for a given date (format: YYYY/MM/DD)."""
        try:
            # Parse the date string into a datetime object
            date_obj = datetime.strptime(date_str, "%Y/%m/%d")
            # Get the full name of the weekday
            weekday = date_obj.strftime("%A")
            await ctx.send(f"The date {date_str} falls on a {weekday}.")
        except ValueError:
            await ctx.send("Please provide the date in YYYY/MM/DD format.")
