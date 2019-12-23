import discord
from discord.ext import commands
from googleapiclient import discovery

import os
import asyncio

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev_ip = None

        self.project = os.getenv('GCP_PROJECT')
        self.zone = os.getenv('GCE_ZONE')
        self.instance = os.getenv('GCE_INSTANCE')
        self.master = os.getenv('MASTER_ID')

    @commands.group(name='mc')
    async def mc(self, ctx):
        if ctx.invoked_subcommand is None:
                await ctx.send('使い方: /mc [open|close|status]')

    @mc.command(name='open')
    async def server_open(self, ctx):
        compute = discovery.build('compute', 'v1')
        await ctx.send('OK! インスタンスが立ち上がるまでしばらくお待ち下さい…\nサーバーの起動には5分程度かかるので、ゆっくり待っててください :tea:')
        await start(compute, self.project, self.zone, self.instance)
        await asyncio.sleep(20)
        status = await get_status(compute, self.project, self.zone, self.instance)
        now_ip = status['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        await self.bot.change_presence(
            status = discord.Status.online,
            activity = discord.Activity(
                name = 'MC server on {}'.format(now_ip),
                type = discord.ActivityType.playing,
                state = 'hello',
                details = 'on ' + now_ip
            )
        )

        if now_ip == self.prev_ip:
            await ctx.send('前回と同じIPなので、このまま遊べます！')
        else:
            await ctx.send('新しいアクセスポイントは{}です。'.format(now_ip))

        self.prev_ip = now_ip

    @mc.command(name='close')
    async def server_close(self, ctx):
        compute = discovery.build('compute', 'v1')
        await ctx.send('OK! インスタンスが落ちてなさそうならもう1度実行してください。')
        await stop(compute, self.project, self.zone, self.instance)
        await asyncio.sleep(10)
        await self.bot.change_presence(status=discord.Status.idle)

    @mc.command(name='status')
    async def server_status(self, ctx):
        compute = discovery.build('compute', 'v1')
        res = await get_status(compute, self.project, self.zone, self.instance)
        status = res['status']

        if status == 'RUNNING':
            await ctx.send('インスタンスは立ち上がっています！つながらない場合はサーバーの起動中です。　もうしばらくお待ち下さい…')
            await self.bot.change_presence(
            status = discord.Status.online,
            activity = discord.Activity(
                name = 'MC server on {}'.format(self.prev_ip),
                type = discord.ActivityType.playing,
                state = 'hello',
                details = 'on ' + self.prev_ip
            )
        )
        elif status == 'TERMINATED':
            await ctx.send('インスタンスは停止しています。openしてminecraftで遊びましょう！')
            await self.bot.change_presence(status=discord.Status.idle)
        elif status == 'STOPPING':
            await ctx.send('インスタンスは停止中です。　安心して寝てください！')
            await self.bot.change_presence(status=discord.Status.idle)
        else:
            await ctx.send('管理者が把握していない状態 {} です。　しばらくしてからもう1度お試しください。'.format(status))

def setup(bot):
    bot.add_cog(Server(bot)) #cogの登録


async def start(c, p, z, i):
    c.instances().start(project = p, zone = z, instance = i).execute()

async def stop(c, p, z, i):
    c.instances().stop(project = p, zone = z, instance = i).execute()

async def get_status(c, p, z, i):
    res = c.instances().get(project = p, zone = z, instance = i).execute()
    return res
