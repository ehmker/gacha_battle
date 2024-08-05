#!/usr/bin/env python3
import discord
import os
import psycopg
import actions
from discord.ext import commands
from dotenv import load_dotenv
from database import Database
from creature import Creature
import yaml

test_creature = Creature(
    "TEST_CREATURE",
    {"HP": {"d20": 3}, "ATK": {"d20": 1}, "END": {"d6": 1}, "REC": {"d20": 1}},
)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
db = Database()

# Setup Bot
description = (
    """A bot created with the intention of building a Gacha style Autobattler"""
)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix=["/", "!"], description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    db.load_init_file("initialize_tables.sql")


@bot.event
async def on_member_join(member):
    print(f"User {member.name} has joined the server")
    db.add_new_user(member.name)


@bot.command()
async def ping(ctx):
    await actions.dungeon_run(test_creature, ctx)


@bot.command()
async def attack(ctx, target):
    await ctx.send(f"\n:game_die: {ctx.author} attacks {target}")


@bot.command()
async def roll(ctx):
    user_info = db.get_user_info(1)
    await ctx.send(f"fetched info: {user_info}")


@bot.command()
async def start(ctx):
    user_info = db.get_user_info_by_name(ctx.author.name)

    # c = creature.Generate_New_Creature()
    # await ctx.send("New Creature Generated")
    # await ctx.send(str(c))


bot.run(TOKEN)
