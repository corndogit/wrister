import os
import disnake
import json
import random
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
EMBED_COLOR = 0x0080ff  # hex value for colour of the embed highlight
wrister = commands.Bot(
    command_prefix=disnake.ext.commands.when_mentioned,
    command_sync_flags=commands.CommandSyncFlags.default()
)
with open("wrister/assets/data/exercises.json") as file:
    exercises = json.loads(file.read())["exercises"]


@wrister.event
async def on_ready():
    print(f"{wrister.user} is now online!")


@wrister.slash_command(description="Responds with 'Hello there!'")
async def hello(inter):
    await inter.response.send_message("Hello there!")


@wrister.slash_command(description="Show information about Wrister")
async def about(inter):
    embed = disnake.Embed(
        title="About",
        url="https://github.com/corndogit",
        description="A bot reminding you to exercise your wrists."
    )
    embed.set_thumbnail(url=wrister.user.display_avatar)
    embed.add_field(name="Prefix", value="/")
    embed.add_field(name="Commands",
                    value="`hello`, `about`, `howto <exercise>`",
                    inline=False
                    )
    await inter.response.send_message(embed=embed)


@wrister.slash_command(description="Dev tool for testing that exercises can be fetched")
async def test(inter):
    exercise = exercises[0]
    embed = disnake.Embed(
        title=exercise['title'],
        url=exercise['video_url'],
        color=EMBED_COLOR
    )
    embed.set_author(name="Wrister", icon_url=wrister.user.display_avatar)
    embed.add_field(name="Instructions", value=exercise['description'], inline=False)
    for number, step in enumerate(exercise['instructions'], 1):
        embed.add_field(name=f"Step {number}", value=step, inline=False)
    embed.set_footer(text=f"Click \"{exercise['title']}\" to see a video tutorial")
    await inter.response.send_message(embed=embed)


@wrister.slash_command(description=f"Choose some random exercises (3 by default, between 1 and {len(exercises) - 1})")
async def set_of_exercises(inter, number_of_exercises: str = "3"):
    invalid_message = f"Invalid number of exercises. Must be a number in the range 1 to {len(exercises) - 1}"

    # return immediately if exercise is not a number
    if number_of_exercises and not number_of_exercises.isnumeric():
        await inter.response.send_message(invalid_message)
        return

    # return if exercise_id is not between 1 and total number of exercises
    elif int(number_of_exercises) < 1 or int(number_of_exercises) >= len(exercises):
        await inter.response.send_message(invalid_message)
        return

    # pick some random exercises
    exercise_indexes = list(range(1, len(exercises)))
    random.shuffle(exercise_indexes)

    # generate embed
    embed = disnake.Embed(
        title="Time to stretch those hands!",
        description="Here's your list of exercises to do.",
        color=0x0080ff
    )
    embed.set_author(name="Wrister", icon_url=wrister.user.display_avatar)
    for index in exercise_indexes[0:int(number_of_exercises)]:
        embed.add_field(name=f"Exercise #{index} - {exercises[index]['title']}", value="", inline=False)
    embed.set_footer(text=f"Type `/how_to <exercise #>` for more info about an exercise!")
    await inter.response.send_message(embed=embed)


@wrister.slash_command(description="Detailed information on how to do a certain exercise")
async def how_to(inter, exercise_number: str):
    invalid_message = "Invalid exercise ID. Usage: `/how_to <exercise_number>`"

    # return immediately if exercise is not a number
    if not exercise_number.isnumeric():
        await inter.response.send_message(invalid_message)
        return

    # return if exercise_id is not between 1 and total number of exercises
    index = int(exercise_number)
    if index < 1 or index >= len(exercises):
        await inter.response.send_message(invalid_message)
        return

    # generate embed
    embed = disnake.Embed(
        title=exercises[index]['title'],
        url=exercises[index]['video_url'],
        color=0x0080ff
    )
    embed.set_author(name="Wrister", icon_url=wrister.user.display_avatar)
    embed.add_field(name="Instructions", value=exercises[index]['description'], inline=False)
    for number, step in enumerate(exercises[index]['instructions'], 1):
        embed.add_field(name=f"Step {number}", value=step, inline=False)
    embed.set_footer(text=f"Click \"{exercises[index]['title']}\" to see a video tutorial")
    await inter.response.send_message(embed=embed)


wrister.run(TOKEN)
