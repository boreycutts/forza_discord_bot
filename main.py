import random
import pickle
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import openai

season = 0

raps = [
"""
She hit my Nokia, I had to decline
I'm breaking her back and I'm cracking her spine
I'm getting that recognition, it's a sign
I'm on a mission, I ain't doing the crime (Bitch, okay)
Shooting shit like I'm Gilbert in his prime
Getting that sack, I'm feeling like I'm Hydes
You smoking on midget, you smoking on pine
I do not fuck with the Calvin or Klein
""",
"""
I'm smoking on gas, you smoking a novo
It's 2019, you still saying YOLO (Yes sir!)
I get Guiseppe, mix it with the polo (Wow!)
I'm getting that cream I'm getting that Froyo (Okay)
I hop on the scene I feel like a pogo (Yuh!)
Glock with the beam, I shoot like the logo (Okay)
I do not even really want a photo
She is a groupie, she is a no go
""",
"""
So slimy, I've been serving my pastor
You got a foreign but my Civic go faster
Strapped up like "Inglorious Basterds"
Serving junkies while I'm posted on Packard
Serving junkies up on Little Lake Drive
This ain't a diner, this is a dive
Hit the plug then I'm throwing him five
Geeked up 'cause I'm getting so live
""",
"""
Geeked up 'cause I know it's my time
How you rap but you can't even rhyme?
Poured a deuce in to my lemon lime
Sippin' goop, I don't fuck with the wine
Smoking on dope and I'm feeling sublime
If you wanna feature, gotta pay a fine
My glizzy is singing like it's Lil Shine
I'm eating chicken, I can't fuck with the swine
""",
"""
That bitch got thirty bodies, but you went on a date
I love my plug, so I gave him a plate (bitch)
He servin' that pack at a very low rate (okay)
You ask for a gram, but I give you the shake
These diamonds is drippin', gushin' like a lake (a lake)
He see the uzi, I Eternal Atake (Eternal Atake)
I'm countin' up guala, stackin' up the cake
I'm in an Impala skrrtin' from the jakes
""",
"""
Posted with BasedNas up in PG County (bitch)
Clean, like some Downy (yuh)
Grind for that sack, like Jadeveon Clowney (Jadevoen Clowney)
Price on his head, they're lookin' for a bounty
Keepin' an iron, like Robert Downey Jr
Twitter talkin', okay boomer (pew)
Bitch, I'm in Oklahoma, like a Sooner (pew, pew, pew)
""",
"""
She give me brain, call her a tutor (bitch)
You talkin' that shit, all I hear is a rumor (yuh)
Off of the shrooms, I call me an Uber (okay)
I love a bitch with a good sense of humor (yes)
Got me a pint of Wock' up in the cooler (yes)
You came out the mud, posted in the sewer
I need the love, ain't talkin' computers
Switchin' sides, I know you is a chooser (you is a chooser)
"""
]

tracks = {
    "Brands Hatch": [
        "Brands Hatch GP",
        "Brands Hatch Indy",
    ],
    "Circuit de Barcelona-Catalunya": [
        "Catalunya GP",
        "Catalunya National",
        "Catalunya National Alt",
    ],
    "Daytona International Speedway": [
        "Daytona 24Hr Sports Car",
        "Daytona Tri-Oval",
    ],
    "Eaglerock Speedway": [
        "Eaglerock Oval",
        "Eaglerock Club",
        "Eaglerock Club-R"
    ],
    "Grand Oak Raceway": [
        "Grand Oak National",
        "Grand Oak Club",
        "Grand Oak National-R",
    ],
    "Hakone": [
        "Hakone Grand Prix",
        "Hakone Club",
        "Hakone Club-R",
    ],
    "Hockenheim": [
        "Hockenheim",
        "Hockenheimring National",
        "Hockenheimring Short",
    ],
    "Homestead-Miami Speedway": [
        "Homestead Speedway",
        "Homestead Road",
    ],
    "Indianapolis Motor Speedway": [
        "Indianapolis Brickyard Oval",
        "Indianapolis GP",
    ],
    "Kyalami Grand Prix Circuit": [
        "Kyalami Grand Prix Circuit",
    ],
    "Lime Rock Park": [
        "Lime Rock Full",
        "Lime Rock South",
        "Lime Rock Full Alt",
    ],
    "Maple Valley": [
        "Maple Valley",
        "Maple Valley Short",
        "Maple Valley Short-R",
    ],
    "Michelin Raceway Road Atlanta": [
        "Road Atlanta",
        "Road Atlanta Short",
    ],
    "Mid-Ohio Sports Car Course": [
        "Mid-Ohio",
        "Mid-Ohio Short",
    ],
    "Mount Panorama Circuit": [
        "Bathurst",
    ],
    "Mugello Circuit": [
        "Mugello Full",
        "Mugello Club",
    ],
    "Nürburgring GP": [
        "Nürburgring GP",
        "Nürburgring Sprint"
    ],
    "Road America": [
        "Road America",
        "Road America East",
    ],
    "Sebring International Raceway": [
        "Sebring Full",
        "Sebring Short",
    ],
    "Silverstone Racing Circuit": [
        "Silverstone GP",
        "Silverstone National",
        "Silverstone International",
    ],
    "Sunset Peninsula": [
        "Sunset Peninsula Full",
        "Sunset Peninsula Club",
        "Sunset Peninsula Full-R",
        "Sunset Peninsula Speedway",
    ],
    "Suzuka Circuit": [
        "Suzuka Full",
        "Suzuka East",
    ],
    "Virginia International Raceway": [
        "VIR Full",
        "VIR North",
        "VIR South",
        "VIR Grand West",
        "VIR Grand East",
    ],
    "Watkins Glen International Speedway": [
        "Watkins Glen Full",
        "Watkins Glen Short",
    ],
    "WeatherTech Raceway Laguna Seca": [
        "Laguna Seca",
        "Laguna Seca Short",
    ],
    "Yas Marina Circuit": [
        "Yas Marina Full",
        "Yas Marina North",
        "Yas Marina South",
        "Yas Marina North Corkscrew",
    ],
}

classes = [
    "C",
    "B",
    "A",
    "S",
    "R",
]

races = []
teams = []

pst_tz = ZoneInfo("America/Los_Angeles")
est_tz = ZoneInfo("America/New_York")

RACE_START_TIME = 18 # 6:00 pm pst, 9:00 pm pst

def get_pst_now():
    return datetime.now(tz=pst_tz)

def get_est_now():
    return datetime.now(tz=est_tz)

def pst_to_est(pst_dt):
    return pst_dt.astimezone(est_tz)

def get_next_sunday_datetime(dt):
    sunday = 6
    days_until_sunday = (sunday - dt.weekday() + 7) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7
    next_sunday = dt + timedelta(days=days_until_sunday)
    return next_sunday

def get_next_wednesday_datetime(dt):
    wednesday = 3
    days_until_wednesday = (wednesday - dt.weekday() + 7) % 7
    if days_until_wednesday == 0:
        days_until_wednesday = 7
    next_sunday = dt + timedelta(days=days_until_wednesday)
    
    return next_sunday

def days_until_next(start_date, target_weekday_num):
    start_weekday = start_date.weekday()
    days_diff = (target_weekday_num - start_weekday + 7) % 7
    if days_diff == 0:
        days_diff = 7
    return days_diff


def league_start(league_season, number_of_races):
    global season
    print(f"Starting season {league_season}...")
    season = league_season
    league_save_season()

    class0 = classes[random.randint(0, len(classes)-1)]
    class1 = class0
    while class1 == class0:
        class1 = classes[random.randint(0, len(classes)-1)]
    main_tracks = list(tracks.keys())
    for i in range(number_of_races):
        current_tracks = [race["track"] for race in races]
        track = main_tracks[random.randint(0, len(main_tracks)-1)]
        while track in current_tracks:
            track = main_tracks[random.randint(0, len(main_tracks)-1)]
        subtracks = tracks[track]
        subtrack = subtracks[random.randint(0, len(subtracks)-1)]
        raceclass = class0 if i < number_of_races/2 else class1
        race = {
            "track": track,
            "subtrack": subtrack,
            "class": raceclass,
            "date": None
        }
        races.append(race)
    random.shuffle(races)

    dt_now = get_pst_now()

    excluded_dates = [
        date(2026, 2, 8), # Super Bowl weekend
    ]

    days_until_wednesday = days_until_next(dt_now, 2)
    days_until_sunday = days_until_next(dt_now, 6)
    current_dt = dt_now
    is_wednesday = False
    if days_until_wednesday < days_until_sunday:
        current_dt = dt_now + timedelta(days=days_until_wednesday)
        current_dt = current_dt.replace(hour=RACE_START_TIME, minute=0, second=0, microsecond=0)
        is_wednesday = True
    else:
        current_dt = dt_now + timedelta(days=days_until_sunday)
        current_dt = current_dt.replace(hour=RACE_START_TIME, minute=0, second=0, microsecond=0)
    for i in range(0, number_of_races, 2):
        print(current_dt.date())
        if current_dt.date() in excluded_dates:
            if is_wednesday:
                current_dt = current_dt + timedelta(days=4)
                is_wednesday = False
            else:
                current_dt = current_dt + timedelta(days=3) 
                is_wednesday = True
        if is_wednesday:
            races[i]["date"] = current_dt
            current_dt = current_dt + timedelta(hours=1)
            races[i+1]["date"] = current_dt
            current_dt = current_dt - timedelta(hours=1)
            current_dt = current_dt + timedelta(days=4)
            is_wednesday = False
        else:
            races[i]["date"] = current_dt
            current_dt = current_dt + timedelta(hours=1)
            races[i+1]["date"] = current_dt
            current_dt = current_dt - timedelta(hours=1)
            current_dt = current_dt + timedelta(days=3) 
            is_wednesday = True
    
    print("races = [")
    for race in races:
        print("\t" + str(race))
    print("]")
    league_save_races()

def league_save_season():
    with open(f"season.pkl", 'wb') as file:
        pickle.dump(season, file)
    print("Season saved successfully")

def league_load_season():
    global season
    try:
        with open("season.pkl", "rb") as file:
            season = pickle.load(file)
        print("Season loaded successfully")
    except FileNotFoundError:
        print("Error: The races file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def league_get_next_races():
    league_load_races()
    print("Next race:")
    now = get_pst_now()
    if now < races[0]["date"]:
        next_races = [races[0], races[1]]
        print(next_races)
        return(next_races)
    for i in range(len(races)):
        if i == len(races)-1:
            if now > races[i]["date"]:
                print("League is over goofy")
            else:
                next_races = [races[len(races)-1]]
                print(next_races)
                return next_races
        if races[i]["date"] > now:
            next_races = [races[i-1], races[i]]
            print(next_races)
            return next_races

def league_save_races():
    with open(f"races{season}.pkl", 'wb') as file:
        pickle.dump(races, file)
    print("Races saved successfully")

def league_load_races():
    global races
    try:
        with open(f"races{season}.pkl", "rb") as file:
            races = pickle.load(file)
        print("Races loaded successfully")
    except FileNotFoundError:
        print("Error: The races file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def league_save_teams():
    teams.sort(key=lambda team: team["points"], reverse=True)
    with open('teams.pkl', 'wb') as file:
        pickle.dump(teams, file)
    print("Teams saved successfully")
    print(teams)

def league_load_teams():
    global teams
    try:
        with open("teams.pkl", "rb") as file:
            teams = pickle.load(file)
        print("Teams loaded successfully")
    except FileNotFoundError:
        print("Error: The teams file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def league_reset_teams():
    global teams
    teams = []
    league_save_teams()

def league_reset_points():
    league_load_teams()
    for i in range(len(teams)):
        teams[i]["points"] = 0
    league_save_teams()

def league_add_team(user0, user1=None):
    global teams
    league_load_teams()
    if teams == None:
        teams = []
    teams.append({
        "user0": user0,
        "user1": user1,
        "points": 0
    })
    league_save_teams()

def league_remove_team(team_user):
    league_load_teams()
    team_index = None
    for i in range(len(teams)):
        if teams[i]["user0"] == team_user or teams[i]["user1"] == team_user:
            team_index = i
            break
    if team_index != None:
        teams.pop(team_index)
        league_save_teams()
        return True
    return False

def league_give_points(team_user, points, override=False):
    league_load_teams()
    team_index = None
    for i in range(len(teams)):
        if teams[i]["user0"] == team_user or teams[i]["user1"] == team_user:
            team_index = i
            break
    if team_index != None:
        if(override):
            teams[team_index]["points"] = points
        else:
            teams[team_index]["points"] += points
        league_save_teams()
        return True
    return False
        
league_load_season()
league_load_races()
league_load_teams()

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
token = os.getenv('TOKEN')
ai_key = os.getenv('OPENAI')
ai = openai.OpenAI(api_key=ai_key)
def ai_respond_to_user(msg):
    response = ai.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Someone said \"{msg}\" to our discord bot. Respond as the bot in an angry and aggressive tone"}
        ]
    )
    return response.choices[0].message.content.split("\n")[0]

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)
@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))

@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    if message.author == bot.user:
        return
    if "motorsport bot" in message.content or "bot" in message.content:
        print("Uh oh the bot mad as hell")
        await message.channel.send(ai_respond_to_user(message.content))
    if "hello" in user_message.lower():
        await message.channel.send(f"Shut yo bitch ass up we don't say hello in here 😤")
        return
    if "rap" in user_message.lower():
        rap = random.choice(raps)
        await message.channel.send(rap);
        return
    await bot.process_commands(message)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Commands",
        description="Here is a list of all available commands:",
        colour=discord.Color.blue()
    )
    embed.add_field(name="`!ping`", value="Responds with 'Pong!", inline=False)
    embed.add_field(name="`!next_races`", value="Get the upcoming races", inline=False)
    embed.add_field(name="`!standings`", value="Get the current league standings", inline=False)
    if ctx.channel.name == "commands":
        embed.add_field(name="`!start_league <season> <N>`", value="Starts the league for season <season> and creates a random set of <N> races", inline=False)
        embed.add_field(name="`!reset_teams`", value="Erase the teams list", inline=False)
        embed.add_field(name="`!reset_points`", value="Set all team points to 0", inline=False)
        embed.add_field(name="`!add_team <@user0> <@user1>`", value="Add a team with @user0 and @user1 as team members", inline=False)
        embed.add_field(name="`!remove_team <@user0/1>`", value="Remove the team that @user0 or @user1 is on", inline=False)
        embed.add_field(name="`!give_points <@user0/1> <points> <override=False>`", value="Give <points> to the team that @user0 or @user1 is on. Pass in <True> for override to set the points instead of adding.", inline=False)
        embed.add_field(name="`!set_place <@user0/1> <place>`", value="Set the place for the team that @user0 or @user1 is on so they get points.", inline=False)
    
    # embed.add_field(name="`!ping`", value="Responds with 'Pong!'", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
  await ctx.send('Pong!')

@bot.command()
async def next_races(ctx):
    next_races = league_get_next_races()
    embed = discord.Embed(
        title=f"Upcomming Races:",
        description=None,
        colour=discord.Color.blue()
    )
    for race in next_races:
        dt_est = pst_to_est(race["date"])
        datestr = race["date"].strftime("%A %B %d, %-I %p") + " PST [" + dt_est.strftime("%-I %p") + " EST]"
        raceclass = race["class"]
        track = race["track"]
        subtrack = race["subtrack"]
        valuestr = f"**Class:** {raceclass}\n**Track:** {track}\n**Subtrack:** {subtrack}"
        embed.add_field(name=f"`{datestr}`", value=valuestr, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def standings(ctx):
    league_load_teams()
    embed = discord.Embed(
        title=f"Current Standings:",
        description="Here's how the season's going:",
        colour=discord.Color.blue()
    )
    for i in range(len(teams)):
        team = teams[i]
        user0 = team["user0"]
        user1 = team["user1"]
        names = None
        if user1 == None:
            names = f"@{user0}"
        else:
            names = f"@{user0} and @{user1}"
        points = str(team["points"])
        if i == 0:
            embed.add_field(name=f"`🥇 1st: {names}`", value=points, inline=False)
        elif i == 1:
            embed.add_field(name=f"`🥈 2nd: {names}`", value=points, inline=False)
        elif i == 2:
            embed.add_field(name=f"`🥉 3rd: {names}`", value=points, inline=False)
        elif i == 3:
            embed.add_field(name=f"`✅ 4th: {names}`", value=points, inline=False)
        elif i == 4:
            embed.add_field(name=f"`👍 5th: {names}`", value=points, inline=False)
        elif i == 5:
            embed.add_field(name=f"`😕 6th: {names}`", value=points, inline=False)
        elif i == 6:
            embed.add_field(name=f"`👎 7th: {names}`", value=points, inline=False)
        elif i == 7:
            embed.add_field(name=f"`💩 8th: {names}`", value=points, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def start_league(ctx, season, number_of_races):
    global races
    if ctx.channel.name == "commands":
        in_progress = os.path.isfile(f"races{season}.pkl")
        try:
            cont = True
            if in_progress:
                await ctx.send(f"League in progress do you want to restart? [y/n]")
                print("waiting...")
                res = await bot.wait_for(
                    "message",
                    check=lambda x: x.channel.id == ctx.channel.id
                    and ctx.author.id == x.author.id
                    and x.content.lower() == "y"
                    or x.content.lower() == "n",
                    timeout=None,
                )
                print(f"Got res {res.content}")
                cont = res.content == "y"
            if cont:
                league_start(int(season), int(number_of_races))
                await ctx.send(f"League started...")
                embed = discord.Embed(
                    title=f"OG Motorsport League Season {season}",
                    description="Here's the races for the upcomming season:",
                    colour=discord.Color.blue()
                )
                for race in races:
                    dt_est = pst_to_est(race["date"])
                    datestr = race["date"].strftime("%A %B %d, %-I %p") + " PST [" + dt_est.strftime("%-I %p") + " EST]"
                    raceclass = race["class"]
                    track = race["track"]
                    subtrack = race["subtrack"]
                    valuestr = f"Class: {raceclass}\nTrack: {track}\nSubtrack: {subtrack}"
                    embed.add_field(name=f"`{datestr}`", value=valuestr, inline=False)
                await ctx.send(embed=embed)
                await ctx.send(f"Publish? [y/n]")
                print("waiting...")
                res = await bot.wait_for(
                    "message",
                    check=lambda x: x.channel.id == ctx.channel.id
                    and ctx.author.id == x.author.id
                    and x.content.lower() == "y"
                    or x.content.lower() == "n",
                    timeout=None,
                )
                print(f"Got res {res.content}")
                if res.content == "y":
                    channel = discord.utils.get(ctx.guild.channels, name="league-stuff")
                    msg = await channel.send(embed=embed)
                    await msg.pin()
                else:
                    races = []
                    try:
                        os.remove(f"races{season}.pkl")
                    except OSError:
                        pass
        except Exception as e:
            await ctx.send(f"{e}")

def cmd_access(ctx):
    print(ctx.author.display_name)
    return ctx.channel.name == "commands" and (ctx.author.display_name == "boreycutts" or ctx.author.display_name == "deathr0w927")

@bot.command()
async def reset_teams(ctx):
  if cmd_access(ctx):
    await ctx.send(f"This can't be undone and will be a pain in the ass to redo. Are you sure? [y/n]")
    print("waiting...")
    res = await bot.wait_for(
        "message",
        check=lambda x: x.channel.id == ctx.channel.id
        and ctx.author.id == x.author.id
        and x.content.lower() == "y"
        or x.content.lower() == "n",
        timeout=None,
    )
    print(f"Got res {res.content}")
    if res.content == "y":
        league_reset_teams()
        await ctx.send('Teams cleared')

@bot.command()
async def reset_points(ctx):
  if cmd_access(ctx):
    await ctx.send(f"This can't be undone and will be a pain in the ass to redo. Are you sure? [y/n]")
    print("waiting...")
    res = await bot.wait_for(
        "message",
        check=lambda x: x.channel.id == ctx.channel.id
        and ctx.author.id == x.author.id
        and x.content.lower() == "y"
        or x.content.lower() == "n",
        timeout=None,
    )
    print(f"Got res {res.content}")
    if res.content == "y":
        league_reset_points()
        await ctx.send('Points cleared')

@bot.command()
async def add_team(ctx, user0:discord.Member, user1:discord.Member=None):
  if cmd_access(ctx):
    user0name = user0.display_name
    user1name = None
    if user1 != None:
        user1name = user1.display_name
    league_add_team(user0name, user1=user1name)
    await ctx.send('Added team')

@bot.command()
async def remove_team(ctx, team_user):
  if cmd_access(ctx):
    await ctx.send(f"This can't be undone and will be a pain in the ass to redo. Are you sure? [y/n]")
    print("waiting...")
    res = await bot.wait_for(
        "message",
        check=lambda x: x.channel.id == ctx.channel.id
        and ctx.author.id == x.author.id
        and x.content.lower() == "y"
        or x.content.lower() == "n",
        timeout=None,
    )
    print(f"Got res {res.content}")
    if res.content == "y":
        if league_remove_team(team_user) == False:
            await ctx.send('Team not found')
        else:
            await ctx.send('Team removed')

@bot.command()
async def give_points(ctx, team_user:discord.Member, points, override=False):
  if cmd_access(ctx):
    team_username = team_user.display_name
    print(f"Giving {team_username} {points} points [override={override}]")
    ret = league_give_points(team_username, int(points), override=override)
    if ret:
        if override:
            await ctx.send(f'Team @{team_username} now has {points} points')
        else:
            await ctx.send(f'Team @{team_username} got {points} points')
    else:
        await ctx.send('Team not found')

place_map = {
    "1": 25,
    "2": 18,
    "3": 15,
    "4": 12,
    "5": 10,
    "6": 8,
    "7": 6,
    "8": 4,
    "9": 2,
    "10": 1,
}
@bot.command()
async def set_place(ctx, team_user:discord.Member, place):
    if ctx.channel.name == "commands":
        points = place_map[place]
        team_username = team_user.display_name
        ret = league_give_points(team_username, points)
        if ret:
            await ctx.send(f'Team @{team_username} got {points} points')
        else:
            await ctx.send('Team not found')

# client.run(token)
bot.run(token)