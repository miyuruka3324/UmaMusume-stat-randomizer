import discord
from discord.ext import commands
import random
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# 1. Setup Bot Intents and PPrefix
intents = discord.Intents.default()
intents.message_content = True  # Required to read commands
bot = commands.Bot(command_prefix='!', intents=intents)

# 2. The Logic: Weighted Randomizer
def get_random_stats():
    std_ranks = ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
    std_weights = [2, 10, 25, 25, 15, 10, 8, 5]
    surface_ranks = ['A', 'B', 'F']

    def pick_std():
        return random.choices(std_ranks, weights=std_weights)[0]

    # --- 1. Surface Logic (Must have at least one A) ---
    surf_keys = ["Turf", "Dirt"]
    surface = {k: random.choice(surface_ranks) for k in surf_keys}
    
    if 'A' not in surface.values():
        forced_surf = random.choice(surf_keys)
        surface[forced_surf] = 'A'

    # --- 2. Distance Logic (At least one A) ---
    dist_keys = ["Short", "Mile", "Medium", "Long"]
    distance = {k: pick_std() for k in dist_keys}
    
    if 'A' not in distance.values():
        forced_dist = random.choice(dist_keys)
        distance[forced_dist] = 'A'

    # --- 3. Strategy Logic (At least one A) ---
    strat_keys = ["Front", "Pace", "Late", "End"]
    strategy = {k: pick_std() for k in strat_keys}

    if 'A' not in strategy.values():
        forced_strat = random.choice(strat_keys)
        strategy[forced_strat] = 'A'

    return {
        "Surface": surface,
        "Distance": distance,
        "Strategy": strategy
    }

@bot.command(name="randomize")
async def randomize(ctx):
    data = get_random_stats()

    embed = discord.Embed(
        title="🏇 Character Aptitude",
        description="Every character now has a **Primary Specialty** in all categories!",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="🟦 Surface", 
        value=f"**Turf:** {data['Surface']['Turf']} | **Dirt:** {data['Surface']['Dirt']}", 
        inline=False
    )
    
    embed.add_field(
        name="🟩 Distance", 
        value=f"**Short:** {data['Distance']['Short']} | **Mile:** {data['Distance']['Mile']}\n"
              f"**Medium:** {data['Distance']['Medium']} | **Long:** {data['Distance']['Long']}", 
        inline=False
    )

    embed.add_field(
        name="🟧 Strategy", 
        value=f"**Front:** {data['Strategy']['Front']} | **Pace:** {data['Strategy']['Pace']}\n"
              f"**Late:** {data['Strategy']['Late']} | **End:** {data['Strategy']['End']}", 
        inline=False
    )

    await ctx.send(embed=embed)
    embed.set_footer(text=f"Requested by {ctx.author.display_name}")

    await ctx.send(embed=embed)

# 4. Run the Bot
# Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token from the Discord Developer Portal
bot.run(token, log_handler=handler, log_level=logging.DEBUG)