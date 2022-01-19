import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_SERVER')
MESSAGE_CHANNEL = os.getenv('MESSAGE_CHANNEL')
KICK_CHANNEL = os.getenv('KICK_VOICE_CHANNEL')
KICK_MESSAGE = os.getenv('KICK_MESSAGE')
KICK_PRIVATE_MESSAGE = os.getenv('KICK_PRIVATE_MESSAGE')

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.offline)

@client.event
async def on_voice_state_update(member, before, after):
	if (after.channel != None) and (after.channel.name == KICK_CHANNEL):
		guild = discord.utils.get(client.guilds, name=SERVER_NAME)
		channel = discord.utils.get(guild.channels, name=MESSAGE_CHANNEL)
		
		if (not member.guild_permissions.administrator) and (not member.guild_permissions.ban_members):
			kick_message = member.name + " kicked!.. \n" + KICK_MESSAGE

			await member.send(kick_message + "\n" + KICK_PRIVATE_MESSAGE)
			await channel.send(kick_message)
			await member.kick()

client.run(TOKEN)
