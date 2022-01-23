import os

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_SERVER')
MESSAGE_CHANNEL = os.getenv('MESSAGE_CHANNEL')
KICK_CHANNEL = os.getenv('KICK_VOICE_CHANNEL')
KICK_MESSAGE = os.getenv('KICK_MESSAGE')
KICK_PRIVATE_MESSAGE = os.getenv('KICK_PRIVATE_MESSAGE')

DAILY_MESSAGE_TIME = os.getenv('DAILY_MESSAGE_TIME')
DAILY_MESSAGE_CHANNEL = os.getenv('DAILY_MESSAGE_CHANNEL')
DAILY_MESSAGE = os.getenv('DAILY_MESSAGE')

bot = commands.Bot(command_prefix = '.')

async def func():
	await bot.wait_until_ready()
	guild = discord.utils.get(bot.guilds, name=SERVER_NAME)
	message_channel = discord.utils.get(guild.channels, name=DAILY_MESSAGE_CHANNEL)
	print(f"Got channel {message_channel}")
	await message_channel.send(DAILY_MESSAGE)

@bot.event
async def on_ready():
	print("Ready")
	await bot.change_presence(status=discord.Status.offline)

	time_array = DAILY_MESSAGE_TIME.split(":")

	scheduler = AsyncIOScheduler()
	scheduler.add_job(func, CronTrigger(hour=time_array[0], minute=time_array[1], second=time_array[2])) 
	scheduler.start()

@bot.event
async def on_voice_state_update(member, before, after):
	if (after.channel != None) and (after.channel.name == KICK_CHANNEL):
		print("Change detected on kick channel...")

		guild = discord.utils.get(bot.guilds, name=SERVER_NAME)
		channel = discord.utils.get(guild.channels, name=MESSAGE_CHANNEL)
		
		if (not member.guild_permissions.administrator) and (not member.guild_permissions.ban_members):
			print("Member will be kicked soon...")

			kick_message = member.name + " kicked!.. \n" + KICK_MESSAGE
			await member.send(kick_message + "\n" + KICK_PRIVATE_MESSAGE)
			await channel.send(kick_message)
			await member.kick()

			print("Member kicked...")

bot.run(TOKEN)
