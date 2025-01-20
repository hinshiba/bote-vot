import discord
from discord import app_commands
import dotenv
import os
intents = discord.Intents.default()
intents.message_content = True
# bot = commands.Bot(command_prefix="/", intents=intents)
client = discord.Client(intents=intents) 
tree = app_commands.CommandTree(client)


# vote_id = None
isvote = False
vote_stat = {}
vote_hook = None

# 登録絵文字
# YES = "<:berc:1308738819880779816>"
# NO = "<:bercw:1308738841099894854>"

# unicode絵文字
YES = "\u2B55"
NO = "\u274C"

MSG_VOTE_UI = "vote here; voted: "

dotenv.load_dotenv()

class VoteView(discord.ui.View):
    @discord.ui.button(label="OK", style=discord.ButtonStyle.success)
    async def ok(self, interaction: discord.Interaction, button: discord.ui.Button):
        global isvote
        vote_stat[interaction.user.id] = True
        # await interaction.response.send_message(f"{len(vote_stat)}")
        # await interaction.response.send_message("")
        await interaction.response.defer()
        try:
            await interaction.followup.send("")
        except discord.HTTPException as e:
            pass
        await vote_hook.edit(content=MSG_VOTE_UI + str(len(vote_stat)))

        

    @discord.ui.button(label="NG", style=discord.ButtonStyle.danger)
    async def ng(self, interaction: discord.Interaction, button: discord.ui.Button):
        global isvote
        vote_stat[interaction.user.id] = False
        # await interaction.response.send_message(f"{len(vote_stat)}")
        # await interaction.response.send_message("")
        await interaction.response.defer()
        try:
            await interaction.followup.send("")
        except discord.HTTPException as e:
            pass
        await vote_hook.edit(content=MSG_VOTE_UI + str(len(vote_stat)))




@client.event
async def on_ready():
    print(f"Botがログインしました: {client.user}")
    await tree.sync()

@tree.command(name="voteon",description="2択匿名投票の開始")
async def voteyon(interaction: discord.Interaction):
    global isvote
    global vote_stat
    global vote_hook
    await interaction.response.defer()
    if isvote:
        await interaction.followup.send(content="vote already started")
        return
    view = VoteView()
    vote_stat = {}
    vote_hook = await interaction.followup.send(content=MSG_VOTE_UI, view=view)
    isvote = True

# @bot.command()
# async def voteyn(ctx):
#     global vote_id
#     if vote_id:
#         await ctx.send(content="vote already started")
#         return
#     msg = await ctx.send(content="vote here")
#     await msg.add_reaction(YES)
#     await msg.add_reaction(NO)
#     vote_id = msg.id

# @bot.event
# async def on_reaction_add(reaction, user):
#     if user.bot:
#         return

#     msg = reaction.message
#     if msg.id != vote_id:
#         return

#     vote_stat[user.id] = str(reaction)
#     await reaction.remove(user)

@tree.command(name="endon",description="2択匿名投票の終了と結果表示")
async def endon(interaction: discord.Interaction):
    global isvote
    if not isvote:
        await interaction.response.send_message(content="vote not started")
        return
    # await interaction.response.defer()
    # print(vote_stat)
    isvote = False
    yes_count = sum(1 for value in vote_stat.values() if value == True)
    no_count = sum(1 for value in vote_stat.values() if value == False)
    await interaction.response.send_message(content=f"{YES}: {yes_count}\n{NO}: {no_count}")
    # try:
    #     await interaction.followup.send("")
    # except discord.HTTPException as e:
    #     pass
    # await vote_hook.edit(content=f"{YES}: {yes_count}\n{NO}: {no_count}", view=None)
    await vote_hook.delete()

client.run(os.environ.get("DISCORD_TOKEN"))