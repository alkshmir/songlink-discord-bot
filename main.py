import discord 
import json
import os
import re
import requests

from embed import MyEmbed

with open("config.json", "r") as f:
    config = json.load(f)
    bot_token = config["discord_bot_token"]

client = discord.Client(ws= int(os.environ.get('PORT', 5000)))

@client.event
async def on_ready():
    print("ready.")


# convert apple music to other platforms
@client.event
async def on_message(message):
    keyToName = {"spotify": "Spotify", "youtube": "Youtube", "appleMusic":"Apple Music"}
    pattern = "https?://music.apple.com/[\w/:%#\$&\?\(\)~\.=\+\-]+"
    ap_music_url_list = re.findall(pattern, message.content)
    if not ap_music_url_list:
        return
    for url in ap_music_url_list:
        await message.add_reaction(discord.PartialEmoji.from_dict({"name":"↪️"}))
        

        songlink_query = "https://api.song.link/v1-alpha.1/links?url={}&userCountry=JP&key=".format(url)
        response = requests.get(songlink_query)
        js = response.json()
        
        pageURL = js["pageUrl"]
        for v in js["entitiesByUniqueId"].values():
            firstElement = v
            break
        songTitle    = firstElement['title']
        artistName   = firstElement['artistName']
        thumbnailURL = firstElement['thumbnailUrl']

        platforms = set(js["linksByPlatform"].keys()) & set(["spotify", "youtube", "appleMusic"])
        links = {}
        for pl in platforms:
            links[pl] = js["linksByPlatform"][pl]["url"]
        
        embed = MyEmbed("{} - {}".format(artistName, songTitle), "各プラットフォームへのリンクです。", pageURL)
        embed.embed.set_thumbnail(url=thumbnailURL)

        for pl in platforms:
            #embed.add_field(name=keyToName[pl], value=links[pl], inline=False)
            embed.add_field(name=keyToName[pl], value="[{}]({})".format(keyToName[pl], links[pl]), inline=False)

        await message.channel.send(embed=embed.embed)
    

client.run(bot_token)
