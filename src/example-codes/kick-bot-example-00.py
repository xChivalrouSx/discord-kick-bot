import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

client = discord.Client()

@client.event
async def on_ready():
	######### CODE - 01 #########
	# for guild in client.guilds:
	# 	print(guild.name)
	# 	print(guild.id)
	# 	print("------------")
	# 	if guild.name == GUILD:
	# 		break
	######### CODE - 02 #########
	# guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
	######### CODE - 03 #########
	guild = discord.utils.get(client.guilds, name=GUILD)

	print(
		f'{client.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})\n'
	)

	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members:\n - {members}')

# class CustomClient(discord.Client):
# 	async def on_ready(self):
# 		print(f'{self.user} has connected to Discord!')

# client = CustomClient()

@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to my Discord server!'
	)

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	brooklyn_99_quotes = [
		'I\'m the human form of the 💯 emoji.',
		'Bingpot!',
		(
			'Cool. Cool cool cool cool cool cool cool, '
			'no doubt no doubt no doubt no doubt.'
		),
	]

	if message.content == '99!':
		response = random.choice(brooklyn_99_quotes)
		await message.channel.send(response)

client.run(TOKEN)
