import os
import sys
import time
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv('~/.env')

args = sys.argv

mine_name = args[1]
uuid = args[2]
server = args[3]
reqserver = args[4]
reqspace = args[5]
bat = args[6]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)
reqchannel = int(os.getenv("REQ_CHANNEL"))
#reqchannel = int(os.getenv("TEST_CHANNEL"))

        # discord.ui.Button を継承し，callback 関数をオーバーライド
class YesButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        channelid = bot.get_channel(reqchannel)
        user_id = interaction.user.id
        mention = "<@" + str(user_id) + ">"
        msg = f"{mention}\n{reqserver}サーバーが起動します。"
        await channelid.send(msg)
        status = "start"
        os.system(f"start {bat}")
        os.system(f"php "+ str(os.getenv("PHP_DB_PATH")) + f" {mine_name} {uuid} {server} {reqserver} {reqspace} {status}")
        os.system(f"php "+ str(os.getenv("PHP_SOCKET_PATH")) + f" {mine_name} {uuid} {server} {reqserver} {reqspace} {status}")
        await asyncio.sleep(5)
        bot.close()
        sys.exit()
        
class NoButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        channelid = bot.get_channel(reqchannel)
        user_id = interaction.user.id
        mention = "<@" + str(user_id) + ">"
        msg = f"{mention}\n{reqserver}サーバーの起動をキャンセルしました。"
        await channelid.send(msg)
        status = "cancel"
        os.system(f"php "+ str(os.getenv("PHP_DB_PATH")) + f" {mine_name} {uuid} {server} {reqserver} {reqspace} {status}")
        os.system(f"php "+ str(os.getenv("PHP_SOCKET_PATH")) + f" {mine_name} {uuid} {server} {reqserver} {reqspace} {status}")
        await asyncio.sleep(5)
        bot.close()
        sys.exit()

@bot.command()
async def ping(ctx: commands.Context):
    view = discord.ui.View()
    yes_button = YesButton(label='Start', style=discord.ButtonStyle.green)
    view.add_item(yes_button)
    await ctx.send('pong', view=view)

@bot.event 
async def on_ready():
    channelid = bot.get_channel(reqchannel)
    view = discord.ui.View()
    yes_button = YesButton(label='Start', custom_id='yes',style=discord.ButtonStyle.green)
    view.add_item(yes_button)
    no_button = NoButton(label='Cancel',custom_id="no",style=discord.ButtonStyle.red)
    view.add_item(no_button)
    msg = f"{mine_name}さんが{reqserver}サーバーの起動リクエストを送信しました。起動しますか？"
    await channelid.send(msg, view=view)
    i=0
    while True:
        print(f"{i}分が経過")
        await asyncio.sleep(60)
        if i==3:
            status = "nores"
            os.system(f"php "+ str(os.getenv("PHP_DB_PATH")) + f" {mine_name} {uuid} {server} {reqserver} {reqspace} {status}")
            os.system(f"php "+ str(os.getenv("PHP_SOCKET_PATH")) + f" {mine_name} {uuid} {server} {reqserver} {reqspace} {status}")
            await asyncio.sleep(5)
            bot.close()
            sys.exit()
        i=i+1

if reqspace=="req0":
    token = str(os.getenv("DISCORD_REQ0_TOKEN"))
elif reqspace=="req1":
    token = str(os.getenv("DISCORD_REQ1_TOKEN"))
elif reqspace=="req2":
    token = str(os.getenv("DISCORD_REQ2_TOKEN"))

bot.run(token)
