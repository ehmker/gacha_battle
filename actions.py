from creature import Creature
from discord.ext import commands
from dungeon import DungeonRun
import time
import random


async def dungeon_run(pc: Creature, ctx: commands.Context):
    run = DungeonRun(pc, ctx)
    await run.start()
    # pc.initialize_HP()
    # lvl = 1
    # message_space = await ctx.send(
    #     content=f"Starting dungeon.  **{pc.name}** will begin **Floor 1** in *~5 seconds*",
    #     silent=True,
    # )
    # time.sleep(5)
    # await message_space.edit(content="Now begining the event")
    # while True:

    #     npc = generate_opponent_npc(lvl)
    #     while npc.is_alive and pc.is_alive:
    #         dmg_results = pc.attack(npc)

    #         if not pc.is_alive:
    #             print(f"{pc.name} was defeated by {npc.name} on floor {lvl}")
    #             break
    #         pc_rec_results = pc.recover()
    #         npc_rec_results = npc.recover()

    #     lvl += 1
