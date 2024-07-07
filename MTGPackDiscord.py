import discord
import random
import logging
import aiohttp
import os
import requests
import urllib.parse
from discord.ext import commands
from discord.ext.commands import BucketType, CommandOnCooldown
from dotenv import load_dotenv
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online!')


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'{bot.user.name}: {round(bot.latency * 1000)}ms')


@bot.group(invoke_without_command=True)
async def pull(ctx):
    embed_card = discord.Embed(
        title="Card Puller",
        description=f'{ctx.author.mention} Use command:\n.pull dm (Double Masters)\n.pull mh3 (Modern Horizons 3)\n.pull lotrc (LOTR: Tales of Middle-Earth Commander)\n.pull lotr (LOTR: Tales of Middle-Earth)',
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed_card)


#Double Masters
@pull.command(name='dm')
async def pull_dm(ctx):
    embed_card = discord.Embed(
        title="Card Pulled",
        description=f'{ctx.author.mention} pulled a card!',
        color=discord.Color.blue()
    )
    with open('MTGCards/double_masters.txt', 'r') as file:
        urls = file.readlines()
        random_url = random.choice(urls).strip()
        embed_card.set_image(url=random_url)

    await ctx.send(embed=embed_card)



#Modern Horizons 3
@pull.command(name='mh3')
async def pull_mh3(ctx):
    embed_card = discord.Embed(
        title="Card Pulled",
        description=f'{ctx.author.mention} pulled a card!',
        color=discord.Color.blue()
    )
    with open('MTGCards/MH3.txt', 'r') as file:
        urls = file.readlines()
        random_url = random.choice(urls).strip()
        embed_card.set_image(url=random_url)

    await ctx.send(embed=embed_card)


#LOTR: Tales of Middle-Earth Commander
@pull.command(name='lotrc')
async def pull_mh3(ctx):
    embed_card = discord.Embed(
        title="Card Pulled",
        description=f'{ctx.author.mention} pulled a card!',
        color=discord.Color.blue()
    )
    with open('MTGCards/LOTR_Commander.txt', 'r') as file:
        urls = file.readlines()
        random_url = random.choice(urls).strip()
        embed_card.set_image(url=random_url)

    await ctx.send(embed=embed_card)


#LOTR: Tales of Middle-Earth 
@pull.command(name='lotr')
async def pull_mh3(ctx):
    embed_card = discord.Embed(
        title="Card Pulled",
        description=f'{ctx.author.mention} pulled a card!',
        color=discord.Color.blue()
    )
    with open('MTGCards/LOTR.txt', 'r') as file:
        urls = file.readlines()
        random_url = random.choice(urls).strip()
        embed_card.set_image(url=random_url)

    await ctx.send(embed=embed_card)

@bot.command(name='avi')
async def avi(ctx):
    embed_card = discord.Embed(
        title="Card Pulled",
        description=f'{ctx.author.mention} pulled a card!',
        color=discord.Color.blue()
    )
    embed_card.set_image(url="https://cardmerchant.co.nz/cdn/shop/products/4efac807-954e-5e4e-ba9e-445bce58a82a_07d2537c-4820-40d9-8776-bc09b78448c5_800x.jpg?v=1655485857")
    await ctx.send(embed=embed_card)


#Card Search Feature
@bot.command(name='search')
async def search(ctx, *, card_name):
    search_url = f"https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[{urllib.parse.quote(card_name)}]"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                
                card_image_div = soup.find('div', class_='cardImage')
                if card_image_div:
                    img_src = card_image_div.find('img')['src']
                    if img_src.startswith('../../'):
                        img_src = urllib.parse.urljoin('https://gatherer.wizards.com/', img_src)
                    await ctx.send(img_src)
                else:
                    await ctx.send(f"Card image not found. Try this link: {search_url}/")
            else:
                await ctx.send("Failed to retrieve card information.")

    

bot.run(TOKEN)
