from creature import Creature
from discord.ext import commands
import time
import random


async def dungeon_run(player_one: Creature, ctx: commands.Context):
    player_one.initialize_HP()
    lvl = 1

    while True:
        npc = generate_opponent_npc(lvl)
        while npc.is_alive and player_one.is_alive:
            player_one.attack(npc)

        if not player_one.is_alive:
            print(f"{player_one.name} was defeated by {npc.name} on floor {lvl}")
            break

        lvl += 1


def run_round():
    pass


def generate_opponent_npc(difficulty_level: int) -> Creature:
    npc_dice = generate_npc_stats(difficulty_level)
    npc_name = generate_npc_name(difficulty_level)
    npc = Creature(npc_name, npc_dice)
    npc.initialize_HP()
    return npc


def generate_npc_name(lvl: int) -> str:
    npc_nouns = [
        "mob",
        "monster",
        "ghoul",
        "doctor",
        "vampire",
        "wolf",
        "giant",
        "wisp",
        "skeleton",
    ]
    return f"The {random.choice(npc_nouns)} of Floor {lvl}"


def generate_npc_stats(difficulty_level: int):
    """
    Generate NPC stats for a given level.
    Returns the stats in terms of dice
    """
    # Define base stat ranges for NPCs
    base_stats = {"ATK": (1, 2), "HP": (1, 5), "END": (1, 2), "REC": (1, 1)}
    stats_int = {}
    for stat, (base_min, base_max) in base_stats.items():
        stats_int[stat] = scale_stat(base_min, base_max, difficulty_level)
    return stats_int_to_dice(stats_int)


def scale_stat(base_min, base_max, level):
    """
    Scale a stat based on the level using an exponential function.
    """
    # Increase the range of possible values as the level increases
    scale_factor = 1.025  # You can adjust the scale factor to tune difficulty
    min_stat = base_min * (scale_factor**level)
    max_stat = base_max * (scale_factor**level)

    # Generate a stat within the new range, weighted towards the lower end
    stat = random.triangular(min_stat, max_stat, min_stat)
    return int(stat)


def stats_int_to_dice(stats_int: dict) -> dict:
    dice_vals = {
        0: "0",
        1: "d4",
        2: "d6",
        3: "d8",
        4: "d10",
        5: "d12",
    }
    stats_dice = {}
    for attribute, stat_val in stats_int.items():
        stats_dice[attribute] = {}
        num_d20 = stat_val // 6
        remainder_die = stat_val % 6
        if num_d20 > 0:
            stats_dice[attribute]["d20"] = num_d20

        if remainder_die > 0:
            stats_dice[attribute][dice_vals[remainder_die]] = 1

    return stats_dice
