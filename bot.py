#!/usr/bin/python3

import asyncio
import os
import traceback

import discord
from googleapiclient import discovery
from discord.ext import commands

BOT_TOKEN = os.getenv('BOT_TOKEN')

INIT_EXT = [
    'cogs.manage',
    'cogs.debug'
]

compute = discovery.build('compute', 'v1')

class MC_Server(commands.Bot):
    def __init__(self, command_prefix):
        # super class constructor
        super().__init__(command_prefix)

        # loading cogs in INIT_EXT list
        for cog in INIT_EXT:
            try:
                self.load_extension(cog)
            except Exception:
                print('cog loading error.')
                traceback.print_exc()




    async def on_ready(self):
        print('Bot logged in.')
        await self.change_presence(status=discord.Status.idle)
        self.prev_ip = None


if __name__ == '__main__':
    bot = MC_Server(command_prefix='/')
    bot.run(BOT_TOKEN)

