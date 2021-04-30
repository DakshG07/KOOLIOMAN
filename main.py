import guilded
from guilded.ext import commands

bot = commands.Bot(command_prefix='~', owner_id='R40y3pEd')
warriors = ['jake', 'bob']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(int(times)):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: guilded.Member):
    """Says when a member joined."""
    print(dir(member))
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

#Guilded Only
@bot.command()
async def setxp(ctx, member: guilded.Member, xp: int):
  try:
    await member.edit(xp=xp)
  except:
    await ctx.send("There was an error. I may have insufficient role permissions. Please fix the issue and try again.")
  else:
    await ctx.send(f"Successfully set {member.name}'s XP to {xp}.")


bot.run('xenigib207@quossum.com', 'KOOLIOMAN123')