import discord
from discord.ext import commands
import asyncio
import requests
import json
import random

bot = commands.Bot(command_prefix="!@#$%^&*()", self_bot=True)

user = 'R8N8u173I12C9BIN'
key = 'FL1Adqmjq2VDvVFVEdpivciKnaW9zWfo'

@bot.event
async def on_ready():
    print('Logged in as '+bot.user.name+' (ID:'+bot.user.id+') | '+str(len(bot.servers))+' servers')

@bot.event
async def on_message(message):
    if not message.author.id == "465203839621136385" and len(message.mentions) == 0:
        #await bot.send_typing(message.channel)
        txt = message.content
        print("text:" + txt)
        r = json.loads(requests.post('https://cleverbot.io/1.0/ask', json={'user':user, 'key':key, 'nick':'mycxle', 'text':txt}).text)
        if r['status'] == 'success':
            print("response: " + r['response'])
            await bot.send_message(message.channel, r['response'] )

print('Starting...')
requests.post('https://cleverbot.io/1.0/create', json={'user':user, 'key':key, 'nick':'mycxle'})
bot.run("NDY1MjAzODM5NjIxMTM2Mzg1.Dl3_iw.30LO973wUNKkrJ9wuXgkEB4VJ2c", bot=False)