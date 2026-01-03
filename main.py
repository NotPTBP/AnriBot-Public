#dependencies
from enum import member
from operator import truediv

import discord
from discord.app_commands.checks import has_role
from discord.ext import commands
from discord.ui import View, Button
import logging
from dotenv import load_dotenv
from math import floor
import os
import webservice
import json


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

#setup
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.polls = True
intents.reactions = True
intents.webhooks = True


secret_role = "anritest"
mods_role = "Mods test"
STATS_FILE = "stats.json"
STAT_FIELDS = ["Dribble", "IQ field", "Pass", "Shoot", "Offense", "Defense"]
myid = 1386741175469215774
LOG_LOG_FILE = "message_logs.txt"

#prefix
bot = commands.Bot(command_prefix='.', intents=intents)
tree = bot.tree

@bot.event #making her online

async def on_ready():
    print(f"{bot.user} is on celebrate (ID: {bot.user.id})")
    try:
        synced = await tree.sync()
        print(f"And slash command works")
    except Exception as e:
        print(f"you failed as a dev here's the error: {e}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to Marseille {member.name} !")


@bot.event
async def on_message(message):

    user_id = message.author.id
    print(f"{message.author} has user ID {user_id} with content: {message.content}")

    if message.author == bot.user:
        return


banned_words = [
    "nigger", "n1gger", "ni99er", "nigga", "n1gga", "ni99a",
    "faggot", "f4ggot", "fa99ot", "fag", "f4g", "fa9",
    "retard", "r3tard", "reeetard", "ret@rd", "r3t@rd",
    "tranny", "tr4nny", "tr4nni", "trannie",
    "kike", "kyke", "k1ke", "ki1ke",
    "spic", "sp1c", "sp!c",
    "coon", "k00n", "c00n",
    "chink", "ch1nk", "ch!nk",
    "gook", "g00k", "g0ok",
    "wetback", "w3tback", "wetb4ck",
    "towelhead", "t0welhead", "towelh3ad",
    "sandnigger", "sandni99er", "sandn1gger",
    "rape", "r4pe", "raape", "rap3",
    "rapist", "r4pist", "rap1st",
    "molest", "molester", "m0lest", "m0lester",
    "pedophile", "pedo", "paedo", "p3do", "ped0",
    "groom", "groomer", "gr00m", "gr00mer",
    "incest", "inc3st",
    "bestiality", "b3stiality",
    "zoophilia", "zo0philia",
    "kill", "k1ll", "ki1l", "k!ll",
    "murder", "murdr", "murda",
    "suicide", "su1cide", "suiside",
    "kms", "killmyself", "k1llmyself",
    "kys", "k1llyourself", "killurself",
    "selfharm", "self-harm", "s3lfharm",
    "cutting", "cutmyself", "slitwrists",
    "die", "d13", "d1e",
    "dead", "d3ad", "d34d",
    "terrorist", "t3rrorist", "terr0rist",
    "bomb", "b0mb", "b0m8",
    "explode", "expl0de", "explod3",
    "shoot", "sh00t", "sh0ot",
    "schoolshoot", "schoolsh00t",
    "gun", "gunn", "guhn",
    "nazis", "nazi", "n4zi",
    "hitler", "h1tler", "h!tler",
    "holocaust", "hol0caust",
    "gaschamber", "g4schamber",
    "lynch", "l1nch", "l!nch",
    "hang", "h4ng", "h@ng",
    "slut", "slutt", "slvt",
    "whore", "wh0re", "whor3",
    "hoe", "h03", "h0e",
    "cumdumpster", "cumdumper",
    "rapeplay", "forcedsex",
    "nonconsensual", "noncon", "cnc",
    "gore", "g0re", "g0r3",
    "dismember", "dism3mb3r",
    "decapitate", "dec4pitate",
    "behead", "b3head",
    "necrophilia", "n3crophilia",
    "snuff", "snuf", "snuhff",
    "blood", "bl00d", "bl0od",
    "cannibal", "c4nnibal",
    "cannibalism", "c4nnibalism",
    "childporn", "cp", "c.p.", "c\\*p",
    "lolicon", "lolic0n", "l0licon",
    "shotacon", "sh0tacon",
    "nsfw", "n.s.f.w", "nsf\\*w",
    "lewd", "lewds", "lewdd",
    "onlyfans", "0nlyfans", "onlyfanz",
    "porn", "pr0n", "p0rn",
    "porno", "p0rn0",
    "nudes", "n00des", "nudez",
    "dickpic", "d1ckpic", "dicpic",
    "boobpic", "b00bpic", "boobpick",
    "anal", "4nal", "an@l",
    "deepthroat", "deepthr0at",
    "69ing", "sixtynine",
    "blowjob", "bl0wjob", "blowj0b",
    "handjob", "handj0b", "h4ndjob",
    "cum", "cumm", "cvm",
    "jizz", "j1zz", "j!zz",
    "masturbate", "masturb8", "mast3rbate",
    "fap", "f@p", "phap",
    "orgasm", "0rgasm", "0rgazm",
    "moan", "m0an", "mo@n",
    "clit", "cl1t", "cl!t",
    "pussy", "pussi", "pussie", "p\\*ssy",
    "vagina", "v4gina", "v@gina",
    "cock", "c0ck", "c\\*ck",
    "dick", "d1ck", "d!ck",
    "penis", "p3nis", "pen1s",
    "ballsack", "b4llsack",
    "testicles", "t3sticles",
    "butthole", "buttho1e",
    "asshole", "assh0le", "a55hole",
    "rimjob", "r1mjob", "rimj0b",
    "suck", "sux", "suckk",
    "lick", "l1ck", "lickk",
    "thot", "th0t", "th0ttie",
    "camgirl", "camboi", "camboy",
    "escort", "esc0rt", "esc0rts",
    "prostitute", "pr0stitute", "pr0st1tute",
    "pimp", "p1mp", "p!mp",
    "drug", "drugs", "drvg",
    "weed", "we3d", "w33d",
    "cocaine", "c0caine", "c0k3",
    "crack", "cr4ck", "krack",
    "meth", "m3th", "methh",
    "heroin", "her0in", "her0ine",
    "lsd", "acidtrip",
    "shrooms", "shr00ms", "shro0ms",
    "ecstasy", "3cstasy", "exstacy",
    "ketamine", "k3tamine", "k3ta",
    "fentanyl", "f3ntanyl", "fentanil",
    "overdose", "0verdose", "0verd0se",
    "dealer", "d3aler", "de4ler",
    "cartel", "c4rtel", "cart3l",
    "smuggle", "smuggler", "smuggl3"
    "goon", "gooning", "edging", "edgeplay", "ruinedorgasm",
    "futa", "futanari", "yiff", "yiffy", "furryfucking",
    "creampie", "creampies", "bukkake", "bukkakke",
    "facial", "cumshot", "cumslut", "cumdump", "cumdumpster",
    "gloryhole", "gloryholes", "gangbang", "gangbanged",
    "dp", "doublepenetration", "triplepenetration",
    "spitroast", "spitroasting",
    "anal", "deepthroat", "deepthroating",
    "throatfuck", "throatfucking", "facefuck",
    "felch", "felching",
    "snowballing", "snowball",
    "rimjob", "rimming", "analingus",
    "prolapse", "rosebud", "analprolapse",
    "breeding", "breeder", "breedme",
    "breedingkink", "breedingfetish",
    "ddlg", "daddydom", "littlespace",
    "ageplay", "abdl", "adultbaby",
    "mommydom", "mdlb", "cgl",
    "cockvore", "vore", "unbirth",
    "tentacle", "tentaclesex",
    "pegging", "pegged", "strapon", "strap-ons",
    "pissing", "watersports", "goldenshower",
    "scat", "scatplay", "coprophilia",
    "vomitplay", "emeto", "emetoophilia",
    "enema", "enemas", "enemaplay",
    "fisting", "fisted", "doublefisting",
    "sounding", "soundplay",
    "cbt", "cockandballtorture",
    "humiliation", "degradation", "degrading",
    "slutplay", "sluttraining", "whoretraining",
    "findom", "financialdomination",
    "chastity", "chastitycage",
    "keyholder", "cuckold", "cuck",
    "cuckquean", "hotwife",
    "bull", "bulls", "breederbull",
    "alpha", "betaorbiter",
    "bdsm", "bondage", "shibari",
    "hogtie", "hogtied", "ropebondage",
    "sensorydeprivation", "forcedorgasm",
    "forcedbi", "hypnokink", "hypnosmut",
    "hypnofetish", "hypno",
    "mindcontrol", "brainwash",
    "consensualnonconsent", "cnc", "ravish",
    "ravishment", "noncon", "non-consensual",
    "rapeplay", "rapefantasy", "forceplay",
    "slave", "master", "mistress",
    "dominatrix", "dominance", "submission",
    "submissive", "sub", "dom", "domme",
    "petplay", "puppyplay", "kittenplay",
    "collar", "leash", "kennel",
    "breathplay", "asphyxiation",
    "choking", "chokeplay",
    "sensualhumiliation", "sexslave",
    "porn", "pr0n", "pornhub",
    "onlyfans", "onlyfan", "onlyfanz",
    "lewds", "lewd", "lewded",
    "nsfw", "n.s.f.w", "nsf\\*w"
]


# Pre-compile a regex
banned_pattern = re.compile(r"|".join(re.escape(word) for word in banned_words), re.IGNORECASE)

@bot.command()
@commands.has_permissions(administrator=True)
async def removebadword(ctx, *, word):
    if word.lower() in banned_words:
        banned_words.remove(word.lower())
        await ctx.send(f"✅ Removed '{word}' from banned words.")
    else:
        await ctx.send("❌ That word isn't in the list.")

@bot.command()
@commands.has_permissions(administrator=True)
async def addbadword(ctx, *, word):
    if word.lower() not in banned_words:
        banned_words.append(word.lower())
        await ctx.send(f"✅ Added '{word}' to banned words.")
    else:
        await ctx.send("❌ That word is already banned.")
        
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if banned_pattern.search(message.content):
        try:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, I'll mangle you")
        except discord.Forbidden:
            print("❌ Cannot delete message in this channel.")


    await bot.process_commands(message)


# .hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def reply(ctx):
    await (ctx.reply(f"I'm replying to your message {ctx.author.mention}!"))

@bot.command()
async def poll(ctx):
    embed = discord.Embed(title="Y'all I'm working", description="are y'all happy about it ?")
    poll_message = await ctx.send(embed=embed)
    await ctx.message.delete()
    await poll_message.add_reaction("💯")
    await poll_message.add_reaction("💔")
    await ctx.send(f"<@&1363291651057123530>")

@bot.command()
async def training(ctx):
    embed = discord.Embed(title="HOST INCOMING", description="Training session")
    poll_message = await ctx.send(embed=embed)
    await ctx.message.delete()
    await poll_message.add_reaction("💯")
    await poll_message.add_reaction("💔")
    await ctx.send(f"<@&1363291651057123530>")

@bot.command()
async def test(ctx):
    embed = discord.Embed(title="TESTING", description="don't mind this, I'm trying to see if y'all get pinged through the bot, does it work though ?")
    poll_message = await ctx.send(embed=embed)
    await ctx.message.delete()
    await poll_message.add_reaction("✅")
    await poll_message.add_reaction("❌")
    await ctx.send(f"<@&1363291651057123530>")

@bot.command()
@commands.has_role("Mods_test")
async def say(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)


@bot.command()
@commands.has_role("Mods_test")
@commands.has_permissions(manage_roles=True)
async def s_assign(ctx, member: discord.Member, role: discord.Role):
    bot_member = ctx.guild.me
    if role.position >= bot_member.top_role.position:
        await ctx.send("❌ I can't remove a role higher or equal to my own top role!")
        return

    if role.position >= member.top_role.position:
        await ctx.send(f"❌ Can't remove {role.name} because it's higher or equal to {member.display_name}'s highest role!")
        return

    await member.remove_roles(role)
    await ctx.send(f"✅ Removed {role.name} from {member.mention}")

@bot.command()
@commands.has_role("Mods_test")
@commands.has_permissions(manage_roles=True)
async def m_assign(ctx, role: discord.Role, *members: discord.Member):
    for member in members:
        try:
            await member.add_roles(secret_role)
        except discord.Forbidden:
            await ctx.send(f"Can't add role to {member.mention}")
    await ctx.send(f"Assigned {role.name} to {len(members)} user(s)")

@bot.command()
@commands.has_role("Mods_test")
@commands.has_permissions(manage_roles=True)
async def s_remove(ctx, member: discord.Member, role: discord.Role):
    bot_member = ctx.guild.me
    if role.position >= bot_member.top_role.position:
        await ctx.send("❌ I can't remove a role higher or equal to my own top role!")
        return

    if role.position >= member.top_role.position:
        await ctx.send(f"❌ Can't remove {role.name} because it's higher or equal to {member.display_name}'s highest role!")
        return

    await member.remove_roles(role)
    await ctx.send(f"✅ Removed {role.name} from {member.mention}")

@bot.command()
@commands.has_role("Mods_test")
@commands.has_permissions(manage_roles=True)
async def m_remove(ctx, role: discord.Role, *members: discord.Member):
    for member in members:
        try:
            await member.remove_roles(secret_role)
        except discord.Forbidden:
            await ctx.send(f"Can't remove role to {member.mention}")
    await ctx.send(f"Removed {role.name} to {len(members)} user(s)")

@bot.command()
async def replyto(ctx, message_id: int, *, content: str):
    try:
        # Fetch the message from the current channel
        target_message = await ctx.channel.fetch_message(message_id)
        await target_message.reply(content)
    except discord.NotFound:
        await ctx.send("Message not found.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to reply.")
    except discord.HTTPException as e:
        await ctx.send(f"Failed to send reply: {e}")

# File loading/saving
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_stats(data):
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_total(entry):
    values = [entry.get(stat, 0) for stat in STAT_FIELDS]
    return floor(sum(values) / len(STAT_FIELDS))

def build_leaderboard_pages():
    data = load_stats()
    sorted_data = sorted(data.items(), key=lambda x: x[1]["Total"], reverse=True)

    entries = []
    for i, (uid, entry) in enumerate(sorted_data, start=1):
        block = (
            f"{i}. {entry['name']} — Total: {entry['Total']}\n"
            f"   Dribble: {entry['Dribble']} | IQ field: {entry['IQ field']} | Pass: {entry['Pass']}\n"
            f"   Shoot: {entry['Shoot']} | Offense: {entry['Offense']} | Defense: {entry['Defense']}\n"
        )
        entries.append(block)

    pages = []
    for i in range(0, len(entries), 10):  # 10 users per page
        page = "".join(entries[i:i+10])
        pages.append(page)

    return pages

class LeaderboardView(View):
    def __init__(self, pages, author):
        super().__init__(timeout=60)
        self.pages = pages
        self.current = 0
        self.author = author

    async def send_page(self, interaction):
        embed = discord.Embed(
            title="🏆 Stats Leaderboard",
            description=f"```{self.pages[self.current]}```",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Page {self.current + 1} of {len(self.pages)}")
        await interaction.response.edit_message(embed=embed, view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("❌ You can’t control this leaderboard.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.secondary, row=0)
    async def first_page(self, interaction: discord.Interaction, button: Button):
        self.current = 0
        await self.send_page(interaction)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary, row=0)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        self.current = (self.current - 1) % len(self.pages)
        await self.send_page(interaction)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary, row=0)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        self.current = (self.current + 1) % len(self.pages)
        await self.send_page(interaction)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.secondary, row=0)
    async def last_page(self, interaction: discord.Interaction, button: Button):
        self.current = len(self.pages) - 1
        await self.send_page(interaction)


@bot.command()
@commands.has_role("Tryout_Hoster")
async def setstats(ctx, member: discord.Member, dribble: int, iq: int, pas: int, shoot: int, offense: int, defense: int):
    data = load_stats()
    uid = str(member.id)
    data[uid] = {
        "name": str(member),
        "Dribble": dribble,
        "IQ field": iq,
        "Pass": pas,
        "Shoot": shoot,
        "Offense": offense,
        "Defense": defense
    }
    data[uid]["Total"] = calculate_total(data[uid])
    save_stats(data)
    await ctx.send(f"✅ Full stats set for {member.mention}.")

@bot.command()
@commands.has_role("Tryout_Hoster")
async def editstats(ctx, member: discord.Member, field: str, value: int):
    data = load_stats()
    uid = str(member.id)

    if uid not in data:
        await ctx.send("❌ User not found.")
        return

    field = field.capitalize()
    if field == "Iq":
        field = "IQ field"

    if field not in STAT_FIELDS:
        await ctx.send(f"❌ Invalid stat. Use one of: {', '.join(STAT_FIELDS)}")
        return

    data[uid][field] = value
    data[uid]["Total"] = calculate_total(data[uid])
    save_stats(data)
    await ctx.send(f"🛠️ Updated {field} for {member.mention} to `{value}`. New total: `{data[uid]['Total']}`.")

@bot.command()
async def stats(ctx):
    pages = build_leaderboard_pages()
    if not pages:
        await ctx.send("📉 No stats available.")
        return

    data = load_stats()
    sorted_users = sorted(data.items(), key=lambda x: x[1]["Total"], reverse=True)
    user_id = str(ctx.author.id)

    # Find user's rank
    user_rank = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == user_id), None)
    total_users = len(sorted_users)

    # Leaderboard embed with rank note
    rank_note = f"📍 You are ranked **#{user_rank}** out of **{total_users}** users\n\n" if user_rank else ""

    embed = discord.Embed(
        title="🏆 Stats Leaderboard",
        description=rank_note + f"```{pages[0]}```",
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Page 1 of {len(pages)}")

    view = LeaderboardView(pages, ctx.author)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def mystats(ctx, member: discord.Member = None):
    user = member or ctx.author
    data = load_stats()
    uid = str(user.id)

    if uid not in data:
        await ctx.send("❌ No stats found for this user.")
        return

    # Get the user's stat entry
    stats = data[uid]

    # Compute rank
    sorted_users = sorted(data.items(), key=lambda x: x[1]["Total"], reverse=True)
    user_rank = next((i + 1 for i, (user_id, _) in enumerate(sorted_users) if user_id == uid), None)
    total_users = len(sorted_users)

    # Format the embed
    embed = discord.Embed(
        title=f"📊 Stats for {user.display_name}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Dribble", value=stats["Dribble"], inline=True)
    embed.add_field(name="IQ field", value=stats["IQ field"], inline=True)
    embed.add_field(name="Pass", value=stats["Pass"], inline=True)
    embed.add_field(name="Shoot", value=stats["Shoot"], inline=True)
    embed.add_field(name="Offense", value=stats["Offense"], inline=True)
    embed.add_field(name="Defense", value=stats["Defense"], inline=True)
    embed.add_field(name="Total", value=stats["Total"], inline=True)
    embed.set_footer(text=f"📍 Ranked #{user_rank} out of {total_users}")

    await ctx.send(embed=embed)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("🚫 You don't have permission to use this command.")

@bot.command()
@has_role("Tryout_Hoster")
async def removestats(ctx, member: discord.Member):
    data = load_stats()
    uid = str(member.id)

    if uid in data:
        del data[uid]
        save_stats(data)
        await ctx.send(f"🗑️ Stats for {member.mention} have been removed.")
    else:
        await ctx.send("❌ No stats found for that user.")



webservice.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.INFO)