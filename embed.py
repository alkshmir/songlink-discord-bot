import discord
import json

class MyEmbed(object):
    def __init__(self, title, description, url):
        with open("config.json", "r") as f:
            config = json.load(f)
        self.embed = discord.Embed.from_dict({
            "title": title, 
            "type": "rich", 
            "description": description,
            "url": url,
            "color": int(config["embed_color"], 16)}
        )
        self.embed.set_author(name=config["author"], icon_url=config["avater_image_url"])
    
    def add_field(self, name, value, inline=True):
        self.embed.add_field(name=name, value=value, inline=inline)