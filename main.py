import discord
import asyncio
import random
import cgi
import sys
from clever import Cleverbot
from helpers import *
import os
from selenium import webdriver

client = discord.Client()

options = None
if 'DYNO' in os.environ:
    chrome_driver = CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

    chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_bin
    options.add_argument('headless')
    options.add_argument("--no-sandbox")
    options.add_argument('window-size=1366x768')

cb = Cleverbot(options=options)

total_sent = 0

args = sys.argv
if len(args) <= 1:
    print("Please pass account.txt file..")
    sys.exit(1)

user_token = None
email = None
password = None
server_channel = None

with open(sys.argv[1]) as f:
    content = f.readlines()
    if len(content) == 2:
        user_token = content[0].strip()
    else:
        email = content[0].strip()
        password = content[1].strip()
    server_channel = content[-1].strip()

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+')')

@client.event
async def on_message(message):
    if not message.author.id == client.user.id and cb.done is True and message.channel.id == server_channel:
        txt = message.content.replace(message.server.me.mention,'') if message.server else message.content
        txt = tag_re.sub('', txt)
        txt = emoji_pattern.sub(r'', txt)
        txt = cgi.escape(txt)

        delay = random.uniform(0.5, 1.5)
        await asyncio.sleep(delay)
        await client.send_typing(message.channel)
        delay = random.uniform(0.5, 1.5)
        await asyncio.sleep(delay)

        if len(txt) > 0:
            resp = await cb.send_message(txt)
        else:
            resp = await cb.send_message("qwertyuiop")
        if resp is False:
            return

        resp = resp.lower()

        if resp[-1] == ".":
            resp = resp[:-1]

        if "clever" in resp or "cleverbot" in resp:
            resp = "lol"

        print(message.author.name + ": " + txt)
        print(client.user.name + ": " + resp)

        await client.send_message(message.channel, resp)
        global total_sent
        total_sent += 1
        if total_sent >= 500:
            print("sent 500 messages, sleeping..")
            sys.exit(0)

print('\nStarting...')
if not user_token is None:
    client.run(user_token, bot=False)
elif not email is None:
    client.run(email, password, bot=False)