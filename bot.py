import os
import discord
from dotenv import load_dotenv
from objects import Carpool, User
from db import add_carpool, remove_carpool, add_passenger, remove_passenger, is_carpool, all_carpools, get_carpool

load_dotenv()
discord.http.API_VERSION = 9
bot = discord.Bot()

guild_id = int(os.environ.get('GUILD_ID'))
token = os.environ.get('TOKEN')

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(description="create a new carpool", guild_ids=[guild_id])
async def new_carpool(ctx, event_name: discord.Option(str), capacity: discord.Option(int)):
    driver = User(str(ctx.author.id), ctx.author.nick)
    await ctx.respond("Creating Carpool...")

    embed = discord.Embed(title="Carpool", color=0xE5E242, description="A new carpool!")
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.add_field(name="Event", value=event_name)
    embed.add_field(name="Driver", value=driver.username)
    embed.set_footer(text="react with ⬆️ to join the carpool!")
    message = await ctx.send(embed=embed)

    message_id = str(message.id)
    carpool = Carpool(message_id, event_name, capacity, driver)
    print('creating carpool')
    add_carpool(carpool)


@bot.slash_command(description="show all active carpools", guild_ids=[guild_id])
async def show_carpools(ctx):
    all_cp = all_carpools()
    embed = discord.Embed(title="All Carpools", color=0xE5E242, description="A list of all available carpools")

    if len(all_cp) == 0:
        
        await ctx.respond(embed=embed)
        return

    embed.set_thumbnail(url=ctx.author.display_avatar.url)

    for c in all_cp:
        event_name = c["event_name"]

        text = f'driver: {c["driver"]["username"]}\n' \
               f'{c["capacity"] - len(c["passengers"])} spaces left'

        if len(c["passengers"]) > 0:
            passengers = [x["username"] for x in c["passengers"]]
            p_string = ', '.join(passengers)
            text += f'\npassengers: {p_string}'
        embed.add_field(name=event_name, value=text)

    await ctx.respond(embed=embed)


@bot.event
async def on_raw_message_delete(payload):
    message_id = str(payload.message_id)
    if is_carpool(message_id):
        print('removing carpool')
        remove_carpool(message_id)


@bot.event
async def on_raw_reaction_add(payload):
    message_id = str(payload.message_id)
    name = str(payload.member.nick)
    user_id = str(payload.user_id)
    emoji = payload.emoji
    carpool = get_carpool(message_id)
    not_driver = carpool['driver']['user_id'] != user_id
    capacity = carpool["capacity"]

    if is_carpool(message_id) and \
            not_driver and \
            emoji.name == '⬆️' and \
            len(carpool["passengers"]) < capacity:
        print('add passenger')
        passenger = User(user_id, name)
        add_passenger(message_id, passenger)


@bot.event
async def on_raw_reaction_remove(payload):
    message_id = str(payload.message_id)
    user_id = str(payload.user_id)
    emoji = payload.emoji

    if is_carpool(message_id) and \
            emoji.name == '⬆️':
        print('remove passenger')
        remove_passenger(message_id, user_id)


bot.run(token)
