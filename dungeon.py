from creature import Creature
from discord.ext import commands
import time
import random


class DungeonRun:
    def __init__(self, pc: Creature, ctx: commands.Context):
        self.ctx = ctx
        self.message_space = None
        self.pc = pc
        self.pc.initialize_HP()

        self.npc: Creature = None
        self.current_floor = 1
        self.round_num = None
        self.round_detail = {
            "pc": {"hp_start": None, "dmg_tkn": None, "end_chk": None, "rec_amt": None},
            "npc": {
                "hp_start": None,
                "dmg_tkn": None,
                "end_chk": None,
                "rec_amt": None,
            },
        }

    def round_begin_phase(self):
        self.round_detail["pc"]["hp_start"] = self.pc.cur_hp
        self.round_detail["npc"]["hp_start"] = self.npc.cur_hp

    def attack_phase(self):
        pc_dmg_to_npc = self.pc.roll_dice("ATK")
        self.npc._apply_dmg(pc_dmg_to_npc)
        self.round_detail["npc"]["dmg_tkn"] = pc_dmg_to_npc

        npc_dmg_to_pc = self.npc.roll_dice("ATK")
        self.pc._apply_dmg(npc_dmg_to_pc)
        self.round_detail["pc"]["dmg_tkn"] = npc_dmg_to_pc

    def recovery_phase(self):

        self.round_detail["pc"]["end_chk"] = self.pc.roll_dice("END")
        if self.round_detail.get("pc").get("end_chk") >= self.round_detail.get(
            "pc"
        ).get("dmg_tkn"):
            self.round_detail["pc"]["rec_amt"] = self.pc.recover()

        self.round_detail["npc"]["end_chk"] = self.npc.roll_dice("END")
        if self.round_detail.get("npc").get("end_chk") >= self.round_detail.get(
            "npc"
        ).get("dmg_tkn"):
            self.round_detail["npc"]["rec_amt"] = self.npc.recover()

    async def output_round(self):
        # Determine max column length based on the longest name
        max_col_len = max(len(self.pc.name), len(self.npc.name))

        # Format numerical details with right alignment within each column
        format_str = f"{{:<{max_col_len}}} {{:>{max_col_len}}}"

        # Compile formatted output string
        out = f"""```
        {self.pc.name:<{max_col_len}} (Max HP: {self.pc.max_hp}) | {self.npc.name:<{max_col_len}}
        {'-' * max_col_len} | {'-' * max_col_len}
        {format_str.format('Starting HP', self.round_detail['pc']['hp_start'])} | {format_str.format('Starting HP', self.round_detail['npc']['hp_start'])}
        {format_str.format('DMG Taken', self.round_detail['pc']['dmg_tkn'])} | {format_str.format('DMG Taken', self.round_detail['npc']['dmg_tkn'])}
        {format_str.format('Endurance Check', self.round_detail['pc']['end_chk'])} | {format_str.format('Endurance Check', self.round_detail['npc']['end_chk'])}
        {format_str.format('Recovery Amt', str(self.round_detail['pc']['rec_amt']))} | {format_str.format('Recovery Amt', str(self.round_detail['npc']['rec_amt']))}
        {format_str.format('Ending HP', self.pc.cur_hp)} | {format_str.format('Ending HP', self.npc.cur_hp)}
        
        **Round Count: {self.round_num}**
        ```"""
        await self.message_space.edit(content=out)

    async def do_round(self):
        self.round_begin_phase()
        self.attack_phase()
        self.recovery_phase()
        await self.output_round()
        self._reset_round_detail()

    async def start(self):
        self.message_space = await self.ctx.send(
            content=f"{self.pc.name} will begin **Floor {self.current_floor}** in a moment"
        )
        time.sleep(3)

        while True:
            # Generate NPC
            self.npc = self.generate_opponent_npc()
            self.round_num = 1
            while self.npc.is_alive and self.pc.is_alive:
                self.round_num += 1
                await self.do_round()
                time.sleep(3)

            if not self.pc.is_alive:
                break

            self.current_floor += 1
            free_recovery = self.pc.recover()
            await self.ctx.send(
                content=f"{self.pc.name} recovered {free_recovery} after defeating {self.npc.name}!",
                delete_after=3,
            )
            time.sleep(3)

    def generate_opponent_npc(self) -> Creature:
        npc_dice = self.generate_npc_stats()
        npc_name = self.generate_npc_name()
        npc = Creature(npc_name, npc_dice)
        npc.initialize_HP()
        return npc

    def generate_npc_name(self) -> str:
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
        return f"The {random.choice(npc_nouns)} of Floor {self.current_floor}"

    def generate_npc_stats(self):
        """
        Generate NPC stats for a given level.
        Returns the stats in terms of dice
        """

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

        # Define base stat ranges for NPCs
        base_stats = {"ATK": (1, 2), "HP": (1, 5), "END": (1, 2), "REC": (1, 1)}
        stats_int = {}
        for stat, (base_min, base_max) in base_stats.items():
            stats_int[stat] = scale_stat(base_min, base_max, self.current_floor)

        return stats_int_to_dice(stats_int)

    def _reset_round_detail(self):
        self.round_detail = self.round_detail = {
            "pc": {"hp_start": None, "dmg_tkn": None, "end_chk": None, "rec_amt": None},
            "npc": {
                "hp_start": None,
                "dmg_tkn": None,
                "end_chk": None,
                "rec_amt": None,
            },
        }
