import discord
import asyncio
import requests
import json
import random
import re, cgi

from clever import Cleverbot

client = discord.Client()

c = 0

@asyncio.coroutine
async def get_resp(txt, i):
    return await Cleverbot().send_message(txt, i)

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | '+str(len(client.servers))+' servers')

@client.event
async def on_message(message):
   # if message.server.id == "355493390378336267":
    #    return
    if not message.author.id == "481652009473277972" and Cleverbot.done is True and message.channel.id == "355493390378336267":
    #if not message.author.id == "465203839621136385" and Cleverbot.done is True and message.channel.id == "369944965629083652":
        txt = message.content.replace(message.server.me.mention,'') if message.server else message.content

        tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
        
        txt = txt.lower()

        txt = tag_re.sub('', txt)
        txt = cgi.escape(txt)

        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        txt = emoji_pattern.sub(r'', txt)

        print("length of text: " + str(len(txt)))

        if len(txt) == 0:
            txt = "ok"

        if "clever" in txt or "cleverbot" in txt:
            txt = "lol"

        delay = random.uniform(0.5, 2.5)
        await asyncio.sleep(delay)
        await client.send_typing(message.channel)
        delay = random.uniform(0.5, 3.5)
        await asyncio.sleep(delay)

        global c
        resp = await get_resp(txt, c)
        c += 1
        if c >= Cleverbot.num_drivers:
            c = 0
        if resp is False:
            print("resp was False")
            return
        resp = resp.lower()
        if resp[-1] == ".":
            resp = resp[:-1]
        await client.send_message(message.channel, resp)

print('Starting...')
client.run("NDgxNjUyMDA5NDczMjc3OTcy.Dl5hoA.eTidXIUD9IIsqmhh08tyA37E39c", bot=False)