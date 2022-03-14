import discord
import requests
import asyncio
import json
import re
import random
from bs4 import BeautifulSoup
# import youtube api file
from youtube import YoutubeAssistant



# Globals
# connect
bot = discord.Client()
TOKEN = "OTQ2OTcxMTEzMDkzNzU0OTEx.Yhmdkw.2rvIEFY9W6RLizfxEf2S8lrfYeA"

# dad joke api
url = "https://icanhazdadjoke.com/"

# load trigger words and funny responses from json file
f = open('./joke_data/funny_data.json')
funny_file = json.load(f)

funny_words = funny_file['funny_words']

funny_responses = funny_file['funny_responses']

youtube = YoutubeAssistant()

success_emoji = '👍🏾'
negative_emoji = '👎🏾'


# returns quote from api
def get_joke():

    """
    Retrieves a random dad joke from the icanhazdadjoke.com joke api.
    """
    response = requests.get(url)
    HTML = response.text
    soup = BeautifulSoup(HTML, features="html.parser")

    s = soup.getText().split("\n")
    # gets rid of parts we don't need
    data = list(filter(("").__ne__, s))
    
    joke = data[8]

    # return joke
    return joke

# checking
async def get_new_uploads():
    """
    Constantly checks for new uploads for channels in the channel.txt file.
    """
    
    await bot.wait_until_ready() # ensures cache is loaded
    channel = bot.get_channel(id=892163573948756019) # desired channel -> youtube uploads specific one
    while not bot.is_closed():

        vids_list = on_change()
        for vid in vids_list:
            if vid != "":
                await channel.send(vid) # only post if new video
        await asyncio.sleep(300) # 5 minutes

@bot.event
# calls when bot is ready to be used
async def on_ready():
    """
    First function that is called when a bot is being run.
    """
    # prints this
    print("We have logged in as {0.user}".format(bot))


    # constantly check every 5 mins for new uploads
    bot.loop.create_task(get_new_uploads())

@bot.event
async def on_message(msg):
    """
    Checks every message and responds to a supported command.
    """
    # triggers each time a msg is received
    # check if msg is from bot
    if msg.author == bot.user:
        return

    # else check for command 
    if msg.content.startswith("$joke"):
        # returns msg back to discord
        joke = get_joke()
        await msg.channel.send(joke)

    # ask for help 
    if msg.content.startswith("$ythelp"):

        await msg.channel.send("What is a channel id?\nA channel's id is the last portion of the" +
                            "url of the channel page.\n"+
                            "If a channel URL is: \"https://www.youtube.com/channel/UCiMr9kBgaBs9--eFW72Ok-A\""+
                            "\nthen the channel id for that channel is \"UCiMr9kBgaBs9--eFW72Ok-A\"")
         # else check for command 
    elif msg.content.startswith("$yt"):
        # returns msg back to discord
        extracted = msg.content.split()
        if len(extracted) == 2:
            channel_id = extracted[1]
            is_added = youtube.update_channel_info(channel_id)
            if is_added:
                await msg.add_reaction(success_emoji)
            else:
                await msg.add_reaction(negative_emoji)

        else:
            await msg.channel.send("Invalid channel id.\nExample: \"$yt {channel_id}\"")
            await msg.add_reaction(negative_emoji)

    # check if any funny words have been said( in msg)
    if any(word in msg.content for word in funny_words):
        # picks random word from our funny responses list
        await msg.channel.send(random.choice(funny_responses))

# constantly check for a change in channel json files
def on_change():
    """
        Function that checks whether or not a channel has
        uploaded a video after a given amount of time.
    """

    channels = youtube.get_channels()
    youtube.get_latest_video()
    new_vids = youtube.check_json()
    
    return new_vids

# called on exit
def close():
    """
    Closes all the open sockets, bots, and files when program ends.
    """

    bot.close()
    print("Bot terminated")
    youtube.close_socket()


bot.run(TOKEN)
# runs the bot

