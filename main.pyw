import datetime
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import pytz
import schedule
import asyncio

load_dotenv()

#############################################################################
## Discord Configuration
#############################################################################

TOKEN = os.getenv('SPARKS_TOKEN')
ALLOWED_CHANNELS = ['bots', 'bot', 'bot-command', 'bot-spam']
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
client = commands.Bot(command_prefix='!', intents=intents)

sparks_url = 'https://www.bg-wiki.com/ffxi/Category:Sparks_Of_Eminence_Rewards'
acc_url = 'https://www.bg-wiki.com/ffxi/Category:Unity_Concord#Unity_Accolades'

#############################################################################
## Embed Configuration
#############################################################################

now = datetime.datetime.now()
footer_text = '© {year} - Created by Melucine@Bahamut'.format(year=now.year)

#############################################################################
## Bot comes online
#############################################################################

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await start_bot()

#############################################################################
## Logic to send the message every sunday
#############################################################################

async def start_bot():
    await start_daily_message()
    client.loop.create_task(check_schedule())

async def start_daily_message():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60) 

async def check_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

async def daily_message():
    now = datetime.datetime.now(pytz.timezone('Europe/Paris')) 
    
    if now.weekday() == 6 and now.hour == 15 and now.minute == 0:
         for guild in client.guilds:
            for channel_name in ALLOWED_CHANNELS:
                channel = discord.utils.get(guild.channels, name=channel_name)
                if channel is not None:
                    embed = discord.Embed(
                        title='Message from Isakoth',
                        description='',
                        color=0x808000)
                    embed.add_field(name='Attention adventurers! ⚔️🛡️', value='', inline=False)
                    embed.add_field(name='', value='', inline=False)
                    embed.add_field(name='', value=f'Just a friendly reminder that the [Sparks]({sparks_url}) & [Unity Accolades]({acc_url}) will reset in `1 hour` from now! Don\'t miss out on your chance to claim your rewards! 💰💰', inline=False)                     
                    embed.set_footer(text=footer_text)
                    await channel.send(embed=embed)
                else:
                    print(f"Channel '{channel_name}' not found or bot doesn't have permission to send messages in it")

schedule.every().sunday.at("15:00").do(lambda: asyncio.create_task(daily_message()))

#############################################################################
## Start the bot
#############################################################################

client.run(TOKEN)
