import requests
from bs4 import BeautifulSoup
import discord
import os
from discord.ext import commands

discord_token = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

proxy_username = 'geonode_u11gySF6E0'
proxy_password = '2c51f9a3-438d-4982-92c7-d694701bf8ec'

proxy = {
    'http':f'http://{proxy_username}:{proxy_password}@premium-residential.geonode.com:9000', 
    }

def get_url(web_country):
    if web_country == 'hk':
        url = 'https://www.hermes.com/hk/en/category/women/bags-and-small-leather-goods/bags-and-clutches/#|'
        return url
    elif web_country == 'us':
        url = 'https://www.hermes.com/us/en/category/women/bags-and-small-leather-goods/bags-and-clutches/#|'
        return url
    elif web_country == 'fr':
        url = 'https://www.hermes.com/fr/fr/category/femme/sacs-et-petite-maroquinerie/sacs-et-pochettes/#|'
        return url
    elif web_country == 'jp':
        url = 'https://www.hermes.com/jp/ja/category/women/bags-and-small-leather-goods/bags-and-clutches/#|'
        return url
    else:
        return 'Not an available store!'

def proxy_request(url):
    i = 0
    while i <= 5:
        i += 1
        response = requests.get(url, proxies=proxy, timeout=5)
        if response.status_code == 200:
            print(f"Proxy currently being used: {proxy}")
            break
        else:        
            print('Error, trying to reconnect website')
    return response

def scrap_bags(store_url):
    
    bag_meta = []
    re = proxy_request(store_url)
    
    soup = BeautifulSoup(re.content, "html.parser")

    # Find the picture container
    pic_list = soup.find_all("picture")

    # Find the name container
    meta_list = soup.find_all("div",{"class":"product-item-meta"})

    for pic, meta in zip(pic_list, meta_list):
        name = meta.find('span', {"class":"product-item-name"}).text
        price = meta.find('span', {"class": "price price-color medium"}).text
        title = name + price
        src = pic.find('img').get('src')
        img_url = "https:" + src
        bag_meta.append((title, img_url))
    
    return bag_meta

    
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')

# /hk command
@bot.tree.command(name="hk", description="Browse Hermes Hong Kong")
async def hk_slash_command(interaction:discord.Interaction):

    await interaction.response.send_message(f'You are viewing the bags in Hong Kong online store!')

    view_url = get_url('hk')
    meta_data = scrap_bags(view_url)

    embedList = []
        
    for item in meta_data:

        # Construct the embed which will be sent to Discord
        embed = discord.Embed(title=item[0], description=f"Here are the bags picture from the Hermes website! If you want to buy it, please go to {view_url}")
        embed.set_image(url=item[1])

        embedList.append(embed)

    # Split the list of embeds into chunks of maximum 10 embeds
    for chunk in chunks(embedList, 10):
        # Send a message with a chunk of embeds
        await interaction.followup.send(embeds=chunk)

# /us command
@bot.tree.command(name="us", description="Browse Hermes US")
async def us_slash_command(interaction:discord.Interaction):
    
    await interaction.response.send_message(f'You are viewing the bags in US online store!')

    view_url = get_url("us")
    meta_data = scrap_bags(view_url)

    embedList = []
        
    for item in meta_data:

        # Construct the data format which will be sent to Discord
        embed = discord.Embed(title=item[0], description=f"Here are the bags picture from the Hermes website! If you want to buy it, please go to {view_url}")
        embed.set_image(url=item[1])

        embedList.append(embed)
    
    # Split the list of embeds into chunks of maximum 10 embeds
    for chunk in chunks(embedList, 10):
        # Send a message with a chunk of embeds
        await interaction.followup.send(embeds=chunk)

# /jp command
@bot.tree.command(name="jp", description="Browse Hermes Japan")
async def jp_slash_command(interaction:discord.Interaction):

    await interaction.response.send_message(f'You are viewing the bags in Japan online store!')

    view_url = get_url('jp')
    meta_data = scrap_bags(view_url)

    embedList = []
        
    for item in meta_data:

        # Construct the data format which will be sent to Discord
        embed = discord.Embed(title=item[0], description=f"Here are the bags picture from the Hermes website! If you want to buy it, please go to {view_url}")
        embed.set_image(url=item[1])

        embedList.append(embed)
    
    # Split the list of embeds into chunks of maximum 10 embeds
    for chunk in chunks(embedList, 10):
        # Send a message with a chunk of embeds
        await interaction.followup.send(embeds=chunk)
    

@bot.tree.command(name="fr", description="Browse Hermes France")
async def de_slash_command(interaction:discord.Interaction):
    await interaction.response.send_message('You are viewing the bags in France online store!')

    view_url = get_url('fr')
    meta_data = scrap_bags(view_url)

    embedList = []
        
    for item in meta_data:

        # Construct the data format which will be sent to Discord
        embed = discord.Embed(title=item[0], description=f"Here are the bags picture from the Hermes website! If you want to buy it, please go to {view_url}")
        embed.set_image(url=item[1])

        embedList.append(embed)
    
    # Split the list of embeds into chunks of maximum 10 embeds
    for chunk in chunks(embedList, 10):
        # Send a message with a chunk of embeds
        await interaction.followup.send(embeds=chunk)
    
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

bot.run(discord_token)





