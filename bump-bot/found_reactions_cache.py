from typing import Dict, List
import discord

import config
import discord_client

FoundReactions = Dict[str, List[discord.Member]]

found_reactions_cache: Dict[int, FoundReactions] = {}

def get_emoji_string(emoji):
	if isinstance(emoji, discord.Emoji):
		return "{}".format(emoji.name)
	return emoji

async def get_found_reactions(message: discord.Message):
	if message.id in found_reactions_cache:
		return found_reactions_cache[message.id]

	found_reactions = {}
	for reaction in message.reactions:
		emoji_string = get_emoji_string(reaction.emoji)
		if emoji_string in config.get_reactions():
			users = [user async for user in reaction.users()]
			users.remove(discord_client.get_client().user)
			found_reactions[emoji_string] = users
	
	found_reactions_cache[message.id] = found_reactions
	return found_reactions

def initialize_found_reactions(message: discord.Message):
	found_reactions = {}
	for emoji_string in config.get_reactions():
		found_reactions[emoji_string] = []
	found_reactions_cache[message.id] = found_reactions

def add_found_reaction(message_id: int, emoji: discord.PartialEmoji, member: discord.Member):
	if message_id in found_reactions_cache:
		found_reactions_cache[message_id][emoji.name].append(member)

def remove_found_reaction(message_id: int, emoji: discord.PartialEmoji, member: discord.Member):
	if message_id in found_reactions_cache:
		found_reactions_cache[message_id][emoji.name].remove(member)