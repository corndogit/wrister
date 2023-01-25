import os
import disnake
import json
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
wrister = commands.Bot(
    command_prefix=disnake.ext.commands.when_mentioned,
    command_sync_flags=commands.CommandSyncFlags.default()
)


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
                    inline=False)
    await inter.response.send_message(embed=embed)


@wrister.slash_command(description="Dev tool for testing that exercises can be fetched")
async def test(inter):
    with open("wrister/assets/data/exercises.json") as file:
        exercise = json.loads(file.read())["exercises"][0]
    embed = disnake.Embed(
        title=exercise['title'],
        url=exercise['video_url'],
        color=0x0080ff
    )
    embed.set_author(name="Wrister", icon_url=wrister.user.display_avatar)
    embed.add_field(name="Instructions", value=exercise['description'], inline=False)
    for number, step in enumerate(exercise['instructions'], 1):
        embed.add_field(name=f"Step {number}", value=step, inline=False)
    embed.set_footer(text=f"Click \"{exercise['title']}\" to see a video tutorial")
    await inter.response.send_message(embed=embed)


@wrister.slash_command(description="Detailed information on how to do a certain exercise")
async def howto(inter, exercise_number: str):
    invalid_message = "Invalid exercise ID. Usage: `/howto <exercise_number>`"

    # return immediately if exercise is not a number
    if not exercise_number.isnumeric():
        await inter.response.send_message(invalid_message)
        return

    with open("wrister/assets/data/exercises.json") as file:
        exercises = json.loads(file.read())["exercises"]

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
